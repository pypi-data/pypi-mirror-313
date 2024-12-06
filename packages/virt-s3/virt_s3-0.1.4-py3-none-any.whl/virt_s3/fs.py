from virt_s3.utils import get_custom_logger, ImageFormatType, archive_zip_as_buffer, KB, MB

from io import BytesIO
from dataclasses import dataclass as pydataclass
from typing import List, Generator, Union, Any, Dict, Optional

import os, shutil, pathlib, zipfile, base64, traceback

logger = get_custom_logger()


# Numpy and Pillow
try: 
    from PIL import Image
except ModuleNotFoundError as me:
    class Image:
        class Image: 
            pass
    logger.warning(f"{me} -> `$ poetry install -E image` to use.")

try: 
    import numpy as np
except ModuleNotFoundError as me:
    class np:
        class ndarray:
            pass
    logger.warning(f"{me} -> `$ poetry install -E image` to use.")



@pydataclass
class LocalFSParams:
    """Dataclass for Using Local File System for all S3 Calls
    
    :param use_local_fs: flag to use the local file system or not for S3 calls
    :param root_dir: local file system root dir that represents your 'bucket'
    :param user: your username
    :param bucket_name: emulated S3 'bucket' directory in file system within root dir
    """
    use_local_fs: bool
    root_dir: str
    user: str
    bucket_name: str


class LocalFSSessionManager:
    """Session Context Manager for Local File System

    :param local_fs_params: instance of LocalFSParams, defaults to None
    :param client: existing session client can be passed in, defaults to None
    :param keep_open: boolean flag to keep the session open or not outside of the context manager scope, defaults to False
    """
    def __init__(
        self,
        local_fs_params: LocalFSParams = None,
        client = None,
        keep_open: bool = False,
        **session_client_kwargs
    ) -> None:
        # use default if not provided
        if local_fs_params is None: 
            local_fs_params = get_local_fs_params()
        self.local_fs_params = local_fs_params
        self.client = client
        self.kwargs = session_client_kwargs
        self.keep_open = keep_open
        self.status = None

    def __enter__(self): 
        self.status = "open"
        return self.client

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.keep_open is False:
            self.status = "closed"
        
        if exc_value or exc_type or exc_tb:
            logger.error(f"LocalFSSessionError: {exc_type}:{exc_value}")
            # traceback.print_exception(exc_type, exc_value, exc_tb)
            return False


##############################################################
################ Local File System Functions #################
##############################################################


def get_local_fs_params() -> LocalFSParams:
    """Function to get local file system parameters.

    Checks for the following Environment Variables:
    1. LOCAL_FS -> 1 or 0 (indicating whether to use local filesystem or not. 1 is True, 0 is False). Default behavior is False.
    2. LOCAL_FS_ROOT_DIR -> path to local file system root dir
    3. LOCAL_FS_USER -> username (email address) for app you're trying to emulate
    4. S3_DEFAULT_BUCKET -> bucket name proxy for local file system. Defaults to 'default_bucket'.

    :return: instance of LocalFSParams
    """
    logger.debug(f"Getting Local FS Params ...")
    use_local: bool = True
    if os.getenv('LOCAL_FS', "0") == "0": use_local = False
    root_dir: str = os.getenv('LOCAL_FS_ROOT_DIR', os.path.join(os.getcwd(), 'tests/data'))
    user = os.getenv('LOCAL_FS_USER', "default@default.com")
    bucket_name = os.getenv('S3_DEFAULT_BUCKET', 'default-bucket')
    return LocalFSParams(use_local_fs=use_local, root_dir=root_dir, user=user, bucket_name=bucket_name)


