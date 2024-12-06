from virt_s3.utils import get_custom_logger
from virt_s3.main import get_default_params, get_valid_file_paths, get_file, get_session_client, upload_data, SessionManager
import virt_s3.s3 as s3
import virt_s3.fs as fs

from io import BytesIO
from abc import ABC, abstractmethod
from typing import List, Union, Any, Callable
import json

logger = get_custom_logger()

try: 
    import pandas as pd
except ModuleNotFoundError as me: 
    logger.warning(f"{me} -> `$ poetry install -E dataframe` to use.")
    class pd:
        class DataFrame: 
            pass
try: 
    import pyarrow.parquet as pq
except ModuleNotFoundError as me: 
    logger.warning(f"{me} -> `$ poetry install -E dataframe` to use.")

#######################################################################
################ Extra Functions, Classes, Interfaces #################
#######################################################################


def read_parquet_file_df(
    fpath: str,
    params: Union[s3.S3Params, fs.LocalFSParams] = None,
    client: Union[s3.Session, None] = None,
    engine: str = "auto",
    columns: List[str] = None,
    filters: List[tuple] = None,
    use_nullable_dtypes: bool = False,
    **download_kwargs
) -> pd.DataFrame:
    """Convenience function to read parquet file as pandas DataFrame.
    Attempts to first read full buffer at once, then falls back to reading in batches if error
    in reading full buffer at once.

    :param fpath: path to parquet file or key
    :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to None
    :param client: instance of either s3.boto3.Sesssion or None, defaults to None
    :param engine: {{'auto', 'pyarrow', 'fastparquet'}}, defaults to 'auto'
        - Parquet library to use. If 'auto', then the option
        ``io.parquet.engine`` is used. The default ``io.parquet.engine``
        behavior is to try 'pyarrow', falling back to 'fastparquet' if
        'pyarrow' is unavailable. When using the ``'pyarrow'`` engine and no storage options are provided
        and a filesystem is implemented by both ``pyarrow.fs`` and ``fsspec`` (e.g. "s3://"), 
        then the ``pyarrow.fs`` filesystem is attempted first. Use the filesystem keyword with an
        instantiated fsspec filesystem if you wish to use its implementation.

    :param columns: If not None, only these columns will be read from the file, defaults to None
    :param filters: To filter out data, defaults to None
        - Filter syntax: [[(column, op, val), ...],...]
        where op is [==, =, >, >=, <, <=, !=, in, not in]
        The innermost tuples are transposed into a set of filters applied
        through an `AND` operation. The outer list combines these sets of filters through an `OR`
        operation. A single list of tuples can also be used, meaning that no `OR`
        operation between set of filters is to be conducted. Using this argument will NOT result in 
        row-wise filtering of the final partitions unless ``engine="pyarrow"`` is also specified.  For other engines, filtering 
        is only performed at the partition level, that is, to prevent the loading of some row-groups and/or files.

    :param use_nullable_dtypes: boolean flag, defaults to False
        - If True, use dtypes that use ``pd.NA`` as missing value indicator for the resulting DataFrame. 
        (only applicable for the ``pyarrow`` engine). As new dtypes are added that support ``pd.NA`` in the future, the
        output with this option will change to use those dtypes.
        Note: this is an experimental option, and behaviour (e.g. additional
        support dtypes) may change without notice.
    
    :return: pd.DataFrame
    """
    # if no params passed in get default params
    if params is None:  params = get_default_params()
    # create session client if not provided
    if client is None: client = get_session_client(params)
    # get file as dataframe
    buffer = get_file(fpath, params=params, client=client, bytes_io=True, **download_kwargs)
    try:
        return pd.read_parquet(
            buffer,
            engine=engine,
            columns=columns,
            filters=filters,
            use_nullable_dtypes=use_nullable_dtypes
        )
    except Exception as e:
        logger.debug(f"Failed to read full parquet file from buffer. Falling back to reading in batches. {e}")
        parquet_file = pq.ParquetFile(buffer)
        dfs = [batch.to_pandas() for batch in parquet_file.iter_batches()]
        return pd.concat(dfs, ignore_index=True, copy=False)   


