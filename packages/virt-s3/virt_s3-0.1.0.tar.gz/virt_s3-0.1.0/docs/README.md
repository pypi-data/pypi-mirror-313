# Virt-S3 🪣

A Virtualitics utility package to handle file I/O with Object Storage Systems like AWS S3 and Minio. 

With versatility in mind, `virt-s3` was designed to be a relatively lightweight package that can either used independently or in conjunction with the larger Virtualitics AI platform. The `virt-s3` module includes two primary submodules `s3` and `fs` that implement each API function of the `virt-s3` module specific to the target system: either S3/S3-like systems or local file systems.

We hope that you can use it, break it, and even help us improve it!

## Table of Contents
1. [Prerequisites](#Prerequisites)
2. [Example Usage](#Example-Usage)
3. [Getting Started](#Getting-Started)
4. [Documentation](#Code-Documentation)


## Prerequisites
- Requires python>=3.11
- Local File System features currently only support posix `/` pathing (Linux, Mac, etc.)
    * Support for Windows `\` pathing [Coming Soon]


## Example Usage

### Writing a File
```python
import virt_s3
import pandas as pd
from io import BytesIO

# get default params (LocalFS or S3 determined by env variables)
# can also explicitly create instance of LocalFSParams or S3Params
params = virt_s3.get_default_params()

# test data -- write to in-memory buffer
df = pd.DataFrame([{'a': 1, 'b': 2}])
buffer = BytesIO()
df.to_csv(buffer, index=None)

# use context manager to manage session scope
with virt_s3.SessionManager(params=params) as session:
    # create bucket
    virt_s3.create_bucket('test-bucket', params=params, client=session)

    # upload data
    path = f"fixture/data/data.csv"
    saved_key = virt_s3.upload_data(buffer.getbuffer(), path, params=params, client=session)
```

### Reading a File
```python
import virt_s3
import pandas as pd

# get default params (LocalFS or S3 determined by env variables)
# can also explicitly create instance of LocalFSParams or S3Params
params = virt_s3.get_default_params()

# use context manager to manage session scope
with virt_s3.SessionManager(params=params) as session:
    # download data
    data = virt_s3.get_file(saved_key, bytes_io=True, params=params, client=session)
    df = pd.read_csv(data)
```

## Getting Started
1. Create a fresh virtual environment with python >= 3.11

2. Install the necessary dependencies
```bash
$ pip install poetry
$ poetry install
$ pip show virt-s3
$ poetry install -E s3 -E dataframe -E image -E test -E docs
```
- Note: the last command above will install the optional extra dependencies needed to do the following
    * **s3** = installs dependencies required to interact with object stores like Minio/S3 (primarily relying on `boto3`)
    * **dataframe** = installs dependencies required for using `numpy`, `pandas`, and `pyarrow` dataframe/parquet operations
    * **image** = installs dependencies required to utilize image operations (e.g. get file as an image)
    * **test** = installs pytest related dependencies for testing
    * **docs** = installs sphinx documentation generation dependencies

    * e.g. If you want to use `virt_s3`, but can't install `pandas` or `pyarrow` in your restricted environment, then you can simply install `virt_s3` without the `dataframe` extra dependencies. You won't be able to use `virt_s3.extras.CSVFileValidator`, `virt_s3.extras.ParquetFileValidator`, `read_parquet_file_df`, and `write_parquet_file_df` but these are also not necessarily core functions of the library (therefore extras).

3. Make sure the following environment variables are set

```.env
#########################################
# Required Custom Environment Variables #
#########################################
LOCAL_FS_USER=<your username>
# use the local fs mirror or s3/minio: 1 = True, 0 = False
LOCAL_FS=0
LOCAL_FS_ROOT_DIR=</path/to/your/data/dir/>

########################################################
# Required Virtualitics Platform Environment Variables #
########################################################
# e.g. http://mock-s3:9000 or http://localhost:9000
S3_URL=<your s3/minio url>
S3_DEFAULT_BUCKET=test-buck<your bucket name>
AWS_SECRET_ACCESS_KEY=<your aws secret access key>
AWS_ACCESS_KEY_ID=<your aws access key id>
# e.g. us-east-1
AWS_REGION=<your aws region>
```

- Note: `S3_URL` can be replaced with a localhost url (e.g. http://localhost:9000) if not being run within a docker container

4. Run the above [example usage](#Example-Usage)

## Code Documentation

- [Full Module Table of Contents](modules.md)
- [Full Module API Specs](virt_s3.md)

| API |  Description  |
|-----|---------------|
|[`PredictConnectionStoreParams`](virt_s3.md#class-virt_s3predictconnectionstoreparamsuser_id-store_name-store_owner)| Dataclass for Predict Connection Store Parameters |
|[`S3Params`](virt_s3.md#class-virt_s3s3paramsbucket_name-endpoint_url-aws_access_key_idnone-aws_secret_access_keynone-region_namenone-profile_namenone-connection_store_paramsnone)| Dataclass for S3 Boto3 Connection Parameters |
|[`SessionManager`](virt_s3.md#class-virt_s3sessionmanagerparamsnone-clientnone-keep_openfalse-session_client_kwargs)| General Session Context Manager for virt_s3 repo |
|[`TransferConfig`](virt_s3.md#class-virt_s3transferconfigmultipart_threshold8388608-max_concurrency10-multipart_chunksize8388608-num_download_attempts5-max_io_queue100-io_chunksize262144-use_threadstrue-max_bandwidthnone-preferred_transfer_clientauto)| [boto3.s3.TransferConfig](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3.html) used to configure higher throughput upload/download functions |
|[`LocalFSParams`](virt_s3.md#class-virt_s3localfsparamsuse_local_fs-root_dir-user-bucket_name)| Dataclass for Using Local File System for all S3 Calls |
|[`ImageFormatType`](virt_s3.md#class-virt_s3imageformattypevalue-namesnone--modulenone-qualnamenone-typenone-start1-boundarynone)| Enum class type for Image Format Types |
|[`get_default_params()`](virt_s3.md#virt_s3get_default_paramsuse_localfalse-use_s3false)| Function to get default parameters to use for all functions (default behavior is based off of ENV variables) |
|[`get_session_client()`](virt_s3.md#virt_s3get_session_clientparamsnone-kwargs)| Function to get session client based on passed in `S3Params` or `LocalFSParams`|
|[`create_bucket()`](virt_s3.md#virt_s3create_bucketbucket_name-paramsnone-clientnone)| Function to create a bucket to read and write from |
|[`get_file_chunked()`](virt_s3.md#virt_s3get_file_chunkedfpath-paramsnone-clientnone-kwargs)| Function to get a file using a chunking loop. This can be useful when trying to retrieve very large files |
|[`get_file()`](virt_s3.md#virt_s3get_filefpath-paramsnone-clientnone-bytes_iofalse-kwargs)| Function to retrieve specified file as in-memory object|
|[`get_image()`](virt_s3.md#virt_s3get_imagefpath-paramsnone-clientnone-img_formatnone-bytes_iofalse-kwargs)| Function to get image from either s3 or local file system |
|[`get_files_generator()`](virt_s3.md#virt_s3get_files_generatorfpath_li-paramsnone-clientnone-bytes_iofalse-kwargs)| Generator function to quickly loop through reading a list of keys or file paths |
|[`get_files_batch()`](virt_s3.md#virt_s3get_files_batchfpath_li-paramsnone-clientnone-max_concurrency0-bytes_iofalse-kwargs)| Function to get list of file paths or key paths in batch |
|[`list_dirs()`](virt_s3.md#virt_s3list_dirsdir_path-paramsnone-clientnone-delimiter-kwargs)| Function to list valid 'folders' within 'bucket'|
|[`get_valid_file_paths()`](virt_s3.md#virt_s3get_valid_file_pathsdir_path-ignoreds_store-filter_extensions-paramsnone-clientnone-kwargs)| Function to get list of valid file paths or keys within particular directory of bucket |
|[`file_exists()`](virt_s3.md#virt_s3file_existsfpath-paramsnone-clientnone-kwargs)| Function to see if key or file path exists in bucket |
|[`upload_data()`](virt_s3.md#virt_s3upload_datadata-fpath-paramsnone-clientnone-kwargs)| Function to upload data to S3 or local file system |
|[`delete_file()`](virt_s3.md#virt_s3delete_filefpath-paramsnone-clientnone-kwargs)| Function to delete a file from s3 or local file system |
|[`delete_files_by_dir()`](virt_s3.md#virt_s3delete_files_by_dirdir_path-paramsnone-clientnone-kwargs)| Function to delete all files and subdirectories, etc. in a given folder |
|[`archive_zip_as_buffer()`](virt_s3.md#virt_s3archive_zip_as_bufferdata_bytes_dict)| Function to create a zip archive from dictionary of expected archive filepaths and data bytes|
|[`extract_compressed_file()`](virt_s3.md#virt_s3extract_compressed_filefpath-extracted_dir_prefixnone-paramsnone-clientnone-kwargs) | Function to extract zip file contents into bucket |
|[`format_bytes()`](virt_s3.md#virt_s3utilsformat_bytesnum_bytes) | Funtion to take as input a number of bytes and return a formatted string for B, KB, MB, GB |
|[`read_parquet_file_df()`](virt_s3.md#virt_s3read_parquet_file_dffpath-paramsnone-clientnone-engineauto-columnsnone-filtersnone-use_nullable_dtypesfalse-download_kwargs)| Convenience function to read parquet file as pandas DataFrame |
|[`write_parquet_file_df()`](virt_s3.md#virt_s3write_parquet_file_dfdf-save_fpath-paramsnone-clientnone-engineauto-compressionnone-indexnone-partition_colsnone-upload_kwargs)| Convenience function to write pandas DataFrame to parquet file |