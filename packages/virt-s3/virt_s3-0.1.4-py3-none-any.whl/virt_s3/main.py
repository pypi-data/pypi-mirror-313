from virt_s3.utils import get_custom_logger, ImageFormatType, archive_zip_as_buffer, KB, MB
import virt_s3.s3 as s3
import virt_s3.fs as fs

from io import BytesIO
from typing import List, Union, Any, Optional, Generator
import os

logger = get_custom_logger()


#######################################################
################## Main API Functions #################
#######################################################


class SessionManager:
    """General Session Context Manager for virt_s3 repo

    :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to None
    :param client: instance of either s3.boto3.Sesssion or None, defaults to None
    :param keep_open: boolean flag to keep the session open or not outside of the context manager scope, defaults to False
    :raises ValueError: if the params either passed in or retreived is not of type `fs.LocalFSParams` or `s3.S3Params`

    Example
    --------
    >>> params = virt_s3.get_default_params()
    >>> with virt_s3.SessionManager(params=params) as session:
    ...     virt_s3.create_bucket('default-bucket', params=params, client=session)
    ...
    """
    def __init__(
        self, 
        params: Union[s3.S3Params, fs.LocalFSParams] = None,
        client: Union[s3.Session, None] = None,
        keep_open: bool = False,
        **session_client_kwargs
    ) -> None:
        # if no params passed in get default params
        if params is None:  params = get_default_params()
        # create session client if not provided
        if client is None: client = get_session_client(params)
    
        # handle local fs function
        if isinstance(params, fs.LocalFSParams) and client is None:
            self.manager = fs.LocalFSSessionManager(
                local_fs_params=params, 
                client=client, 
                keep_open=keep_open, 
                **session_client_kwargs
            )
        elif isinstance(params, s3.S3Params) or isinstance(client, s3.Session):
            self.manager = s3.S3SessionManager(
                s3_params=params,
                s3_client=client,
                keep_open=keep_open,
                **session_client_kwargs
            )
        else:
            raise ValueError(f"Params is not of instance `fs.LocalFSParams` or `s3.S3Params`")

    def __enter__(self):
        return self.manager.__enter__()
    
    def __exit__(self, exc_type, exc_value, traceback):
        return self.manager.__exit__(exc_type, exc_value, traceback)


def get_default_params(
    use_local: bool = False, 
    use_s3: bool = False,
) -> Union[s3.S3Params, fs.LocalFSParams]:
    """Function to get default parameters to use for all functions (default behavior is based off of env variables)

    :param use_local: overrides env variables and forces to use local fs params, defaults to False
    :param use_s3: overrieds env variables and forces to use s3 params, defaults to False
    :return: either instance of s3.S3Params or fs.LocalFSParams
    """
    # check overrides
    if use_local: return fs.get_local_fs_params()
    elif use_s3: return s3.get_s3_default_params()

    # check env variables and return default beahvior
    local_fs_params = fs.get_local_fs_params()
    if local_fs_params.use_local_fs:
        if not os.path.exists(local_fs_params.root_dir):
            logger.error(f"Root Directory for Local File System Parameters Does not Exist!: {local_fs_params.root_dir}") 
        return local_fs_params
    
    return s3.get_s3_default_params()


def get_session_client(
    params: Union[s3.S3Params, fs.LocalFSParams] = None, 
    **kwargs
) -> Union[s3.Session, None]:
    """Function to get session client based on passed in s3.S3Params or fs.LocalFSParams

    :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to None
    :return: instance of either s3.boto3.Sesssion or None
    """
    # local file system does not have concept of 'session client' so return None
    if params is None: params = get_default_params()
    if isinstance(params, fs.LocalFSParams): return
    elif isinstance(params, s3.S3Params): return s3.get_s3_session_client(params, **kwargs)
    return 


def create_bucket(
    bucket_name: str,
    params: Union[s3.S3Params, fs.LocalFSParams] = None,
    client: Union[s3.Session, None] = None,
    **kwargs
) -> bool:
    """Function to create a bucket to read and write from

    :param bucket_name: name of bucket to create
    :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to None
    :param client: instance of either s3.boto3.Sesssion or None, defaults to None
    :return: True if successfully created (or already exists), else False
    """
    # if no params passed in get default params
    if params is None:  params = get_default_params()
    # create session client if not provided
    if client is None: client = get_session_client(params)

    # handle local fs function
    if isinstance(params, fs.LocalFSParams) and client is None:
        return fs.create_fs_bucket(bucket_name, local_fs_params=params)
    
    # handle s3 function
    return s3.create_s3_bucket(bucket_name, s3_params=params, s3_client=client, **kwargs)


