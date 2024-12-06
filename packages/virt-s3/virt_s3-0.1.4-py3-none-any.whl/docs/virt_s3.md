# virt_s3 package

## Module contents

### virt_s3.get_custom_logger(name='VirtS3', log_level=10)

Function to return a custom formatted logger object

* **Parameters:**
  * **name** (`str`) – name of logger, defaults to ‘VirtS3’
  * **log_level** (`int`) – desired logging level, defaults to logging.DEBUG
* **Return type:**
  `Logger`
* **Returns:**
  custom formatted Logger streaming to stdout

### *class* virt_s3.PredictConnectionStoreParams(user_id, store_name, store_owner)

Bases: `object`

Dataclass for Predict Connection Store Parameters

* **Parameters:**
  * **user_id** (`str`) – predict user id
  * **store_name** (`str`) – connection store name
  * **store_owner** (`str`) – connection store owner

### *class* virt_s3.S3Params(bucket_name, endpoint_url, aws_access_key_id=None, aws_secret_access_key=None, region_name=None, profile_name=None, connection_store_params=None)

Bases: `object`

Dataclass for S3 Boto3 Connection Parameters

Required:
- bucket_name
- endpoint_url

Optional:
- region_name

Authentication Methods (and necessary params):

1. Explicit Credentials
  - aws_access_key_id
  - aws_secret_access_key
2. AWS Profile
  - profile_name
3. Predict Backend Connection Store
  - connection_store_params