def write_parquet_file_df(
    df: pd.DataFrame,
    save_fpath: str,
    params: Union[s3.S3Params, fs.LocalFSParams] = None,
    client: Union[s3.Session, None] = None,
    engine: str = "auto",
    compression: str = None,
    index: bool = None,
    partition_cols: List[str] = None,
    **upload_kwargs
) -> str:
    """Convenience function to write pandas DataFrame to parquet file.

    :param df: pandas DataFrame to save
    :param save_fpath: parquet file save path or key (e.g. data.parquet.sz)
    :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to None
    :param client: instance of either s3.boto3.Sesssion or None, defaults to None
    :param engine: {{'auto', 'pyarrow', 'fastparquet'}}, defaults to 'auto'
        - Parquet library to use. If 'auto', then the option
        ``io.parquet.engine`` is used. The default ``io.parquet.engine``
        behavior is to try 'pyarrow', falling back to 'fastparquet' if
        'pyarrow' is unavailable. When using the ``'pyarrow'`` engine and no storage options are provided
        and a filesystem is implemented by both ``pyarrow.fs`` and ``fsspec`` (e.g. "s3://"), 
        then the ``pyarrow.fs`` filesystem is attempted first. Use the filesystem keyword with an
        instantiated fsspec filesystem if you wish to use its implementation.

    :param compression: compression algorithm to use, default 'snappy'
        - Name of the compression to use. Use None for no compression. 
        - Supported options: 'snappy', 'gzip', 'brotli', 'lz4', 'zstd'.

    :param index: _description_, defaults to None
        - If True, include the dataframe's index(es) in the file output. 
        - If False, they will not be written to the file. 
        - If None, similar to True the dataframe's index(es) will be saved. 
        However, instead of being saved as values, the RangeIndex will be stored as 
        a range in the metadata so it doesn't require much space and is faster. 
        Other indexes will be included as columns in the file output.
    
    :param partition_cols: column names by which to partition the dataset, defaults to None
        - Columns are partitioned in the order they are given
        - Must be None if path is not a string

    :return: saved key or file path
    """
    # if no params passed in get default params
    if params is None:  params = get_default_params()
    # create session client if not provided
    if client is None: client = get_session_client(params)
    # write to buffer
    buffer = BytesIO()
    df.to_parquet(buffer, engine=engine, compression=compression, partition_cols=partition_cols, index=index)
    buffer.seek(0)
    # upload
    return upload_data(buffer.getvalue(), save_fpath, params=params, client=client, **upload_kwargs)


class FileValidator(ABC):
    """Base Abstract Interface for File Type Validators
   
    :param file_extensions: supported file extensions by this Validator, defaults to [".json", ".csv", ".parquet.sz"]
    :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to get_default_params
    """
    def __init__(
        self, 
        file_extensions: List[str] = [".json", ".csv", ".parquet.sz"],
        params: Union[s3.S3Params, fs.LocalFSParams] = get_default_params,
    ) -> None:
        
        if isinstance(params, Callable):
            params = params()
        self.file_extensions = file_extensions
        self.params = params

        self.fpaths: List[str] = []
        self.bad_fpaths: List[str] = []
    
    @abstractmethod
    def validate_file(
        self, 
        fpath: str, 
        *args, 
        params: Union[s3.S3Params, fs.LocalFSParams] = None, 
        client: Union[s3.Session, None] = None,
        **kwargs
    ) -> bool:
        """Method to implement based on specific child validator

        :param fpath: path to file or key
        :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to get_default_params()
        :param client: instance of either s3.boto3.Sesssion or None, defaults to None
        :return: True if valid file, False if invalid file
        """
        pass
    
    def run(
        self, 
        fpath_li: List[str] = [],
        root_path: str = None, 
        ignore: List[str] = [],
    ) -> dict:
        """Method to run File Validator

        :param fpath_li: list of files paths to run validation on, defaults to []
        :param root_path: root dir path or prefix to start looking for files within to validated, defaults to None
        :param ignore: list of dirs/prefixes/files to ignore, defaults to []
        :return: dictionary of { 'valid': List[file paths], 'invalid': List[file paths] }
        """
        ## Check for valid arguments passed in 
        if root_path is None and (fpath_li is None or (isinstance(fpath_li, list) and len(fpath_li) < 1)):
            raise Exception(f"Invalid arguments passed in to FileValidator.run(). Either `fpath_li` or `root_path` must be passed in and non-null.")

        # initialize valid and invalid file paths
        self.fpaths, self.bad_fpaths = [], []

        ## File Path retrieval
        # if fpath list passed in, use that to read and validate files
        fpaths = fpath_li
        if len(fpaths) < 1: 
            with SessionManager(params=self.params) as client:
                # else, get current list of file paths
                fpaths = get_valid_file_paths(
                    root_path, 
                    ignore=ignore,
                    params=self.params, 
                    client=client,
                    filter_extensions=self.file_extensions
                )
                logger.info(f"Retrieved {len(fpaths)} Files with one of the following extensions: {self.file_extensions}")

        ## Filtering Extensions
        logger.debug(f"Checking to make sure all files include extensions: {self.file_extensions} ...")
        remove = []
        for fpath in fpath_li:
            correct_extension = False
            for extension in self.file_extensions:
                if fpath.endswith(extension):
                    correct_extension = True
            if not correct_extension:
                # logger.debug(f"Removing file from list due to non-inclusion of extensions {self.file_extensions}: {fpath}")
                remove.append(fpath)
        fpaths = [f for f in fpaths if f not in remove]
        logger.debug(f"Correct Files to Validate: {fpaths[:10]}, ... +{len(fpaths)-10}")

        ## Data Validation
        logger.info(f'Running Data Validation for {self.file_extensions} files ...')
        with SessionManager(params=self.params) as client:
            for i, fpath in enumerate(fpaths):
                is_valid = self.validate_file(fpath, params=self.params, client=client)
                if not is_valid:
                    self.bad_fpaths.append(fpath)
                    continue
                self.fpaths.append(fpath)

            logger.debug(f"Valid Files: {len(self.fpaths)}")
            logger.debug(f"Invalid Files: {len(self.bad_fpaths)}")

        return {'valid': self.fpaths, 'invalid': self.bad_fpaths}


