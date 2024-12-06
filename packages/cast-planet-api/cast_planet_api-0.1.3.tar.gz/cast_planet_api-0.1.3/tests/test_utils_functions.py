import unittest
from unittest.mock import patch, MagicMock
import logging
import os
from requests.models import Response
from io import BytesIO
from cast_planet._utils._functions import setup_logger, download_file  # Adjust import according to your actual module


class TestSetupLogger(unittest.TestCase):
    @patch('logging.getLogger')
    def test_setup_logger_with_file(self, mock_get_logger):
        """Test the setup_logger function with a file handler."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Call the setup_logger function with a log file path
        logger = setup_logger('test.log')

        # Ensure the logger is created with the correct parameters
        mock_get_logger.assert_called_once_with('cast_planet._utils._functions')
        mock_logger.setLevel.assert_called_once_with(logging.ERROR)

        # Check if file handler was added
        file_handler = mock_logger.addHandler.call_args_list[1][0][0]
        self.assertIsInstance(file_handler, logging.FileHandler)
        self.assertEqual(os.path.basename(file_handler.baseFilename), 'test.log')

    @patch('logging.getLogger')
    def test_setup_logger_without_file(self, mock_get_logger):
        """Test the setup_logger function without a file handler (console only)."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Call the setup_logger function without a log file
        logger = setup_logger()

        # Ensure the logger is created with the correct parameters
        mock_get_logger.assert_called_once_with('cast_planet._utils._functions')
        mock_logger.setLevel.assert_called_once_with(logging.ERROR)

        # Ensure that no file handler was added
        self.assertEqual(len(mock_logger.addHandler.call_args_list), 1)  # Only console handler should be added


class TestDownloadFile(unittest.TestCase):
    @patch('os.makedirs')  # Mock os.makedirs to avoid actually creating directories
    @patch('builtins.open', new_callable=MagicMock)
    @patch('requests.Session.get')
    @patch('tqdm.tqdm')  # Mock tqdm to avoid progress bar in test output
    def test_download_file_success(self, mock_tqdm, mock_get, mock_open, mock_makedirs):
        """Test the download_file function for a successful download."""
        # Mock the response object
        mock_response = MagicMock(spec=Response)
        mock_response.headers = {'content-length': '100'}
        mock_response.iter_content.return_value = [b'chunk1', b'chunk2']  # Simulated chunks
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Set up mock for tqdm
        mock_progress_bar = MagicMock()
        mock_tqdm.return_value = mock_progress_bar

        # Mock open to return a mock file object
        mock_file = MagicMock()
        mock_open.return_value = mock_file

        # Call download_file
        result = download_file(MagicMock(), 'http://example.com/file', folder='test_folder', filename='test_file.txt')

        # Check that the file path returned is correct
        self.assertEqual(result, 'test_folder/test_file.txt')

        # Ensure the directory is created
        mock_makedirs.assert_called_once_with('test_folder', exist_ok=True)

    @patch('requests.Session.get')
    def test_download_file_no_location(self, mock_get):
        """Test that download_file raises an error when no location is provided."""
        with self.assertRaises(ValueError) as context:
            download_file(MagicMock(), None)  # Pass None for location

        self.assertEqual(str(context.exception), "Failed to Download. No location provided.")

    @patch('requests.Session.get')
    def test_download_file_no_filename_in_response(self, mock_get):
        """Test that download_file raises an exception when no filename is provided and cannot be derived from the response."""
        # Mock the response object
        mock_response = MagicMock(spec=Response)
        mock_response.headers = {}  # No content-disposition header
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as context:
            download_file(MagicMock(), 'http://example.com/file')

        self.assertTrue("Could not determine file name from HTTP response" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
