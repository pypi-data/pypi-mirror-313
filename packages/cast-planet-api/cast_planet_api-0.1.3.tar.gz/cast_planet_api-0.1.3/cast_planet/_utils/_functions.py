import logging
import os
from typing import Union, Optional

from requests import Session
from tqdm import tqdm


def setup_logger(log_filename = None, level: Optional[int] = None) -> logging.Logger:
    """
    Set up the logger to log to the console by default or to a file if `log_filename` is provided.

    :param level: Log level for logging, default is ERROR
    :param log_filename: If provided, logs will be written to a log file.
    :return: The configured logger instance.
    """
    if level is None:
        level = logging.ERROR

    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    # Create console handler and set level to debug
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add console handler to logger
    logger.addHandler(console_handler)

    # If log_to_file is True, also add a file handler
    if log_filename is not None:
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def download_file(session: Session, location: str, folder: str = None, filename: str = None) -> str:
    """
    Helper function to download a file and save it to a specified folder with a progress bar.

    :param session: Active Planet API session.
    :param location: URL of the file to download.
    :param folder: Folder to save the downloaded file. Default is current directory.
    :param filename: Filename for the downloaded file. If None, it will be extracted from the response.
    :return: The full file path of the downloaded file.
    """
    # Ensure location is provided
    if location is None:
        raise ValueError("Failed to Download. No location provided.")

    # Perform the HTTP GET request to fetch the file
    response = session.get(location, stream=True)
    response.raise_for_status()  # Assumes error handling is done in custom session

    # Set default folder to the current location if not provided
    if folder is None:
        folder = "."

    # Determine the filename if not provided
    if filename is None:
        content_disposition = response.headers.get("content-disposition")
        if content_disposition and "filename=" in content_disposition:
            filename = content_disposition.split("filename=")[-1].strip("\"'")
        else:
            raise Exception("Could not determine file name from HTTP response. Please supply a filename manually.")


    # Build the full file path
    local_filename = os.path.join(folder, filename)

    # Make sure the folder exists
    os.makedirs(os.path.dirname(local_filename), exist_ok=True)

    # Get the total size for the progress bar
    total_size = int(response.headers.get('content-length', 0))

    # Download the file with a progress bar
    with open(local_filename, "wb") as f:
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=local_filename, ascii=True) as progress_bar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    progress_bar.update(len(chunk))

    return local_filename
