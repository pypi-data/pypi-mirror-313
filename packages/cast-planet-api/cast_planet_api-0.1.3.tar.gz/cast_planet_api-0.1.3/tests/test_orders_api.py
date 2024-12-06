import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, call, MagicMock
from uuid import UUID

from cast_planet.orders.api import OrdersApi
from cast_planet.orders.models.order_details import OrderDetails, ResultState, OrderDetailsLinks, OrderResult, OrderState


class TestDownloadOrderResults(unittest.TestCase):
    @patch("cast_planet.orders.api.download_file")
    @patch("cast_planet.orders.api.OrdersApi.get_order_details_by_id")
    @patch("cast_planet._utils._base_api.setup_logger")
    def test_download_order_results_logs_errors(self, mock_setup_logger, mock_get_order_details_by_id, mock_download_file):
        # Mock the logger
        mock_logger = MagicMock()
        mock_setup_logger.return_value = mock_logger

        # Mock the order details with results
        mock_order = OrderDetails(
            id=UUID("12345678-1234-5678-1234-567812345678"),
            name='test_order',
            _links=OrderDetailsLinks(
                _self='not used',
                results=[
                    OrderResult(
                        delivery=ResultState.SUCCESS,
                        name="file1",
                        location="https://example.com/file1",
                        expires_at=datetime.now() + timedelta(days=1),
                    ),
                    OrderResult(
                        delivery=ResultState.SUCCESS,
                        name="file2",
                        location="https://example.com/file2",
                        expires_at=datetime.now() + timedelta(days=1),
                    ),
                ]
            ),
            created_on=datetime.now(),
            last_modified=datetime.now(),
            source_type='not used',
            order_type='not_used',
            error_hints=[],
            state=OrderState.SUCCESS,
            last_message='none'
        )
        mock_get_order_details_by_id.return_value = mock_order

        # Mock the download_file function to raise an exception for the second file
        mock_download_file.side_effect = ["/path/to/file1", Exception("Download failed for file2")]

        # Initialize OrdersApi and call download_order_results
        api = OrdersApi(api_key="test_api_key")
        downloaded_files = api.download_order_results(order=mock_order, folder="/downloads")

        # Assert that only the successful file is returned
        self.assertEqual(downloaded_files, ["/path/to/file1"])

        # Verify that the logger.error was called for the failed download
        mock_logger.error.assert_called_once_with(str(Exception('Download failed for file2')))

        # Verify that download_file was called twice
        self.assertEqual(mock_download_file.call_count, 2)

        # Verify the calls to download_file
        mock_download_file.assert_has_calls([
            call(api._session, "https://example.com/file1", "/downloads", "file1"),
            call(api._session, "https://example.com/file2", "/downloads", "file2")
        ])


if __name__ == "__main__":
    unittest.main()
