import unittest
from unittest.mock import MagicMock, patch
from uuid import UUID

from mocks.models.mosaic_factory import MosaicModelFactory
from mocks.models.orders_factory import OrdersModelFactory
from cast_planet.orders.models.order_details import OrderDetails, OrderState
from cast_planet import BaseMapAOISearch
from cast_planet.basemap.models import OrderStatus

washingtonCounty = {
    "type": "Polygon",
    "properties": {
        "name": "Washington County, Arkansas"
    },
    "coordinates": [
        [
            [-94.5342, 35.9746],
            [-94.5342, 36.2414],
            [-94.0893, 36.2414],
            [-94.0893, 35.9746],
            [-94.5342, 35.9746]
        ]
    ]
}


class TestBaseMapAOISearch(unittest.TestCase):

    @patch("cast_planet.basemap.aoi_search.BasemapApi")
    @patch("cast_planet.basemap.aoi_search.OrdersApi")
    def setUp(self, mock_orders_api, mock_basemap_api):
        # Mock the APIs
        self.mock_orders_api = mock_orders_api.return_value
        self.mock_basemap_api = mock_basemap_api.return_value

        # Initialize BaseMapAOISearch with mocked APIs
        self.api = BaseMapAOISearch(api_key="test_api_key")

    def test_list_mosaics(self):
        # Mock list_mosaics response
        mock_mosaics = [
            MosaicModelFactory.create('Mosaic 1'),
            MosaicModelFactory.create('Mosaic 2'),
        ]

        self.mock_basemap_api.list_mosaics.return_value = mock_mosaics

        # Call the method
        mosaics = self.api.list_mosaics()

        # Assert the result
        self.assertEqual(mosaics, mock_mosaics)
        self.mock_basemap_api.list_mosaics.assert_called_once()

    @patch("cast_planet.basemap.aoi_search.uuid4")
    def test_order_mosaic_geojson(self, mock_uuid):
        # Mock UUID generation
        mock_uuid.return_value = UUID("12345678-1234-5678-1234-567812345678")

        # Mock order creation
        self.mock_orders_api.create_order.return_value = (
            OrdersModelFactory.createOrderDetails('Test', OrderState.SUCCESS))

        # Call the method
        result = self.api.order_mosaic_geojson(
            mosaic_names=["Mosaic1", "Mosaic2"],
            aoi=washingtonCounty,
            projection="EPSG:4326",
            email_notification=True
        )

        # Assert the result
        self.assertEqual(result.name, 'Test')

        # Verify order creation call
        self.mock_orders_api.create_order.assert_called_once()
        create_order_call_args = self.mock_orders_api.create_order.call_args[0][0]
        self.assertEqual(create_order_call_args.name, "Basemap AOI Wizard: 12345678-1234-5678-1234-567812345678")
        self.assertEqual(len(create_order_call_args.products), 2)

    def test_check_status(self):
        # Mock order status response
        mock_order_status = MagicMock(spec=OrderStatus)
        mock_order_details = MagicMock(spec=OrderDetails)
        self.mock_orders_api.get_order_details_by_id.return_value = mock_order_details
        mock_order_details.model_dump.return_value = {"state": "success", "last_message": "Order complete"}

        # Call the method
        result = self.api.check_status(UUID("12345678-1234-5678-1234-567812345678"))

        # Assert the result
        self.assertIsInstance(result, OrderStatus)
        self.assertEqual(result.state, OrderState.SUCCESS)
        self.assertEqual(result.last_message, "Order complete")

        # Verify get_order_details_by_id was called
        self.mock_orders_api.get_order_details_by_id.assert_called_once_with("12345678-1234-5678-1234-567812345678")


if __name__ == "__main__":
    unittest.main()