* **Parameters:**
  * **bucket_name** (`str`) – aws s3 bucket
  * **endpoint_url** (`str`) – aws s3 url
  * **aws_access_key_id** (`str`) – your aws access key id, defaults to None
  * **aws_secret_access_key** (`str`) – your aws secret access key, defaults to None
  * **region_name** (`str`) – your aws region name, defaults to None
  * **profile_name** (`str`) – your aws IAM profile name, defaults to None
  * **connection_store_params** ([`PredictConnectionStoreParams`](#virt_s3.s3.PredictConnectionStoreParams)) – instance of PredictConnectionStoreParams, defaults to None

### *class* virt_s3.SessionManager(params=None, client=None, keep_open=False, \*\*session_client_kwargs)

Bases: `object`

General Session Context Manager for virt_s3 repo

* **Parameters:**
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to None
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
  * **keep_open** (`bool`) – boolean flag to keep the session open or not outside of the context manager scope, defaults to False
* **Raises:**
  **ValueError** – if the params either passed in or retreived is not of type fs.LocalFSParams or s3.S3Params

### Example

```pycon
>>> params = virt_s3.get_default_params()
>>> with virt_s3.SessionManager(params=params) as session:
...     virt_s3.create_bucket('default-bucket', params=params, client=session)
...
```

### *class* virt_s3.TransferConfig(multipart_threshold=8388608, max_concurrency=10, multipart_chunksize=8388608, num_download_attempts=5, max_io_queue=100, io_chunksize=262144, use_threads=True, max_bandwidth=None, preferred_transfer_client='auto')

Bases: `TransferConfig`

### *class* virt_s3.LocalFSParams(use_local_fs, root_dir, user, bucket_name)

Bases: `object`

Dataclass for Using Local File System for all S3 Calls

* **Parameters:**
  * **use_local_fs** (`bool`) – flag to use the local file system or not for S3 calls
  * **root_dir** (`str`) – local file system root dir that represents your ‘bucket’
  * **user** (`str`) – your username
  * **bucket_name** (`str`) – emulated S3 ‘bucket’ directory in file system within root dir

### *class* virt_s3.ImageFormatType(value, names=None, \*, module=None, qualname=None, type=None, start=1, boundary=None)

Bases: `Enum`

Enum class type for Image Format Types

Enum Options:
- PIL_IMAGE = “pil_img”
- BASE64_HTML_STRING = “base64_html_string”
- NUMPY_ARRAY = “numpy_array”

### virt_s3.get_default_params(use_local=False, use_s3=False)

Function to get default parameters to use for all functions (default behavior is based off of env variables)

* **Parameters:**
  * **use_local** (`bool`) – overrides env variables and forces to use local fs params, defaults to False
  * **use_s3** (`bool`) – overrieds env variables and forces to use s3 params, defaults to False
* **Return type:**
  `Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]
* **Returns:**
  either instance of s3.S3Params or fs.LocalFSParams

### virt_s3.get_session_client(params=None, \*\*kwargs)

Function to get session client based on passed in s3.S3Params or fs.LocalFSParams

* **Parameters:**
  **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to None
* **Return type:**
  `Optional`[`Session`]
* **Returns:**
  instance of either s3.boto3.Sesssion or None

### virt_s3.create_bucket(bucket_name, params=None, client=None)

Function to create a bucket to read and write from

* **Parameters:**
  * **bucket_name** (`str`) – name of bucket to create
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to None
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
* **Return type:**
  `bool`
* **Returns:**
  True if successfully created (or already exists), else False

### virt_s3.get_file_chunked(fpath, params=None, client=None, \*\*kwargs)

Function to get a file using a chunking loop. This can be useful when trying to
retrieve very large files

* **Parameters:**
  * **fpath** (`str`) – file path or key path of object to get
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to None
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
* **Return type:**
  `Union`[`BytesIO`, `bytes`, `None`]
* **Returns:**
  either instance of BytesIO object, bytes object, or None

### virt_s3.get_file(fpath, params=None, client=None, bytes_io=False, \*\*kwargs)

Function to retrieve specified file

* **Parameters:**
  * **fpath** (`str`) – file path or key path of object to get
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to None
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
  * **bytes_io** (`bool`) – flag to convert pulled object as BytesIO instance, defaults to False
* **Return type:**
  `Union`[`BytesIO`, `bytes`, `None`]
* **Returns:**
  either BytesIO object, bytes object, or None

### virt_s3.get_image(fpath, params=None, client=None, img_format=None, bytes_io=False, \*\*kwargs)

Function to get image from either s3 or local file system

* **Parameters:**
  * **fpath** (`str`) – file path or key path of object to get
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to None
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
  * **img_format** (`Optional`[[`ImageFormatType`](#virt_s3.utils.ImageFormatType)]) – one of ImageFormatType enum, defaults to None, defaults to None
  * **bytes_io** (`bool`) – flag to convert pulled object as BytesIO instance, defaults to False
* **Return type:**
  `Union`[`BytesIO`, `Image`, `ndarray`, `str`, `bytes`, `None`]
* **Returns:**
  an instance of either io.BytesIO, PIL.Image.Image, np.ndarray, string, bytes, or None

### virt_s3.get_files_generator(fpath_li, params=None, client=None, bytes_io=False, \*\*kwargs)

Generator function to quickly loop through reading a list of keys or file paths

* **Parameters:**
  * **fpath_li** (`List`[`str`]) – list of key or file paths to retreive as generator loop
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to None
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
  * **bytes_io** (`bool`) – flag to convert pulled object as BytesIO instance, defaults to False
* **Return type:**
  `Generator`[`Union`[`BytesIO`, `bytes`, `None`], `Any`, `None`]
* **Returns:**
  None
* **Yield:**
  either BytesIO object, bytes object, or None

### virt_s3.get_files_batch(fpath_li, params=None, client=None, max_concurrency=0, bytes_io=False, \*\*kwargs)

Function to get list of file paths or key paths in batch

* **Parameters:**
  * **fpath_li** (`List`[`str`]) – list of key or file paths to retreive as generator loop
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to None
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
  * **max_concurrency** (`int`) – max no. of concurrent threads to use when downloading a file (0 means no concurrency), defaults to 0
  * **bytes_io** (`bool`) – flag to convert pulled object as BytesIO instance, defaults to False
* **Return type:**
  `List`[`Union`[`BytesIO`, `bytes`, `None`]]
* **Returns:**
  list of either BytesIO object, bytes object, or None

### virt_s3.list_dirs(dir_path, params=None, client=None, delimiter='/', \*\*kwargs)

Function to list valid folders within ‘bucket’

* **Parameters:**
  * **dir_path** (`str`) – directory or prefix path
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to None
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
  * **delimiter** (`str`) – delimiter used to filter objects in S3 (e.g. only subfolders - delimiter=”/”), defaults to ‘/’
* **Return type:**
  `List`[`str`]
* **Returns:**
  list of folder paths

### virt_s3.get_valid_file_paths(dir_path, ignore=['.DS_Store'], filter_extensions=[], params=None, client=None, \*\*kwargs)

Function to get list of valid file paths or keys within particular directory of bucket

* **Parameters:**
  * **dir_path** (`str`) – directory or prefix path to search
  * **ignore** (`List`[`str`]) – list of directories/prefixes and filepaths to ignore, defaults to [‘.DS_Store’]
  * **filter_extensions** (`List`[`str`]) – list of file extensions to filter for (empty list means get everything), defaults to []
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to None
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
* **Return type:**
  `List`[`str`]
* **Returns:**
  list of valid file paths or key paths

### virt_s3.file_exists(fpath, params=None, client=None, \*\*kwargs)

Function to see if key or file path exists in bucket

* **Parameters:**
  * **fpath** (`str`) – file path or key path to check
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to None
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
* **Return type:**
  `bool`
* **Returns:**
  True if key or file path exists, False otherwise

### virt_s3.upload_data(data, fpath, params=None, client=None, \*\*kwargs)

Function to upload data to S3 or local file system

* **Parameters:**
  * **data** (`Union`[`bytes`, `memoryview`, `BytesIO`]) – data to save as bytes, memoryview, or BytesIO
  * **fpath** (`str`) – path to save data to
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to None
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
* **Raises:**
  **Exception** – either General exception if not HTTP Status Code 200 or Exception if input data is not of instance ‘bytes’ or ‘BytesIO’
* **Return type:**
  `str`
* **Returns:**
  saved key or file path

### virt_s3.delete_file(fpath, params=None, client=None, \*\*kwargs)

Function to delete a file from s3 or local file system

* **Parameters:**
  * **fpath** (`str`) – file path to delete
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to None
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
* **Return type:**
  `bool`
* **Returns:**
  True if delete successful, else return False

### virt_s3.delete_files_by_dir(dir_path, params=None, client=None, \*\*kwargs)

Function to delete all files and subdirectories, etc. in a given folder

* **Parameters:**
  * **dir_path** (`str`) – path to folder or prefix to delete
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to None
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
* **Return type:**
  `List`[`str`]
* **Returns:**
  list of deleted file or key paths

### virt_s3.archive_zip_as_buffer(data_bytes_dict)

Function to create a zip archive from dictionary of expected archive filepaths
and data bytes

* **Parameters:**
  **data_bytes_dict** (`Dict`[`str`, `bytes`]) – { “/path/to/data/file/in/archive/file.extension”: data_as_bytes_obj }
* **Return type:**
  `BytesIO`
* **Returns:**
  zipped buffer BytesIO object

### virt_s3.extract_compressed_file(fpath, extracted_dir_prefix=None, params=None, client=None, \*\*kwargs)

Function to extract zip file contents

Compression Support:
- .zip
- .gzip [TODO]
- .tar.gz [TODO]

* **Parameters:**
  * **fpath** (`str`) – path to compressed file or key to extract
  * **extracted_dir_prefix** (`Optional`[`str`]) – directory to prefix the extracted archive, defaults to None
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to None
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
* **Return type:**
  `str`
* **Returns:**
  path to directory or prefix path where uncompressed file contents exist

### virt_s3.read_parquet_file_df(fpath, params=None, client=None, engine='auto', columns=None, filters=None, use_nullable_dtypes=False, \*\*download_kwargs)

Convenience function to read parquet file as pandas DataFrame.
Attempts to first read full buffer at once, then falls back to reading in batches if error
in reading full buffer at once.

* **Parameters:**
  * **fpath** (`str`) – path to parquet file or key
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to None
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
  * **engine** (`str`) – {{‘auto’, ‘pyarrow’, ‘fastparquet’}}, defaults to ‘auto’
    - Parquet library to use. If ‘auto’, then the option
    `io.parquet.engine` is used. The default `io.parquet.engine`
    behavior is to try ‘pyarrow’, falling back to ‘fastparquet’ if
    ‘pyarrow’ is unavailable. When using the `'pyarrow'` engine and no storage options are provided
    and a filesystem is implemented by both `pyarrow.fs` and `fsspec` (e.g. “s3://”),
    then the `pyarrow.fs` filesystem is attempted first. Use the filesystem keyword with an
    instantiated fsspec filesystem if you wish to use its implementation.
  * **columns** (`List`[`str`]) – If not None, only these columns will be read from the file, defaults to None
  * **filters** (`List`[`tuple`]) – To filter out data, defaults to None
    - Filter syntax: [[(column, op, val), …],…]
    where op is [==, =, >, >=, <, <=, !=, in, not in]
    The innermost tuples are transposed into a set of filters applied
    through an AND operation. The outer list combines these sets of filters through an OR
    operation. A single list of tuples can also be used, meaning that no OR
    operation between set of filters is to be conducted. Using this argument will NOT result in
    row-wise filtering of the final partitions unless `engine="pyarrow"` is also specified.  For other engines, filtering
    is only performed at the partition level, that is, to prevent the loading of some row-groups and/or files.
  * **use_nullable_dtypes** (`bool`) – boolean flag, defaults to False
    - If True, use dtypes that use `pd.NA` as missing value indicator for the resulting DataFrame.
    (only applicable for the `pyarrow` engine). As new dtypes are added that support `pd.NA` in the future, the
    output with this option will change to use those dtypes.
    Note: this is an experimental option, and behaviour (e.g. additional
    support dtypes) may change without notice.
* **Returns:**
  pd.DataFrame

### virt_s3.write_parquet_file_df(df, save_fpath, params=None, client=None, engine='auto', compression=None, index=None, partition_cols=None, \*\*upload_kwargs)

Convenience function to write pandas DataFrame to parquet file.

* **Parameters:**
  * **df** (`DataFrame`) – pandas DataFrame to save
  * **save_fpath** (`str`) – parquet file save path or key (e.g. data.parquet.sz)
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to None
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
  * **engine** (`str`) – {{‘auto’, ‘pyarrow’, ‘fastparquet’}}, defaults to ‘auto’
    - Parquet library to use. If ‘auto’, then the option
    `io.parquet.engine` is used. The default `io.parquet.engine`
    behavior is to try ‘pyarrow’, falling back to ‘fastparquet’ if
    ‘pyarrow’ is unavailable. When using the `'pyarrow'` engine and no storage options are provided
    and a filesystem is implemented by both `pyarrow.fs` and `fsspec` (e.g. “s3://”),
    then the `pyarrow.fs` filesystem is attempted first. Use the filesystem keyword with an
    instantiated fsspec filesystem if you wish to use its implementation.
  * **compression** (`str`) – compression algorithm to use, default ‘snappy’
    - Name of the compression to use. Use None for no compression.
    - Supported options: ‘snappy’, ‘gzip’, ‘brotli’, ‘lz4’, ‘zstd’.
  * **index** (`bool`) – \_description_, defaults to None
    - If True, include the dataframe’s index(es) in the file output.
    - If False, they will not be written to the file.
    - If None, similar to True the dataframe’s index(es) will be saved.
    However, instead of being saved as values, the RangeIndex will be stored as
    a range in the metadata so it doesn’t require much space and is faster.
    Other indexes will be included as columns in the file output.
  * **partition_cols** (`List`[`str`]) – column names by which to partition the dataset, defaults to None
    - Columns are partitioned in the order they are given
    - Must be None if path is not a string
* **Return type:**
  `str`
* **Returns:**
  saved key or file path

## Submodules

## virt_s3.s3 module

### *class* virt_s3.s3.PredictConnectionStoreParams(user_id, store_name, store_owner)

Bases: `object`

Dataclass for Predict Connection Store Parameters

* **Parameters:**
  * **user_id** (`str`) – predict user id
  * **store_name** (`str`) – connection store name
  * **store_owner** (`str`) – connection store owner

### *class* virt_s3.s3.S3Params(bucket_name, endpoint_url, aws_access_key_id=None, aws_secret_access_key=None, region_name=None, profile_name=None, connection_store_params=None)

Bases: `object`

Dataclass for S3 Boto3 Connection Parameters

Required:
- bucket_name
- endpoint_url

Optional:
- region_name

Authentication Methods (and necessary params):

1. Explicit Credentials
  - aws_access_key_id
  - aws_secret_access_key

2. AWS Profile
  - profile_name

3. Predict Backend Connection Store
  - connection_store_params

* **Parameters:**
  * **bucket_name** (`str`) – aws s3 bucket
  * **endpoint_url** (`str`) – aws s3 url
  * **aws_access_key_id** (`str`) – your aws access key id, defaults to None
  * **aws_secret_access_key** (`str`) – your aws secret access key, defaults to None
  * **region_name** (`str`) – your aws region name, defaults to None
  * **profile_name** (`str`) – your aws IAM profile name, defaults to None
  * **connection_store_params** ([`PredictConnectionStoreParams`](#virt_s3.s3.PredictConnectionStoreParams)) – instance of PredictConnectionStoreParams, defaults to None

### *class* virt_s3.s3.S3SessionManager(s3_params=None, s3_client=None, keep_open=False, \*\*session_client_kwargs)

Bases: `object`

Session Context Manager for S3

* **Parameters:**
  * **s3_params** ([`S3Params`](#virt_s3.s3.S3Params)) – instance of S3Params, defaults to None
  * **s3_client** (`Session`) – boto3 s3 client object, defaults to None
  * **keep_open** (`bool`) – boolean flag to keep the session open or not outside of the context manager scope, defaults to False

### *class* virt_s3.s3.PerformanceMetrics(mbps=0.0)

Bases: `object`

Dataclass for different performance metrics

* **Parameters:**
  **mbps** (`float`) – megabytes per second, defaults to 0.0

### *class* virt_s3.s3.PerformanceRecord(\_type, metrics={'simple': [], 'transfer': []}, count=0, chosen_func=None)

Bases: `object`

Encpasulates performance for a given performance monitoring type

* **Parameters:**
  * **\_type** (`str`) – ‘upload’ or ‘download’
  * **metrics** (`Dict`[`str`, `List`[[`PerformanceMetrics`](#virt_s3.s3.PerformanceMetrics)]]) – dictionary of function name str -> list of PerformanceMetrics, defaults to { ‘simple’: [], ‘transfer’: [] }
  * **count** (`int`) – number of times this performance record has been updated, defaults to 0
  * **chosen_func** (`str`) – the specific function key name that was chosen to be run, defaults to None

### *class* virt_s3.s3.UploadDownloadPerformanceManager

Bases: `object`

Class used to record and determine which different upload or download
function to run based on a record of performance metrics over the course of
the program run lifetime

#### reset(\_type)

Method to reset the performance records dictionary

* **Parameters:**
  **\_type** (`str`) – ‘upload’ or ‘download’

#### average_metrics(metrics_li)

Method to get average of list of metrics

* **Parameters:**
  **metrics_li** (`List`[[`PerformanceMetrics`](#virt_s3.s3.PerformanceMetrics)]) – list of PerformanceMetrics
* **Return type:**
  [`PerformanceMetrics`](#virt_s3.s3.PerformanceMetrics)
* **Returns:**
  single instance of PerformanceMetrics aggregated as simple average

#### get_metrics(\_type, func_str)

Method to get the specific function PerformanceMetrics

* **Parameters:**
  * **\_type** (`str`) – ‘upload’ or ‘download’
  * **func_str** (`str`) – name of function key that you want to return list of PerformanceMetrics for
* **Return type:**
  `List`[[`PerformanceMetrics`](#virt_s3.s3.PerformanceMetrics)]
* **Returns:**
  list of PerformanceMetrics

#### choose_function(\_type)

Method to choose the right function to run based on historical throughput MBPS

* **Parameters:**
  **\_type** (`str`) – ‘upload’ or ‘download’
* **Return type:**
  `str`
* **Returns:**
  chosen function string name

#### update_performance_record(\_type, bytes_transferred, transfer_time)

Method used to update the performance record based
with throughput metrics

* **Parameters:**
  * **\_type** (`str`) – ‘upload’ or ‘download’
  * **bytes_transferred** (`int`) – number of bytes transferred
  * **transfer_time** (`float`) – total seconds the transfer took
* **Return type:**
  `None`

### virt_s3.s3.get_s3_default_params()

Function to get kwargs necessary for S3 connections

* **Return type:**
  [`S3Params`](#virt_s3.s3.S3Params)
* **Returns:**
  instance of S3Params

### virt_s3.s3.get_s3_session_client(s3_params, \*\*kwargs)

Function to get an S3 Boto3 Session client

Authentication priority in case multiple options are provided:
1. explicit supplied credentials (aws_access_key_id, aws_secret_access_key)
2. aws profile
3. connection store

* **Parameters:**
  **s3_params** ([`S3Params`](#virt_s3.s3.S3Params)) – instance of S3Params outlining s3 connectin parameters
* **Return type:**
  `Session`
* **Returns:**
  instance of boto3.Session.client that can be used to make requests to S3

### virt_s3.s3.create_s3_bucket(bucket_name, s3_client=None, s3_params=None, \*\*kwargs)

Function to create an S3 Bucket

* **Parameters:**
  * **bucket_name** (`str`) – name of bucket to create
  * **s3_client** – boto3 s3 client object, defaults to None
  * **s3_params** ([`S3Params`](#virt_s3.s3.S3Params)) – instance of S3Params, defaults to None
  * **local_fs_params** – instance of LocalFSParams, defaults to None
* **Return type:**
  `bool`
* **Returns:**
  True if successfully created, else False

### virt_s3.s3.get_s3_file_chunked(s3_fpath, s3_client=None, s3_params=None, chunk_size=1048576, progress_callback=None, bytes_io=False, \*\*kwargs)

Function to read an s3 file using a chunking loop. This can be useful
when trying to get very large files (relies on boto3.s3.get_object())

* **Parameters:**
  * **s3_fpath** (`str`) – s3 key
  * **s3_client** – boto3 s3 client object, defaults to None
  * **s3_params** ([`S3Params`](#virt_s3.s3.S3Params)) – instance of S3Params, defaults to None
  * **chunk_size** (`int`) – integer number of bytes per chunk to download, defaults to 1 \* MB
  * **progress_callback** (`Callable`[[`int`, `int`], `any`]) – user-defined custom progress callback that is called throughout the download process that takes as input         (current number of bytes downloaded so far, total number of bytes to download)
  * **bytes_io** (`bool`) – flag to convert pulled object as BytesIO instance, defaults to False
* **Return type:**
  `Union`[`BytesIO`, `bytes`, `None`]
* **Returns:**
  either BytesIO object, bytes object, or None

### virt_s3.s3.get_s3_file_simple(s3_fpath, s3_client=None, s3_params=None, bytes_io=False, \*\*kwargs)

Function to downlad a given s3 file (relies on boto3.s3.get_object())

* **Parameters:**
  * **s3_fpath** (`str`) – key to s3 file to download
  * **s3_client** – provided s3 client object, defaults to None
  * **s3_params** ([`S3Params`](#virt_s3.s3.S3Params)) – provided instance of S3Params, defaults to None
  * **bytes_io** (`bool`) – flag to convert pulled object as BytesIO instance, defaults to False
* **Return type:**
  `Union`[`BytesIO`, `bytes`, `None`]
* **Returns:**
  either bytes object, BytesIO object, or None

### virt_s3.s3.get_s3_file_transfer(s3_fpath, s3_client=None, s3_params=None, progress_callback=None, transfer_config=<boto3.s3.transfer.TransferConfig object>, bytes_io=False, \*\*kwargs)

Function to downlad a given s3 file (relies on boto3.s3.download_fileobj())

* **Parameters:**
  * **s3_fpath** (`str`) – key to s3 file to download
  * **s3_client** – provided s3 client object, defaults to None
  * **s3_params** ([`S3Params`](#virt_s3.s3.S3Params)) – provided instance of S3Params, defaults to None
  * **progress_callback** (`Callable`[[`int`, `int`], `any`]) – user-defined custom progress callback that is called throughout the download process that takes as input         (current number of bytes downloaded so far, total number of bytes to download)
  * **transfer_config** ([`TransferConfig`](#virt_s3.TransferConfig)) – instance of         [boto3.s3.transfer.TransferConfig]([https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.TransferConfig](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.TransferConfig)),        defaults to boto3.s3.transfer.TransferConfig(max_concurrency=3)
  * **bytes_io** (`bool`) – flag to convert pulled object as BytesIO instance, defaults to False
* **Return type:**
  `Union`[`BytesIO`, `bytes`, `None`]
* **Returns:**
  either bytes object, BytesIO object, or None

### virt_s3.s3.get_s3_file(s3_fpath, s3_client=None, s3_params=None, progress_callback=None, transfer_config=<boto3.s3.transfer.TransferConfig object>, bytes_io=False, \*\*kwargs)

Function to downlad a given s3 file using either: get_s3_file_simple() or get_s3_file_transfer().
Falls back to get_s3_file_chunked() if either of the above functions above fail.

* **Parameters:**
  * **s3_fpath** (`str`) – key to s3 file to download
  * **s3_client** – provided s3 client object, defaults to None
  * **s3_params** ([`S3Params`](#virt_s3.s3.S3Params)) – provided instance of S3Params, defaults to None
  * **progress_callback** (`Callable`[[`int`, `int`], `any`]) – user-defined custom progress callback that is called throughout the download process that takes as input         (current number of bytes downloaded so far, total number of bytes to download)
  * **transfer_config** ([`TransferConfig`](#virt_s3.TransferConfig)) – instance of         [boto3.s3.transfer.TransferConfig]([https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.TransferConfig](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.TransferConfig)),        defaults to boto3.s3.transfer.TransferConfig(max_concurrency=3)
  * **bytes_io** (`bool`) – flag to convert pulled object as BytesIO instance, defaults to False
* **Return type:**
  `Union`[`BytesIO`, `bytes`, `None`]
* **Returns:**
  either bytes object, BytesIO object, or None

### virt_s3.s3.get_s3_image(s3_fpath, s3_client=None, s3_params=None, img_format=None, bytes_io=False, \*\*kwargs)

Function to retrieve an image from S3.
Calls get_s3_file() so you can also pass in additional kwargs through to that function.

Formatting Hierarchy Logic: img_format > bytes_io
1. Check for img_format args
2. Then check for bytes_io arg
3. If neither provided return raw output of s3_object.read()

* **Parameters:**
  * **s3_fpath** (`str`) – key to s3 file to download
  * **s3_client** – provided s3 client object, defaults to None
  * **s3_params** (`Optional`[[`S3Params`](#virt_s3.s3.S3Params)]) – provided instance of S3Params, defaults to None
  * **img_format** (`Optional`[[`ImageFormatType`](#virt_s3.utils.ImageFormatType)]) – one of ImageFormatType enum, defaults to None
  * **bytes_io** (`bool`) – flag to convert pulled object as BytesIO instance, defaults to False
* **Return type:**
  `Union`[`BytesIO`, `Image`, `ndarray`, `str`, `bytes`, `None`]
* **Returns:**
  an instance of either BytesIO, PIL.Image.Image, np.ndarray, string, bytes, or None

### virt_s3.s3.get_s3_files_generator(key_list, s3_client=None, s3_params=None, bytes_io=False, \*\*kwargs)

Generator function to quickly loop through reading a list of s3 file keys.
Calls get_s3_file() so you can also pass in additional kwargs through to that function.

* **Parameters:**
  * **key_list** (`List`[`str`]) – list of s3 keys
  * **s3_client** – provided s3 client object, defaults to None
  * **s3_params** ([`S3Params`](#virt_s3.s3.S3Params)) – provided instance of S3Params, defaults to None
  * **bytes_io** (`bool`) – flag to convert pulled object as BytesIO instance, defaults to False
* **Return type:**
  `Generator`[`Union`[`BytesIO`, `bytes`, `None`], `Any`, `None`]
* **Returns:**
  None
* **Yield:**
  either BytesIO object, bytes object, or None

### virt_s3.s3.get_s3_files_batch(key_list, s3_client=None, s3_params=None, max_concurrency=0, bytes_io=False, \*\*kwargs)

Function to read a list of s3 file keys and return a batch data. Can use multithreading as well.
Calls get_s3_file() when max_concurrency=0 so you can also pass in additional kwargs through to that function.

* **Parameters:**
  * **key_list** (`List`[`str`]) – list of s3 keys
  * **s3_client** – provided s3 client object, defaults to None
  * **s3_params** ([`S3Params`](#virt_s3.s3.S3Params)) – provided instance of S3Params, defaults to None
  * **max_concurrency** (`int`) – max no. of concurrent threads to use when downloading multiple files (0 means no concurrency), defaults to 0
  * **bytes_io** (`bool`) – flag to convert pulled object as BytesIO instance, defaults to False
* **Return type:**
  `list`
* **Returns:**
  either pulled S3 object or BytesIO object

### virt_s3.s3.list_s3_folders(prefix, s3_client=None, s3_params=None, delimiter='/', \*\*kwargs)

Function to get list of valid folders within S3 Bucket Prefix

* **Parameters:**
  * **prefix** (`str`) – S3 Bucket Path Prefix
  * **s3_client** – provided s3 client object, defaults to None
  * **s3_params** ([`S3Params`](#virt_s3.s3.S3Params)) – provided instance of S3Params, defaults to None
  * **delimiter** (`str`) – delimiter used to filter objects in S3 (e.g. only subfolders - delimiter=”/”), defaults to ‘/’
* **Return type:**
  `List`[`str`]
* **Returns:**
  List of S3 Object Keys

### virt_s3.s3.get_valid_s3_keys(prefix, ignore=['.DS_Store'], filter_extensions=[], s3_client=None, s3_params=None, \*\*kwargs)

Function to get list of valid keys within S3 Bucket Path

* **Parameters:**
  * **prefix** (`str`) – S3 Bucket Path Prefix
  * **ignore** (`List`[`str`]) – list of directories/prefixes and filepaths to ignore, defaults to [‘.DS_Store’]
  * **filter_extensions** (`List`[`str`]) – list of file extensions to filter for (empty list means get everything), defaults to []
  * **s3_client** – provided s3 client object, defaults to None
  * **s3_params** ([`S3Params`](#virt_s3.s3.S3Params)) – provided instance of S3Params, defaults to None
* **Return type:**
  `List`[`str`]
* **Returns:**
  List of S3 Object Keys

### virt_s3.s3.key_exists_s3(key, s3_client=None, s3_params=None, \*\*kwargs)

Function to see if key exists in S3

* **Parameters:**
  * **key** (`str`) – key fpath string
  * **s3_client** – provided s3 client object, defaults to None
  * **s3_params** ([`S3Params`](#virt_s3.s3.S3Params)) – provided instance of S3Params, defaults to None
* **Return type:**
  `bool`
* **Returns:**
  True if key exists, False otherwise

### virt_s3.s3.upload_to_s3_simple(data, save_key, s3_client=None, s3_params=None, \*\*kwargs)

Function to upload data object to s3 using boto3.s3.put_object()

* **Parameters:**
  * **data** (`Union`[`bytes`, `memoryview`, `BytesIO`]) – data to save as bytes, memoryview, or BytesIO
  * **save_key** (`str`) – s3 key to save the data to
  * **s3_client** – provided s3 client object, defaults to None
  * **s3_params** ([`S3Params`](#virt_s3.s3.S3Params)) – provided instance of S3Params, defaults to None
* **Raises:**
  **Exception** – General exception if not HTTP Status Code 200
* **Return type:**
  `str`
* **Returns:**
  S3 key of uploaded object if successful

### virt_s3.s3.upload_to_s3_transfer(data, save_key, s3_client=None, s3_params=None, progress_callback=None, transfer_config=<boto3.s3.transfer.TransferConfig object>, \*\*kwargs)

Function to upload data object to s3 using boto3.s3.upload_fileobj()

* **Parameters:**
  * **data** (`Union`[`bytes`, `memoryview`, `BytesIO`]) – data to save as bytes, memoryview, or BytesIO
  * **save_key** (`str`) – s3 key to save the data to
  * **s3_client** – provided s3 client object, defaults to None
  * **s3_params** ([`S3Params`](#virt_s3.s3.S3Params)) – provided instance of S3Params, defaults to None
  * **progress_callback** (`Callable`[[`int`, `int`], `any`]) – user-defined custom progress callback that is called throughout the download process that takes as input         (current number of bytes uploaded so far, total number of bytes to download)
  * **transfer_config** ([`TransferConfig`](#virt_s3.TransferConfig)) – instance of         [boto3.s3.transfer.TransferConfig]([https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.TransferConfig](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.TransferConfig)),        defaults to boto3.s3.transfer.TransferConfig(max_concurrency=3)
* **Return type:**
  `str`
* **Returns:**
  S3 key of uploaded object if successful

### virt_s3.s3.upload_to_s3(data, save_key, s3_client=None, s3_params=None, progress_callback=None, transfer_config=<boto3.s3.transfer.TransferConfig object>, \*\*kwargs)

Function to upload data object to s3 using either: upload_to_s3_simple() or upload_to_s3_transfer().

* **Parameters:**
  * **data** (`Union`[`bytes`, `memoryview`, `BytesIO`]) – data to save as bytes, memoryview, or BytesIO
  * **save_key** (`str`) – s3 key to save the data to
  * **s3_client** – provided s3 client object, defaults to None
  * **s3_params** ([`S3Params`](#virt_s3.s3.S3Params)) – provided instance of S3Params, defaults to None
  * **progress_callback** (`Callable`[[`int`, `int`], `any`]) – user-defined custom progress callback that is called throughout the download process that takes as input         (current number of bytes uploaded so far, total number of bytes to download)
  * **transfer_config** ([`TransferConfig`](#virt_s3.TransferConfig)) – instance of         [boto3.s3.transfer.TransferConfig]([https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.TransferConfig](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.TransferConfig)),        defaults to boto3.s3.transfer.TransferConfig(max_concurrency=3)
* **Raises:**
  **Exception** – General exception if not HTTP Status Code 200 or not of right type
* **Return type:**
  `str`
* **Returns:**
  S3 key of uploaded object if successful

### virt_s3.s3.delete_s3_object(key, s3_client=None, s3_params=None, \*\*kwargs)

Function to delete an object from s3 based on its key

* **Parameters:**
  * **key** (`str`) – s3 key of object to delete
  * **s3_client** – provided s3 client object, defaults to None
  * **s3_params** ([`S3Params`](#virt_s3.s3.S3Params)) – provided instance of S3Params, defaults to None
* **Return type:**
  `bool`
* **Returns:**
  True if delete successful, else return False

### virt_s3.s3.delete_s3_objects_by_prefix(prefix, s3_client=None, s3_params=None, \*\*kwargs)

Function to delete all objects in S3 bucket that share a given prefix

* **Parameters:**
  * **prefix** (`str`) – S3 Bucket Path Prefix
  * **s3_client** – provided s3 client object, defaults to None
  * **s3_params** ([`S3Params`](#virt_s3.s3.S3Params)) – provided instance of S3Params, defaults to None
* **Return type:**
  `List`[`str`]
* **Returns:**
  List of S3 Object Keys that were successfully delete

### virt_s3.s3.extract_compressed_file_s3(key, extracted_dir_prefix=None, s3_client=None, s3_params=None, \*\*kwargs)

Function to extract zip file contents in S3

Compression Support:
- .zip
- .gzip [TODO]
- .tar.gz [TODO]

* **Parameters:**
  * **key** (`str`) – key to compressed file
  * **extracted_dir_prefix** (`Optional`[`str`]) – directory to prefix the extracted archive, defaults to None
  * **s3_client** – provided s3 client object, defaults to None
  * **s3_params** ([`S3Params`](#virt_s3.s3.S3Params)) – provided instance of S3Params, defaults to None
* **Return type:**
  `str`
* **Returns:**
  prefix path to directory where uncompressed file contents exist

## virt_s3.fs module

### *class* virt_s3.fs.LocalFSParams(use_local_fs, root_dir, user, bucket_name)

Bases: `object`

Dataclass for Using Local File System for all S3 Calls

* **Parameters:**
  * **use_local_fs** (`bool`) – flag to use the local file system or not for S3 calls
  * **root_dir** (`str`) – local file system root dir that represents your ‘bucket’
  * **user** (`str`) – your username
  * **bucket_name** (`str`) – emulated S3 ‘bucket’ directory in file system within root dir

### *class* virt_s3.fs.LocalFSSessionManager(local_fs_params=None, client=None, keep_open=False, \*\*session_client_kwargs)

Bases: `object`

Session Context Manager for Local File System

* **Parameters:**
  * **local_fs_params** ([`LocalFSParams`](#virt_s3.fs.LocalFSParams)) – instance of LocalFSParams, defaults to None
  * **client** – existing session client can be passed in, defaults to None
  * **keep_open** (`bool`) – boolean flag to keep the session open or not outside of the context manager scope, defaults to False

### virt_s3.fs.get_local_fs_params()

Function to get local file system parameters.

Checks for the following Environment Variables:
1. LOCAL_FS -> 1 or 0 (indicating whether to use local filesystem or not. 1 is True, 0 is False). Default behavior is False.
2. LOCAL_FS_ROOT_DIR -> path to local file system root dir
3. LOCAL_FS_USER -> username (email address) for app you’re trying to emulate
4. S3_DEFAULT_BUCKET -> bucket name proxy for local file system. Defaults to ‘default_bucket’.

* **Return type:**
  [`LocalFSParams`](#virt_s3.fs.LocalFSParams)
* **Returns:**
  instance of LocalFSParams

### virt_s3.fs.fix_fs_path(fpath, local_fs_params)

Function to fix the file or directory path on a local file system
according to root directory from LocalFSParams. Checks to see if root directory
is in the path or not and fixes it to be a valid path. Else, it joins the root
directory with the input path

* **Parameters:**
  * **fpath** (`str`) – input path
  * **local_fs_params** ([`LocalFSParams`](#virt_s3.fs.LocalFSParams)) – instance of LocalFSParams
* **Return type:**
  `str`
* **Returns:**
  updated file system path

### virt_s3.fs.create_fs_bucket(bucket_path, local_fs_params=None, \*\*kwargs)

Function to create a new ‘bucket’ directory in local file system

* **Parameters:**
  * **bucket_path** (`str`) – path to new ‘bucket’ directory
  * **local_fs_params** ([`LocalFSParams`](#virt_s3.fs.LocalFSParams)) – instance of LocalFSParams, defaults to None
* **Return type:**
  `bool`
* **Returns:**
  True if successfully created, else False

### virt_s3.fs.get_fs_file_chunked(fpath, local_fs_params=None, chunk_size=1048576, bytes_io=False, \*\*kwargs)

Function to read a file from local file system in chunking loop

* **Parameters:**
  * **fpath** (`str`) – file path
  * **local_fs_params** ([`LocalFSParams`](#virt_s3.fs.LocalFSParams)) – instance of LocalFSParams, defaults to None
  * **chunk_size** (`int`) – integer number of bytes per chunk to download, defaults to 1 \* MB
* **Return type:**
  `Union`[`BytesIO`, `bytes`, `None`]
* **Returns:**
  either BytesIO object, bytes object, or None

### virt_s3.fs.get_fs_file(fpath, local_fs_params=None, bytes_io=False, \*\*kwargs)

Function to read file from local file system

* **Parameters:**
  * **fpath** (`str`) – path to file
  * **local_fs_params** ([`LocalFSParams`](#virt_s3.fs.LocalFSParams)) – instance of LocalFSParams, defaults to None
  * **bytes_io** (`bool`) – flag to convert pulled object as BytesIO instance, defaults to False
* **Return type:**
  `Union`[`BytesIO`, `bytes`, `None`]
* **Returns:**
  instance of bytes or BytesIO object

### virt_s3.fs.get_fs_image(fpath, img_format=None, local_fs_params=None, bytes_io=False, \*\*kwargs)

Function to get image from local file system

* **Parameters:**
  * **fpath** (`str`) – path to local image file
  * **img_format** (`Optional`[[`ImageFormatType`](#virt_s3.utils.ImageFormatType)]) – oneof ImageFormatType enum, defaults to None
  * **local_fs_params** ([`LocalFSParams`](#virt_s3.fs.LocalFSParams)) – instance of LocalFSParams, defaults to None
  * **bytes_io** (`bool`) – flag to convert pulled object as BytesIO instance, defaults to False
* **Return type:**
  `Union`[`BytesIO`, `Image`, `ndarray`, `str`, `None`]
* **Returns:**
  an instance of either BytesIO, PIL.Image.Image, np.ndarray, string, or None

### virt_s3.fs.get_fs_files_generator(fpath_list, local_fs_params=None, bytes_io=False, \*\*kwargs)

Generator function to quickly loop through reading a list of file paths from local file system

* **Parameters:**
  * **fpath_list** (`List`[`str`]) – list of file paths
  * **local_fs_params** ([`LocalFSParams`](#virt_s3.fs.LocalFSParams)) – instance of LocalFSParams, defaults to None
  * **bytes_io** (`bool`) – flag to convert pulled object as BytesIO instance, defaults to False
* **Yield:**
  instance of bytes or BytesIO object
* **Return type:**
  `Generator`[`Union`[`BytesIO`, `bytes`, `None`], `Any`, `None`]

### virt_s3.fs.get_fs_files_batch(fpath_list, local_fs_params=None, max_concurrency=0, bytes_io=False, \*\*kwargs)

Function to read a list of file paths from local file system and return a batch of data.

* **Parameters:**
  * **fpath_list** (`List`[`str`]) – list of file paths
  * **local_fs_params** ([`LocalFSParams`](#virt_s3.fs.LocalFSParams)) – instance of LocalFSParams, defaults to None
  * **max_concurrency** (`int`) – max no. of concurrent threads to use when downloading multiple files (0 means no concurrency), defaults to 0
  * **bytes_io** (`bool`) – flag to convert pulled object as BytesIO instance, defaults to False
* **Return type:**
  `List`[`Union`[`BytesIO`, `bytes`, `None`]]
* **Returns:**
  list of bytes or BytesIO object

### virt_s3.fs.list_fs_folders(dir_path, local_fs_params=None, \*\*kwargs)

Function to list all 1st level subdirectories in a given directory path

* **Parameters:**
  * **dir_path** (`str`) – input directory path
  * **local_fs_params** ([`LocalFSParams`](#virt_s3.fs.LocalFSParams)) – instance of LocalFSParams, defaults to None
* **Return type:**
  `List`[`str`]
* **Returns:**
  list of subdirectory paths

### virt_s3.fs.get_valid_fs_fpaths(dir_path, ignore=['.DS_Store'], filter_extensions=[], local_fs_params=None, \*\*kwargs)

Funciton to get list of valid filepaths in file system (recursively) starting from
and input directory path. This includes nested file paths.

* **Parameters:**
  * **dir_path** (`str`) – input directory path to start from
  * **ignore** (`List`[`str`]) – list of directories/prefixes and filepaths to ignore, defaults to [‘.DS_Store’]
  * **filter_extensions** (`List`[`str`]) – list of file extensions to filter for (empty list means get everything), defaults to []
  * **local_fs_params** ([`LocalFSParams`](#virt_s3.fs.LocalFSParams)) – instance of LocalFSParams, defaults to None
* **Return type:**
  `List`[`str`]
* **Returns:**
  list of valid file paths

### virt_s3.fs.fpath_exists_fs(fpath, local_fs_params=None, \*\*kwargs)

Function to check if file path exists

* **Parameters:**
  * **fpath** (`str`) – input file path
  * **local_fs_params** ([`LocalFSParams`](#virt_s3.fs.LocalFSParams)) – instance of LocalFSParams, defaults to None
* **Return type:**
  `bool`
* **Returns:**
  True or False if it exists

### virt_s3.fs.upload_to_fs(data, save_path, local_fs_params=None, \*\*kwargs)

Function to write data to local file system

* **Parameters:**
  * **data** (`Union`[`bytes`, `memoryview`, `BytesIO`]) – input data to upload
  * **save_path** (`str`) – save path for newly written file
  * **local_fs_params** ([`LocalFSParams`](#virt_s3.fs.LocalFSParams)) – instance of LocalFSParams, defaults to None
* **Return type:**
  `str`
* **Returns:**
  saved file path

### virt_s3.fs.delete_fs_file(fpath, local_fs_params=None, \*\*kwargs)

Function to delete file from local file system

* **Parameters:**
  * **fpath** (`str`) – input file path to delete
  * **local_fs_params** ([`LocalFSParams`](#virt_s3.fs.LocalFSParams)) – instance of LocalFSParams, defaults to None
* **Return type:**
  `bool`
* **Returns:**
  True if deleted, False if not deleted

### virt_s3.fs.delete_fs_files_by_dir(dir_path, local_fs_params=None, \*\*kwargs)

Function to delete all files and sub-directories in given directory path (including itself)

* **Parameters:**
  * **dir_path** (`str`) – input directory path to delete
  * **local_fs_params** ([`LocalFSParams`](#virt_s3.fs.LocalFSParams)) – instance of LocalFSParams, defaults to None
* **Return type:**
  `List`[`str`]
* **Returns:**
  list of deleted filepaths

### virt_s3.fs.extract_compressed_file_fs(fpath, extracted_dir_prefix=None, local_fs_params=None, \*\*kwargs)

Function to extract zip file contents in local file system

Compression Support:
- .zip
- .gzip [TODO]
- .tar.gz [TODO]

* **Parameters:**
  * **fpath** (`str`) – path to compressed file to extract
  * **extracted_dir_prefix** (`Optional`[`str`]) – directory to prefix the extracted archive, defaults to None
  * **local_fs_params** ([`LocalFSParams`](#virt_s3.fs.LocalFSParams)) – instance of LocalFSParams, defaults to None
* **Return type:**
  `str`
* **Returns:**
  path to directory where uncompressed file contents exist

## virt_s3.utils module

### *class* virt_s3.utils.ImageFormatType(value, names=None, \*, module=None, qualname=None, type=None, start=1, boundary=None)

Bases: `Enum`

Enum class type for Image Format Types

Enum Options:
- PIL_IMAGE = “pil_img”
- BASE64_HTML_STRING = “base64_html_string”
- NUMPY_ARRAY = “numpy_array”

### virt_s3.utils.get_custom_logger(name='VirtS3', log_level=10)

Function to return a custom formatted logger object

* **Parameters:**
  * **name** (`str`) – name of logger, defaults to ‘VirtS3’
  * **log_level** (`int`) – desired logging level, defaults to logging.DEBUG
* **Return type:**
  `Logger`
* **Returns:**
  custom formatted Logger streaming to stdout

### virt_s3.utils.archive_zip_as_buffer(data_bytes_dict)

Function to create a zip archive from dictionary of expected archive filepaths
and data bytes

* **Parameters:**
  **data_bytes_dict** (`Dict`[`str`, `bytes`]) – { “/path/to/data/file/in/archive/file.extension”: data_as_bytes_obj }
* **Return type:**
  `BytesIO`
* **Returns:**
  zipped buffer BytesIO object

### virt_s3.utils.format_bytes(num_bytes)

Funtion to take as input a number of bytes
and return a formatted string for B, KB, MB, GB
rounded to 2 decimal places

* **Parameters:**
  **num_bytes** (`int`) – integer number of bytes
* **Return type:**
  `str`
* **Returns:**
  formatted byte string (e.g 5.11 MB )

## virt_s3.extras module

### virt_s3.extras.read_parquet_file_df(fpath, params=None, client=None, engine='auto', columns=None, filters=None, use_nullable_dtypes=False, \*\*download_kwargs)

Convenience function to read parquet file as pandas DataFrame.
Attempts to first read full buffer at once, then falls back to reading in batches if error
in reading full buffer at once.

* **Parameters:**
  * **fpath** (`str`) – path to parquet file or key
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to None
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
  * **engine** (`str`) – {{‘auto’, ‘pyarrow’, ‘fastparquet’}}, defaults to ‘auto’
    - Parquet library to use. If ‘auto’, then the option
    `io.parquet.engine` is used. The default `io.parquet.engine`
    behavior is to try ‘pyarrow’, falling back to ‘fastparquet’ if
    ‘pyarrow’ is unavailable. When using the `'pyarrow'` engine and no storage options are provided
    and a filesystem is implemented by both `pyarrow.fs` and `fsspec` (e.g. “s3://”),
    then the `pyarrow.fs` filesystem is attempted first. Use the filesystem keyword with an
    instantiated fsspec filesystem if you wish to use its implementation.
  * **columns** (`List`[`str`]) – If not None, only these columns will be read from the file, defaults to None
  * **filters** (`List`[`tuple`]) – To filter out data, defaults to None
    - Filter syntax: [[(column, op, val), …],…]
    where op is [==, =, >, >=, <, <=, !=, in, not in]
    The innermost tuples are transposed into a set of filters applied
    through an AND operation. The outer list combines these sets of filters through an OR
    operation. A single list of tuples can also be used, meaning that no OR
    operation between set of filters is to be conducted. Using this argument will NOT result in
    row-wise filtering of the final partitions unless `engine="pyarrow"` is also specified.  For other engines, filtering
    is only performed at the partition level, that is, to prevent the loading of some row-groups and/or files.
  * **use_nullable_dtypes** (`bool`) – boolean flag, defaults to False
    - If True, use dtypes that use `pd.NA` as missing value indicator for the resulting DataFrame.
    (only applicable for the `pyarrow` engine). As new dtypes are added that support `pd.NA` in the future, the
    output with this option will change to use those dtypes.
    Note: this is an experimental option, and behaviour (e.g. additional
    support dtypes) may change without notice.
* **Returns:**
  pd.DataFrame

### virt_s3.extras.write_parquet_file_df(df, save_fpath, params=None, client=None, engine='auto', compression=None, index=None, partition_cols=None, \*\*upload_kwargs)

Convenience function to write pandas DataFrame to parquet file.

* **Parameters:**
  * **df** (`DataFrame`) – pandas DataFrame to save
  * **save_fpath** (`str`) – parquet file save path or key (e.g. data.parquet.sz)
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to None
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
  * **engine** (`str`) – {{‘auto’, ‘pyarrow’, ‘fastparquet’}}, defaults to ‘auto’
    - Parquet library to use. If ‘auto’, then the option
    `io.parquet.engine` is used. The default `io.parquet.engine`
    behavior is to try ‘pyarrow’, falling back to ‘fastparquet’ if
    ‘pyarrow’ is unavailable. When using the `'pyarrow'` engine and no storage options are provided
    and a filesystem is implemented by both `pyarrow.fs` and `fsspec` (e.g. “s3://”),
    then the `pyarrow.fs` filesystem is attempted first. Use the filesystem keyword with an
    instantiated fsspec filesystem if you wish to use its implementation.
  * **compression** (`str`) – compression algorithm to use, default ‘snappy’
    - Name of the compression to use. Use None for no compression.
    - Supported options: ‘snappy’, ‘gzip’, ‘brotli’, ‘lz4’, ‘zstd’.
  * **index** (`bool`) – \_description_, defaults to None
    - If True, include the dataframe’s index(es) in the file output.
    - If False, they will not be written to the file.
    - If None, similar to True the dataframe’s index(es) will be saved.
    However, instead of being saved as values, the RangeIndex will be stored as
    a range in the metadata so it doesn’t require much space and is faster.
    Other indexes will be included as columns in the file output.
  * **partition_cols** (`List`[`str`]) – column names by which to partition the dataset, defaults to None
    - Columns are partitioned in the order they are given
    - Must be None if path is not a string
* **Return type:**
  `str`
* **Returns:**
  saved key or file path

### *class* virt_s3.extras.FileValidator(file_extensions=['.json', '.csv', '.parquet.sz'], params=<function get_default_params>)

Bases: `ABC`

Base Abstract Interface for File Type Validators

* **Parameters:**
  * **file_extensions** (`List`[`str`]) – supported file extensions by this Validator, defaults to [“.json”, “.csv”, “.parquet.sz”]
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to get_default_params

#### *abstract* validate_file(fpath, \*args, params=None, client=None, \*\*kwargs)

Method to implement based on specific child validator

* **Parameters:**
  * **fpath** (`str`) – path to file or key
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to get_default_params()
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
* **Return type:**
  `bool`
* **Returns:**
  True if valid file, False if invalid file

#### run(fpath_li=[], root_path=None, ignore=[])

Method to run File Validator

* **Parameters:**
  * **fpath_li** (`List`[`str`]) – list of files paths to run validation on, defaults to []
  * **root_path** (`str`) – root dir path or prefix to start looking for files within to validated, defaults to None
  * **ignore** (`List`[`str`]) – list of dirs/prefixes/files to ignore, defaults to []
* **Return type:**
  `dict`
* **Returns:**
  dictionary of { ‘valid’: List[file paths], ‘invalid’: List[file paths] }

### *class* virt_s3.extras.JSONFileValidator(file_extensions=['.json'], params=<function get_default_params>)

Bases: [`FileValidator`](#virt_s3.extras.FileValidator)

Interface for JSON FIle Validation

* **Parameters:**
  * **file_extensions** (`List`[`str`]) – supported file extensions by this Validator, defaults to [“.json”, “.csv”, “.parquet.sz”]
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to get_default_params

#### validate_file(fpath, client=None)

Implemented method to validate JSON files

* **Parameters:**
  * **fpath** (`str`) – path to file or key
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
* **Return type:**
  `bool`
* **Returns:**
  True if valid file, False if invalid file

### *class* virt_s3.extras.CSVFileValidator(file_extensions=['.csv'], params=<function get_default_params>)

Bases: [`FileValidator`](#virt_s3.extras.FileValidator)

Interface for CSV File Validation

* **Parameters:**
  * **file_extensions** (`List`[`str`]) – supported file extensions by this Validator, defaults to [“.json”, “.csv”, “.parquet.sz”]
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to get_default_params

#### validate_file(fpath, client=None)

Implemented method to validate CSV files

* **Parameters:**
  * **fpath** (`str`) – path to file or key
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
* **Return type:**
  `bool`
* **Returns:**
  True if valid file, False if invalid file

### *class* virt_s3.extras.ParquetFileValidator(file_extensions=['.parquet.sz', '.parquet'], params=<function get_default_params>)

Bases: [`FileValidator`](#virt_s3.extras.FileValidator)

Interface for Parquet File Validation

* **Parameters:**
  * **file_extensions** (`List`[`str`]) – supported file extensions by this Validator, defaults to [“.json”, “.csv”, “.parquet.sz”]
  * **params** (`Union`[[`S3Params`](#virt_s3.s3.S3Params), [`LocalFSParams`](#virt_s3.fs.LocalFSParams)]) – either instance of s3.S3Params or fs.LocalFSParams, defaults to get_default_params

#### validate_file(fpath, client=None)

Implemented method to validate Parquet files

* **Parameters:**
  * **fpath** (`str`) – path to file or key
  * **client** (`Optional`[`Session`]) – instance of either s3.boto3.Sesssion or None, defaults to None
* **Return type:**
  `bool`
* **Returns:**
  True if valid file, False if invalid file