def get_file_chunked(
    fpath: str,
    params: Union[s3.S3Params, fs.LocalFSParams] = None,
    client: Union[s3.Session, None] = None,
    **kwargs
) -> Union[BytesIO, bytes, None]:
    """Function to get a file using a chunking loop. This can be useful when trying to 
    retrieve very large files

    :param fpath: file path or key path of object to get
    :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to None
    :param client: instance of either s3.boto3.Sesssion or None, defaults to None
    :return: either instance of BytesIO object, bytes object, or None
    """
    # if no params passed in get default params
    if params is None:  params = get_default_params()
    # create session client if not provided
    if client is None: client = get_session_client(params)

    # handle local fs function
    if isinstance(params, fs.LocalFSParams) and client is None:
        return fs.get_fs_file_chunked(fpath, local_fs_params=params, **kwargs)

    # handle s3 function
    return s3.get_s3_file_chunked(fpath, s3_params=params, s3_client=client, **kwargs)


def get_file(
    fpath: str,
    params: Union[s3.S3Params, fs.LocalFSParams] = None,
    client: Union[s3.Session, None] = None,
    bytes_io: bool = False,
    **kwargs
) -> Union[BytesIO, bytes, None]:
    """Function to retrieve specified file

    :param fpath: file path or key path of object to get
    :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to None
    :param client: instance of either s3.boto3.Sesssion or None, defaults to None
    :param bytes_io: flag to convert pulled object as BytesIO instance, defaults to False
    :return: either BytesIO object, bytes object, or None
    """
    # if no params passed in get default params
    if params is None:  params = get_default_params()
    # create session client if not provided
    if client is None: client = get_session_client(params)

    # handle local fs function
    if isinstance(params, fs.LocalFSParams) and client is None:
        return fs.get_fs_file(fpath, local_fs_params=params, bytes_io=bytes_io, **kwargs)
    
    # handle s3 function
    return s3.get_s3_file(fpath, s3_params=params, s3_client=client, bytes_io=bytes_io, **kwargs)


def get_image(
    fpath: str,
    params: Union[s3.S3Params, fs.LocalFSParams] = None,
    client: Union[s3.Session, None] = None,
    img_format: Optional[ImageFormatType] = None,
    bytes_io: bool = False,
    **kwargs
) -> Union[BytesIO, s3.Image.Image, s3.np.ndarray, str, bytes, None]:
    """Function to get image from either s3 or local file system

    :param fpath: file path or key path of object to get
    :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to None
    :param client: instance of either s3.boto3.Sesssion or None, defaults to None
    :param img_format: one of ImageFormatType enum, defaults to None, defaults to None
    :param bytes_io: flag to convert pulled object as BytesIO instance, defaults to False
    :return: an instance of either io.BytesIO, PIL.Image.Image, np.ndarray, string, bytes, or None
    """
    # if no params passed in get default params
    if params is None:  params = get_default_params()
    # create session client if not provided
    if client is None: client = get_session_client(params)

    # handle local fs function
    if isinstance(params, fs.LocalFSParams) and client is None:
        return fs.get_fs_image(fpath, img_format, local_fs_params=params, bytes_io=bytes_io, **kwargs)

    # handle s3 function
    return s3.get_s3_image(fpath, s3_params=params, s3_client=client, img_format=img_format, bytes_io=bytes_io, **kwargs)


def get_files_generator(
    fpath_li: List[str],
    params: Union[s3.S3Params, fs.LocalFSParams] = None,
    client: Union[s3.Session, None] = None,
    bytes_io: bool = False,
    **kwargs  
) -> Generator[Union[BytesIO, bytes, None], Any, None]:
    """Generator function to quickly loop through reading a list of keys or file paths

    :param fpath_li: list of key or file paths to retreive as generator loop
    :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to None
    :param client: instance of either s3.boto3.Sesssion or None, defaults to None
    :param bytes_io: flag to convert pulled object as BytesIO instance, defaults to False
    :return: None
    :yield: either BytesIO object, bytes object, or None
    """
    # if no params passed in get default params
    if params is None:  params = get_default_params()
    # create session client if not provided
    if client is None: client = get_session_client(params)

    # handle local fs function
    if isinstance(params, fs.LocalFSParams) and client is None:
        return fs.get_fs_files_generator(fpath_li, local_fs_params=params, bytes_io=bytes_io, **kwargs)
    
    # handle s3 function
    return s3.get_s3_files_generator(fpath_li, s3_params=params, s3_client=client, bytes_io=bytes_io, **kwargs)


