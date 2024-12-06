import unittest
from unittest.mock import patch

from mocks.models.mosaic_factory import MosaicModelFactory
from cast_planet import BasemapApi


class TestGatherMosaicsFromResponse(unittest.TestCase):
    @patch("cast_planet.BasemapApi._get")
    def test_gather_mosaics_from_response(self, mock_get):
        mosaic1 = MosaicModelFactory.create('Mosaic 1')
        mosaic2 = MosaicModelFactory.create('Mosaic 2')
        mosaic3 = MosaicModelFactory.create('Mosaic 3')

        initial_response = MosaicModelFactory.createResponse([mosaic1], "http://next-page-url")

        # Mock responses
        mock_get.side_effect = [
            MosaicModelFactory.createResponse([mosaic2], "http://next-page-url-2").model_dump(by_alias=True),
            MosaicModelFactory.createResponse([mosaic3]).model_dump(by_alias=True)
        ]

        # Initialize API instance
        api = BasemapApi(api_key="test_api_key")

        # Call the method
        result = api.__gather_mosaics_from_response__(initial_response)

        # Assertions
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].name, "Mosaic 1")
        self.assertEqual(result[1].name, "Mosaic 2")
        self.assertEqual(result[2].name, "Mosaic 3")

        # Verify calls
        self.assertEqual(mock_get.call_count, 2)


if __name__ == "__main__":
    unittest.main()