def fix_fs_path(
    fpath: str, 
    local_fs_params: LocalFSParams,
) -> str:
    """Function to fix the file or directory path on a local file system
    according to root directory from LocalFSParams. Checks to see if root directory
    is in the path or not and fixes it to be a valid path. Else, it joins the root
    directory with the input path

    :param fpath: input path
    :param local_fs_params: instance of LocalFSParams
    :return: updated file system path
    """
    logger.debug(f"Fixing File Path to Fit Local FS: {fpath}")
    # check if fpath has already been fixed
    if fpath.startswith(os.path.join(local_fs_params.root_dir, local_fs_params.bucket_name)):
        return fpath

    # split by directory
    tmp_path_components = fpath.strip("/").split("/")
    tmp_root_dir = local_fs_params.root_dir.strip("/")

    # find matching path parts - see if root dir in key file path
    # assume root dir in key
    root_dir_in_key, bucket_in_key = True, True
    for component in tmp_root_dir.split("/"):
        if component not in tmp_path_components:
            root_dir_in_key = False
    
    last_root_dir_component = component
    
    # find if bucket already in file path or not
    # assume bucket name in key by default
    if local_fs_params.bucket_name:
        if local_fs_params.bucket_name not in tmp_path_components: bucket_in_key = False
    else: bucket_in_key = False
        
    ## Logic Conditions:
    # 1. root dir in save key & bucket name not in save key
    if root_dir_in_key and not bucket_in_key:
        # new start index = last component of root dir path index + 1
        new_path_start_index = tmp_path_components.index(last_root_dir_component) + 1
        new_path = "/".join(tmp_path_components[new_path_start_index:])
        # if bucket name is in root dir last component
        if local_fs_params.bucket_name in last_root_dir_component:
            return os.path.join(local_fs_params.root_dir, new_path)
        return os.path.join(local_fs_params.root_dir, local_fs_params.bucket_name, new_path)
    # 2. root dir in save key & bucket name in save key
    elif root_dir_in_key and bucket_in_key:
        # get index of last root dir component
        root_dir_end_index = tmp_path_components.index(last_root_dir_component)
        # get index of bucket name
        bucket_index = tmp_path_components.index(local_fs_params.bucket_name)
        # make sure bucket index comes after root dir end
        new_path = "/".join(tmp_path_components[bucket_index+1:])        
        if bucket_index < root_dir_end_index:
            new_path = "/".join(tmp_path_components[root_dir_end_index+1:])
        # if bucket name is in root dir last component
        if local_fs_params.bucket_name in last_root_dir_component:
            return os.path.join(local_fs_params.root_dir, new_path)
        return os.path.join(local_fs_params.root_dir, local_fs_params.bucket_name, new_path)

    # 3. root dir not in save key & bucket name in save key
    elif not root_dir_in_key and bucket_in_key:
        # get index of bucket name
        bucket_index = tmp_path_components.index(local_fs_params.bucket_name)
        new_path = "/".join(tmp_path_components[bucket_index+1:])
        # if bucket name is in root dir last component
        if local_fs_params.bucket_name in last_root_dir_component:
            return os.path.join(local_fs_params.root_dir, new_path)
        return os.path.join(local_fs_params.root_dir, local_fs_params.bucket_name, new_path)

    # 4. root dir not in save key & bucket name not in save key
    # if bucket name is in root dir last component
    if local_fs_params.bucket_name in last_root_dir_component:
        return os.path.join(local_fs_params.root_dir, fpath)
    return os.path.join(local_fs_params.root_dir, local_fs_params.bucket_name, fpath)


def create_fs_bucket(
    bucket_path: str, 
    local_fs_params: LocalFSParams = None,
    **kwargs
) -> bool:
    """Function to create a new 'bucket' directory in local file system

    :param bucket_path: path to new 'bucket' directory
    :param local_fs_params: instance of LocalFSParams, defaults to None
    :return: True if successfully created, else False
    """
    logger.debug(f"Creating Bucket in Local FS: {bucket_path}")
    # get default local fs params
    if local_fs_params is None: local_fs_params = get_local_fs_params()
    # fix path
    bucket_path = fix_fs_path(bucket_path, local_fs_params)

    path = pathlib.Path(bucket_path)
    path.mkdir(exist_ok=True, parents=True)
    if os.path.exists(bucket_path) and os.path.isdir(bucket_path):
        return True
    
    return False
    

def get_fs_file_chunked(
    fpath: str, 
    local_fs_params: LocalFSParams = None,
    chunk_size: int = 1 * MB,
    bytes_io: bool = False,
    **kwargs
) -> Union[BytesIO, bytes, None]: 
    """Function to read a file from local file system in chunking loop

    :param fpath: file path
    :param local_fs_params: instance of LocalFSParams, defaults to None
    :param chunk_size: integer number of bytes per chunk to download, defaults to 1 * MB
    :return: either BytesIO object, bytes object, or None
    """
    # get default local fs params
    if local_fs_params is None: local_fs_params = get_local_fs_params()
    # fix path
    fpath = fix_fs_path(fpath, local_fs_params)

    if not os.path.exists(fpath): return
    # chunking parameters
    
    # resulting buffer to write to
    buffer = BytesIO()

    with open(fpath, 'rb') as f:
        while True:
            # read in chunk bytes
            chunk = f.read(chunk_size)
            # if returned chunk is None, don't process
            if not chunk: break
            # write  chunk to buffer
            buffer.write(chunk)
    
    # seek buffer to start
    buffer.seek(0)
    # return None if empty buffer
    if buffer.getbuffer().nbytes < 1: return None
    
    # bytesio
    if bytes_io: return buffer
    # bytes
    return buffer.getvalue()