def get_files_batch(
    fpath_li: List[str],
    params: Union[s3.S3Params, fs.LocalFSParams] = None,
    client: Union[s3.Session, None] = None,
    max_concurrency: int = 0, 
    bytes_io: bool = False,
    **kwargs  
) -> List[Union[BytesIO, bytes, None]]:
    """Function to get list of file paths or key paths in batch

    :param fpath_li: list of key or file paths to retreive as generator loop
    :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to None
    :param client: instance of either s3.boto3.Sesssion or None, defaults to None
    :param max_concurrency: max no. of concurrent threads to use when downloading a file (0 means no concurrency), defaults to 0
    :param bytes_io: flag to convert pulled object as BytesIO instance, defaults to False
    :return: list of either BytesIO object, bytes object, or None
    """
    # if no params passed in get default params
    if params is None:  params = get_default_params()
    # create session client if not provided
    if client is None: client = get_session_client(params)

    # handle local fs function
    if isinstance(params, fs.LocalFSParams) and client is None:
        return fs.get_fs_files_batch(fpath_li, local_fs_params=params, max_concurrency=max_concurrency, bytes_io=bytes_io, **kwargs)
    
    # handle s3 function
    return s3.get_s3_files_batch(fpath_li, s3_params=params, s3_client=client, max_concurrency=max_concurrency, bytes_io=bytes_io, **kwargs)


def list_dirs(
    dir_path: str,
    params: Union[s3.S3Params, fs.LocalFSParams] = None,
    client: Union[s3.Session, None] = None,
    delimiter: str ='/',
    **kwargs
) -> List[str]:
    """Function to list valid folders within 'bucket'

    :param dir_path: directory or prefix path
    :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to None
    :param client: instance of either s3.boto3.Sesssion or None, defaults to None
    :param delimiter: delimiter used to filter objects in S3 (e.g. only subfolders - delimiter="/"), defaults to '/'
    :return: list of folder paths
    """
    # if no params passed in get default params
    if params is None:  params = get_default_params()
    # create session client if not provided
    if client is None: client = get_session_client(params)

    # handle local fs function
    if isinstance(params, fs.LocalFSParams) and client is None:
        return fs.list_fs_folders(dir_path, local_fs_params=params, **kwargs)
    
    # handle s3 functions
    return s3.list_s3_folders(dir_path, s3_params=params, s3_client=client, delimiter=delimiter, **kwargs)


def get_valid_file_paths(
    dir_path: str,
    ignore: List[str] = [".DS_Store"],
    filter_extensions: List[str] = [],
    params: Union[s3.S3Params, fs.LocalFSParams] = None,
    client: Union[s3.Session, None] = None,
    **kwargs
) -> List[str]:
    """Function to get list of valid file paths or keys within particular directory of bucket

    :param dir_path: directory or prefix path to search
    :param ignore: list of directories/prefixes and filepaths to ignore, defaults to ['.DS_Store']
    :param filter_extensions: list of file extensions to filter for (empty list means get everything), defaults to []
    :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to None
    :param client: instance of either s3.boto3.Sesssion or None, defaults to None
    :return: list of valid file paths or key paths
    """
    # if no params passed in get default params
    if params is None:  params = get_default_params()
    # create session client if not provided
    if client is None: client = get_session_client(params)

    # handle local fs function
    if isinstance(params, fs.LocalFSParams) and client is None:
        return fs.get_valid_fs_fpaths(
            dir_path, 
            local_fs_params=params, 
            ignore=ignore, 
            filter_extensions=filter_extensions,
            **kwargs
        )

    # handle s3 function
    return s3.get_valid_s3_keys(
        dir_path, 
        ignore=ignore, 
        filter_extensions=filter_extensions, 
        s3_params=params, 
        s3_client=client,
        **kwargs
    )


def file_exists(
    fpath: str,
    params: Union[s3.S3Params, fs.LocalFSParams] = None,
    client: Union[s3.Session, None] = None,
    **kwargs
) -> bool:
    """Function to see if key or file path exists in bucket

    :param fpath: file path or key path to check
    :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to None
    :param client: instance of either s3.boto3.Sesssion or None, defaults to None
    :return: True if key or file path exists, False otherwise
    """
    # if no params passed in get default params
    if params is None:  params = get_default_params()
    # create session client if not provided
    if client is None: client = get_session_client(params)

    # handle local fs function
    if isinstance(params, fs.LocalFSParams) and client is None:
        return fs.fpath_exists_fs(fpath, local_fs_params=params, **kwargs)

    # handle s3 function
    return s3.key_exists_s3(fpath, s3_params=params, s3_client=client, **kwargs)


