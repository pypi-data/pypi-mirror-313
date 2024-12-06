from enum import Enum
from typing import Dict
from io import BytesIO

import logging, zipfile

KB = 1024
MB = KB * KB


class ImageFormatType(Enum):
    """Enum class type for Image Format Types

    Enum Options:
    - PIL_IMAGE = "pil_img"
    - BASE64_HTML_STRING = "base64_html_string"
    - NUMPY_ARRAY = "numpy_array"
    """
    PIL_IMAGE = "pil_img"
    BASE64_HTML_STRING = "base64_html_string"
    NUMPY_ARRAY = "numpy_array"


def get_custom_logger(name: str = "VirtS3", log_level: int = logging.DEBUG) -> logging.Logger:
    """Function to return a custom formatted logger object

    :param name: name of logger, defaults to 'VirtS3'
    :param log_level: desired logging level, defaults to logging.DEBUG
    :return: custom formatted Logger streaming to stdout
    """
    logger = logging.getLogger(name)
    logger.propagate = False
    
    if len(logger.handlers) > 0: return logger
    
    # handlers
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)

    # formatters
    formatter = logging.Formatter(f'[%(name)s][%(filename)s][%(funcName)s][L%(lineno)d][%(asctime)s][%(levelname)s]: %(message)s', "%Y-%m-%d %H:%M:%S")
    stream_handler.setFormatter(formatter)
    logger.setLevel(log_level)
    logger.handlers = [stream_handler]
    return logger


def archive_zip_as_buffer(data_bytes_dict: Dict[str, bytes]) -> BytesIO:
    """Function to create a zip archive from dictionary of expected archive filepaths
    and data bytes
    
    :param data_bytes_dict: { "/path/to/data/file/in/archive/file.extension": data_as_bytes_obj }
    :return: zipped buffer BytesIO object
    """
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as z:
        for fpath, data_bytes in data_bytes_dict.items():
            z.writestr(fpath, data_bytes)
    zip_buffer.seek(0)

    return zip_buffer


def format_bytes(num_bytes: int) -> str:
    """Funtion to take as input a number of bytes 
    and return a formatted string for B, KB, MB, GB
    rounded to 2 decimal places

    :param num_bytes: integer number of bytes
    :return: formatted byte string (e.g 5.11 MB )
    """
    # Define the units in increasing size order
    units = ["B", "KB", "MB", "GB", "TB"]
    
    # Start with bytes, and progressively divide by 1024 for each next unit
    unit_index = 0
    while num_bytes >= 1024 and unit_index < len(units) - 1:
        num_bytes /= 1024
        unit_index += 1

    # Format the number to 2 decimal places and return the formatted string
    return f"{num_bytes:.2f} {units[unit_index]}"