def get_fs_file(
    fpath: str, 
    local_fs_params: LocalFSParams = None,
    bytes_io: bool = False,
    **kwargs
) -> Union[BytesIO, bytes, None]:
    """Function to read file from local file system

    :param fpath: path to file
    :param local_fs_params: instance of LocalFSParams, defaults to None
    :param bytes_io: flag to convert pulled object as BytesIO instance, defaults to False
    :return: instance of bytes or BytesIO object
    """
    logger.debug(f"Getting File from Local FS: {fpath}")
    # get default local fs params
    if local_fs_params is None: local_fs_params = get_local_fs_params()
    # fix path
    fpath = fix_fs_path(fpath, local_fs_params)

    if not os.path.exists(fpath): return
    if bytes_io is False:
        with open(fpath, 'rb') as f:
            data = f.read()
        return data
    
    with open(fpath, 'rb') as f:
        data = f.read()
        data = BytesIO(data)
        data.seek(0)
    
    return data


def get_fs_image(
    fpath: str, 
    img_format: Optional[ImageFormatType] = None,
    local_fs_params: LocalFSParams = None,
    bytes_io: bool = False,
    **kwargs
) -> Union[BytesIO, Image.Image, np.ndarray, str, bytes, None]:
    """Function to get image from local file system

    :param fpath: path to local image file
    :param img_format: oneof ImageFormatType enum, defaults to None
    :param local_fs_params: instance of LocalFSParams, defaults to None
    :param bytes_io: flag to convert pulled object as BytesIO instance, defaults to False
    :return: an instance of either BytesIO, PIL.Image.Image, np.ndarray, string, or None
    """
    # get default local fs params
    if local_fs_params is None: local_fs_params = get_local_fs_params()
    # fix path
    fpath = fix_fs_path(fpath, local_fs_params)

    ## Format functions
    def _get_base64_html_string(fpath: str) -> str:
        # Get image file
        object_data: BytesIO = get_fs_file(fpath, bytes_io=True)

        # if using base64 encoding
        extension = os.path.splitext(fpath)[1].lower()
        extension_dict = {
            ".jpg": 'data:image/jpeg;base64,',
            ".jpeg": 'data:image/jpeg;base64,',
            ".png": 'data:image/png;base64,',
            ".gif": 'data:image/gif;base64,'
        }
        if extension not in extension_dict: 
            return
        image_string = extension_dict[extension]
        image_string += base64.b64encode(object_data.read()).decode('utf-8')
        return image_string

    def _get_pil_image(fpath: str) -> Image.Image:
        # Get image file
        object_data: BytesIO = get_fs_file(fpath, bytes_io=True)
        with Image.open(object_data) as img:
            img.load()
        return img
    
    def _get_np_array_image(fpath: str) -> np.ndarray:
        # Get image file
        object_data: BytesIO = get_fs_file(fpath, bytes_io=True)
        img = np.array(_get_pil_image(object_data))
        return img

    def _get_bytesio_image(fpath: str) -> BytesIO:
        # Get image file
        object_data: BytesIO = get_fs_file(fpath, bytes_io=True)
        return object_data
    
    # functions dictionary
    format_funcs_dict = {
        ImageFormatType.BASE64_HTML_STRING: _get_base64_html_string,
        ImageFormatType.PIL_IMAGE: _get_pil_image,
        ImageFormatType.NUMPY_ARRAY: _get_np_array_image,
        "bytes_io": _get_bytesio_image
    }

    ## Hierarchy of Logic: `img_format` > `bytes_io`
    # first check for img_format args
    # then check for bytes_io arg
    # if nothing provided return raw output of s3_object.read()
    if img_format in format_funcs_dict: return format_funcs_dict[img_format](fpath)
    if bytes_io: return format_funcs_dict['bytes_io'](fpath)

    return get_fs_file(fpath, bytes_io=False)   