def upload_data(
    data: Union[bytes, memoryview, BytesIO],
    fpath: str,
    params: Union[s3.S3Params, fs.LocalFSParams] = None,
    client: Union[s3.Session, None] = None,
    **kwargs
) -> str:
    """Function to upload data to S3 or local file system

    :param data: data to save as bytes, memoryview, or BytesIO
    :param fpath: path to save data to
    :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to None
    :param client: instance of either s3.boto3.Sesssion or None, defaults to None
    :raises Exception: either General exception if not HTTP Status Code 200 or Exception if input data is not of instance 'bytes' or 'BytesIO'
    :return: saved key or file path
    """
    # if no params passed in get default params
    if params is None:  params = get_default_params()
    # create session client if not provided
    if client is None: client = get_session_client(params)

    # handle local fs function
    if isinstance(params, fs.LocalFSParams) and client is None:
        return fs.upload_to_fs(data, fpath, local_fs_params=params, **kwargs)
    
    # handle s3 function
    return s3.upload_to_s3(data, fpath, s3_params=params, s3_client=client, **kwargs)


def delete_file(
    fpath: str,
    params: Union[s3.S3Params, fs.LocalFSParams] = None,
    client: Union[s3.Session, None] = None,
    **kwargs
) -> bool:
    """Function to delete a file from s3 or local file system

    :param fpath: file path to delete
    :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to None
    :param client: instance of either s3.boto3.Sesssion or None, defaults to None
    :return: True if delete successful, else return False
    """
    # if no params passed in get default params
    if params is None:  params = get_default_params()
    # create session client if not provided
    if client is None: client = get_session_client(params)

    # handle local fs function
    if isinstance(params, fs.LocalFSParams) and client is None:
        return fs.delete_fs_file(fpath, local_fs_params=params, **kwargs)
    
    # handle s3 function
    return s3.delete_s3_object(fpath, s3_params=params, s3_client=client, **kwargs)


def delete_files_by_dir(
    dir_path: str,
    params: Union[s3.S3Params, fs.LocalFSParams] = None,
    client: Union[s3.Session, None] = None,
    **kwargs
) -> List[str]:
    """Function to delete all files and subdirectories, etc. in a given folder

    :param dir_path: path to folder or prefix to delete
    :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to None
    :param client: instance of either s3.boto3.Sesssion or None, defaults to None
    :return: list of deleted file or key paths
    """
    # if no params passed in get default params
    if params is None:  params = get_default_params()
    # create session client if not provided
    if client is None: client = get_session_client(params)

    # handle local fs function
    if isinstance(params, fs.LocalFSParams) and client is None:
        return fs.delete_fs_files_by_dir(dir_path, local_fs_params=params, **kwargs)
    
    # handle s3 function
    return s3.delete_s3_objects_by_prefix(dir_path, s3_params=params, s3_client=client, **kwargs)


def extract_compressed_file(
    fpath: str,
    extracted_dir_prefix: Optional[str] = None, 
    params: Union[s3.S3Params, fs.LocalFSParams] = None,
    client: Union[s3.Session, None] = None,
    **kwargs
) -> str:
    """Function to extract zip file contents

    Compression Support:
    - .zip
    - .gzip [TODO]
    - .tar.gz [TODO]

    :param fpath: path to compressed file or key to extract
    :param extracted_dir_prefix: directory to prefix the extracted archive, defaults to None
    :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to None
    :param client: instance of either s3.boto3.Sesssion or None, defaults to None
    :return: path to directory or prefix path where uncompressed file contents exist
    """
    # if no params passed in get default params
    if params is None:  params = get_default_params()
    # create session client if not provided
    if client is None: client = get_session_client(params)

    # handle local fs function
    if isinstance(params, fs.LocalFSParams) and client is None:
        return fs.extract_compressed_file_fs(
            fpath, 
            extracted_dir_prefix=extracted_dir_prefix, 
            local_fs_params=params,
            **kwargs
        )
    
    # handle s3 function
    return s3.extract_compressed_file_s3(
        fpath, 
        extracted_dir_prefix=extracted_dir_prefix,
        s3_params=params,
        s3_client=client,
        **kwargs
    )