class JSONFileValidator(FileValidator):
    """Interface for JSON FIle Validation
   
    :param file_extensions: supported file extensions by this Validator, defaults to [".json", ".csv", ".parquet.sz"]
    :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to get_default_params
    """
    def __init__(
        self, 
        file_extensions: List[str] = [".json"],
        params: Union[s3.S3Params, fs.LocalFSParams] = get_default_params,
    ) -> None:
        
        super().__init__(file_extensions=file_extensions, params=params)
    
    def validate_file(self, fpath: str, client: Union[s3.Session, None] = None) -> bool:
        """Implemented method to validate JSON files

        :param fpath: path to file or key
        :param client: instance of either s3.boto3.Sesssion or None, defaults to None
        :return: True if valid file, False if invalid file
        """
        try:
            obj = get_file(fpath, bytes_io=False, params=self.params, client=client)
            data = json.loads(obj.decode('utf-8'))
            assert len(list(data.keys())) > 0
            return True
        except Exception as e:
            logger.debug(f"JSONFileValidatorException: {e}")
            return False


class CSVFileValidator(FileValidator):
    """Interface for CSV File Validation
   
    :param file_extensions: supported file extensions by this Validator, defaults to [".json", ".csv", ".parquet.sz"]
    :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to get_default_params
    """
    def __init__(
        self, 
        file_extensions: List[str] = [".csv"],
        params: Union[s3.S3Params, fs.LocalFSParams] = get_default_params,
    ) -> None:
        
        try: import pandas as pd
        except: logger.warning(f"'pandas' not installed.  Run `$ poetry install -E dataframe` to use CSVFileValidator, ParquetFileValidator.")
        
        super().__init__(file_extensions=file_extensions, params=params)
    
    def validate_file(self, fpath: str, client: Union[s3.Session, None] = None) -> bool:
        """Implemented method to validate CSV files

        :param fpath: path to file or key
        :param client: instance of either s3.boto3.Sesssion or None, defaults to None
        :return: True if valid file, False if invalid file
        """
        try:
            obj = get_file(fpath, bytes_io=True, params=self.params, client=client)
            df = pd.read_csv(obj)
            assert isinstance(df, pd.DataFrame)
            return True
        except Exception as e:
            logger.debug(f"CSFileVValidatorException: {e}")
            return False
        

class ParquetFileValidator(FileValidator):
    """Interface for Parquet File Validation
   
    :param file_extensions: supported file extensions by this Validator, defaults to [".json", ".csv", ".parquet.sz"]
    :param params: either instance of s3.S3Params or fs.LocalFSParams, defaults to get_default_params
    """
    def __init__(
        self, 
        file_extensions: List[str] = [".parquet.sz", ".parquet"],
        params: Union[s3.S3Params, fs.LocalFSParams] = get_default_params,
    ) -> None:
        try: import pandas as pd
        except: logger.warning(f"'pandas' not installed.  Run `$ poetry install -E dataframe` to use CSVFileValidator, ParquetFileValidator.")
        try: import pyarrow.parquet as pq
        except: logger.warning(f"'pyarrow' not installed. Run `$ poetry install -E dataframe` to use ParquetFileValidator.")
            
        super().__init__(file_extensions=file_extensions, params=params)

    def validate_file(self, fpath: str, client: Union[s3.Session, None] = None) -> bool:
        """Implemented method to validate Parquet files

        :param fpath: path to file or key
        :param client: instance of either s3.boto3.Sesssion or None, defaults to None
        :return: True if valid file, False if invalid file
        """
        try:
            df = read_parquet_file_df(fpath, params=self.params, client=client)
            assert isinstance(df, pd.DataFrame)
            return True
        except Exception as e:
            logger.debug(f"ParquetFileValidatorException: {e}")
            return False