def get_fs_files_generator(
    fpath_list: List[str],
    local_fs_params: LocalFSParams = None, 
    bytes_io: bool = False,
    **kwargs
) -> Generator[Union[BytesIO, bytes, None], Any, None]:
    """Generator function to quickly loop through reading a list of file paths from local file system

    :param fpath_list: list of file paths
    :param local_fs_params: instance of LocalFSParams, defaults to None
    :param bytes_io: flag to convert pulled object as BytesIO instance, defaults to False
    :yield: instance of bytes or BytesIO object
    """
    # get default local fs params
    if local_fs_params is None: local_fs_params = get_local_fs_params()
    # fix paths
    fpath_list = [fix_fs_path(fpath, local_fs_params) for fpath in fpath_list]

    for fpath in fpath_list:
        yield get_fs_file(fpath, bytes_io=bytes_io)

    return


def get_fs_files_batch(
    fpath_list: List[str],
    local_fs_params: LocalFSParams = None,
    max_concurrency: int = 0, 
    bytes_io: bool = False,
    **kwargs
) -> List[Union[BytesIO, bytes, None]]:
    """Function to read a list of file paths from local file system and return a batch of data.

    :param fpath_list: list of file paths
    :param local_fs_params: instance of LocalFSParams, defaults to None
    :param max_concurrency: max no. of concurrent threads to use when downloading multiple files (0 means no concurrency), defaults to 0
    :param bytes_io: flag to convert pulled object as BytesIO instance, defaults to False
    :return: list of bytes or BytesIO object
    """
    # get default local fs params
    if local_fs_params is None: local_fs_params = get_local_fs_params()
    # fix paths
    fpath_list = [fix_fs_path(fpath, local_fs_params) for fpath in fpath_list]

    # TODO: implement multithreading

    li = []
    for count, fpath in enumerate(fpath_list):
        li.append(get_fs_file(fpath, bytes_io=bytes_io))
        print(f"Completed Downloading: {count+1}/{len(fpath_list)}")

    return li


def list_fs_folders(
    dir_path: str,
    local_fs_params: LocalFSParams = None,
    **kwargs
) -> List[str]:
    """Function to list all 1st level subdirectories in a given directory path

    :param dir_path: input directory path
    :param local_fs_params: instance of LocalFSParams, defaults to None
    :return: list of subdirectory paths
    """
    # get default local fs params
    if local_fs_params is None: local_fs_params = get_local_fs_params()
    # fix path
    dir_path = fix_fs_path(dir_path, local_fs_params)

    ret = []
    for p in os.listdir(dir_path):
        if os.path.isdir(os.path.join(dir_path, p)):
            ret.append(os.path.join(dir_path, p))
    return ret


def get_valid_fs_fpaths(
    dir_path: str,
    ignore: List[str] = [".DS_Store"],
    filter_extensions: List[str] = [],
    local_fs_params: LocalFSParams = None,
    **kwargs
) -> List[str]:
    """Funciton to get list of valid filepaths in file system (recursively) starting from
    and input directory path. This includes nested file paths.

    :param dir_path: input directory path to start from
    :param ignore: list of directories/prefixes and filepaths to ignore, defaults to ['.DS_Store']
    :param filter_extensions: list of file extensions to filter for (empty list means get everything), defaults to []
    :param local_fs_params: instance of LocalFSParams, defaults to None
    :return: list of valid file paths
    """
    # get default local fs params
    if local_fs_params is None: local_fs_params = get_local_fs_params()
    # fix path
    dir_path = fix_fs_path(dir_path, local_fs_params)

    ignore = set(ignore)

    fpaths = []
    for root, dirs, files in os.walk(dir_path, topdown=True): 
        for fname in files:
            if fname.startswith("."): continue
            fpaths.append(os.path.join(root, fname))
    
    # Process keys based on ignore_dirs and filter_extensions
    li = []
    for fpath in fpaths:
        parts = fpath.strip("/").split("/")
        fname = parts[-1]

        # check if ignored
        ignored = False
        for part in parts:
            if part in ignore:
                ignored = True
                break
        
        # check if file extension supported
        # if filter_extensions is empty list -- default to supporting all extensions
        supported_extension = False
        if len(filter_extensions) < 1:
            supported_extension = True
        else:
            for extension in filter_extensions:
                if fname.endswith(extension):
                    supported_extension = True
            
        # only append if not ignored and extension supported
        if not ignored and supported_extension: 
            li.append(fpath)
    
    fpaths, li = li, None
    return fpaths


def fpath_exists_fs(
    fpath: str,
    local_fs_params: LocalFSParams = None,
    **kwargs
) -> bool:
    """Function to check if file path exists

    :param fpath: input file path
    :param local_fs_params: instance of LocalFSParams, defaults to None
    :return: True or False if it exists
    """
    # get default local fs params
    if local_fs_params is None: local_fs_params = get_local_fs_params()
    # fix path
    fpath = fix_fs_path(fpath, local_fs_params)

    return os.path.exists(fpath)


def upload_to_fs(
    data: Union[bytes, memoryview, BytesIO], 
    save_path: str,
    local_fs_params: LocalFSParams = None,
    **kwargs
) -> str:
    """Function to write data to local file system

    :param data: input data to upload
    :param save_path: save path for newly written file
    :param local_fs_params: instance of LocalFSParams, defaults to None
    :return: saved file path
    """
    logger.debug(f"Uploading Data to File: {save_path}")
    # get default local fs params
    if local_fs_params is None: local_fs_params = get_local_fs_params()
    # fix path
    save_path = fix_fs_path(save_path, local_fs_params)

    # if data is BytesIO convert to bytes
    if isinstance(data, BytesIO): data = data.getbuffer()
    if not isinstance(data, (bytes, memoryview)):
        raise Exception(f"UploadToLocalFSError: data is not of instance 'bytes' or 'memoryview' for {save_path}.")
    
    # make directories if not already existing
    path = pathlib.Path(save_path)
    path.parent.mkdir(exist_ok=True, parents=True)
    with open(save_path, 'wb') as f:
        f.write(data)
    
    return save_path


def delete_fs_file(
    fpath: str,
    local_fs_params: LocalFSParams = None,
    **kwargs
) -> bool:
    """Function to delete file from local file system

    :param fpath: input file path to delete
    :param local_fs_params: instance of LocalFSParams, defaults to None
    :return: True if deleted, False if not deleted
    """
    # get default local fs params
    if local_fs_params is None: local_fs_params = get_local_fs_params()
    # fix path
    fpath = fix_fs_path(fpath, local_fs_params)

    if not fpath_exists_fs(fpath): return False
    # delete fpath
    os.remove(fpath)
    # if fpath still exists, it has not been deleted successfully
    if fpath_exists_fs(fpath): return False
    return True


def delete_fs_files_by_dir(
    dir_path: str,
    local_fs_params: LocalFSParams = None,
    **kwargs
) -> List[str]:
    """Function to delete all files and sub-directories in given directory path (including itself)

    :param dir_path: input directory path to delete
    :param local_fs_params: instance of LocalFSParams, defaults to None
    :return: list of deleted filepaths
    """
    # get default local fs params
    if local_fs_params is None: local_fs_params = get_local_fs_params()
    # fix path
    dir_path = fix_fs_path(dir_path, local_fs_params)

    deleted_fpaths: List[str] = get_valid_fs_fpaths(dir_path)
    if len(deleted_fpaths) < 1: return deleted_fpaths
    shutil.rmtree(dir_path)

    for i, fpath in enumerate(deleted_fpaths):
        logger.debug(f"Deleted file: {i+1}/{len(deleted_fpaths)} -- {fpath}")
    return deleted_fpaths


def extract_compressed_file_fs(
    fpath: str, 
    extracted_dir_prefix: Optional[str] = None, 
    local_fs_params: LocalFSParams = None,
    **kwargs
) -> str:
    """Function to extract zip file contents in local file system

    Compression Support: 
    - .zip
    - .gzip [TODO]
    - .tar.gz [TODO]

    :param fpath: path to compressed file to extract
    :param extracted_dir_prefix: directory to prefix the extracted archive, defaults to None
    :param local_fs_params: instance of LocalFSParams, defaults to None
    :return: path to directory where uncompressed file contents exist
    """
    # get default local fs params
    if local_fs_params is None: local_fs_params = get_local_fs_params()
    # fix path
    fpath = fix_fs_path(fpath, local_fs_params)

    def _decompress_zip_and_upload_to_fs(buffer: BytesIO, dir_path: str, zip_fpath: str = None) -> List[str]:
        """Inner function to unzip .zip file in S3 and upload unzipped files
        back to Local FS

        :param buffer: zip file buffer
        :param dir_path: path to parent directory of key .zip file
        :param zip_fpath: path to zip file, defaults to None 
        :return: list of uploaded fpaths
        """
        ret = []
        # new ZipFile instance
        try:
            with zipfile.ZipFile(buffer) as z:
                for i, filename in enumerate(z.namelist()): 
                    # ignore directories and MACOSX specific things
                    if filename.endswith("/") or "MACOSX" in filename: continue
                    logger.debug(f"Extracting File Name: {filename}")
                    # get zipfile info
                    file_info = z.getinfo(filename)
                    # create new save key
                    save_key = os.path.join(dir_path, filename) 
                    # Decompress and copy the files to the 'unzipped' folder 
                    uploaded_key = upload_to_fs(z.open(file_info).read(), save_key)

                    # if nested .zip files, recursively extract
                    if filename.endswith(".zip"):
                        # parse new dir path
                        new_dir_path = uploaded_key.split("/")[:-1]
                        new_dir_path = os.path.join(*new_dir_path)
                        if dir_path.startswith("/") and not new_dir_path.startswith("/"):
                            new_dir_path = f"/{new_dir_path}"
                        # add trailing slash if does not exist
                        if not new_dir_path.endswith("/"):
                            new_dir_path = f"{new_dir_path}/"
                        
                        logger.debug(f"Nested .zip File Found. New Dir Path: {new_dir_path}")
                        buffer = get_fs_file(uploaded_key, bytes_io=True)
                        new_path_li = _decompress_zip_and_upload_to_fs(buffer, new_dir_path, zip_fpath=uploaded_key)
                        ret.extend(new_path_li)
                    else:
                        ret.append(uploaded_key)
        except Exception as e:
            logger.error(f"ERROR! ***DecompressZipFileError*** for file: {zip_fpath}. {e}")
        
        return ret

    # read in compressed file
    buffer = get_fs_file(fpath, bytes_io=True)
    if buffer is None: 
        raise Exception(f"Error Reading File: {fpath} from file system")

    # get last directory path
    path_parts = fpath.split("/")
    dir_path = ""
    fname = path_parts[-1]
    if len(path_parts) > 1: 
        dir_path = os.path.join(*path_parts[:-1])
        if fpath.startswith("/") and not dir_path.startswith("/"):
            dir_path = f"/{dir_path}"
    
    # add extracted dir prefix if passed in
    if extracted_dir_prefix:
        dir_path = os.path.join(dir_path, extracted_dir_prefix)

    # get original file name index in split path
    original_file_index = path_parts.index(fname)
    path_offset = 1
    if extracted_dir_prefix:
        path_offset = 2

    # add trailing slash if does not exist
    if not dir_path.endswith("/"):
        dir_path = f"{dir_path}/"
    
    logger.debug(f"Dirpath: {dir_path}")

    # handle different compressions
    new_keys = []
    if fpath.endswith(".zip"):
        new_keys = _decompress_zip_and_upload_to_fs(buffer, dir_path, zip_fpath=fpath)
    elif fpath.endswith(".gzip"):
        pass
    elif fpath.endswith(".tar.gz"):
        pass

    logger.debug(f"extract_compressed_file_fs() -> New Extracted File Paths: {new_keys[:10]}, ... +{len(new_keys)-10}")

    # get archive dir
    if len(new_keys) < 1:
        logger.warning(f"WARNING: extract_compressed_file_fs() -> resulted in 0 Extracted File Paths!")
        return
    
    # get last directory path
    archive_dirpath = None
    for k in new_keys:
        # split key by path
        new_path_parts = k.split("/")
        # we need split path to have at least the original compressed file level
        if len(new_path_parts) < original_file_index+path_offset: continue
        # format the resulting archive dirpath to return
        archive_dirpath = os.path.join(*new_path_parts[:original_file_index+path_offset])
        if fpath.startswith("/") and not archive_dirpath.startswith("/"):
            archive_dirpath = f"/{archive_dirpath}"
        # make sure archive_dirpath ends with "/"
        if not archive_dirpath.endswith("/"): archive_dirpath =f"{archive_dirpath}/"
        # break if found. We only need one.
        break
    
    # return the archive dir/prefix path
    return archive_dirpath 

