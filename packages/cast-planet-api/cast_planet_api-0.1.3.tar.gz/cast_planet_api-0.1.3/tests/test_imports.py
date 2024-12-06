import unittest


class TestPackageImports(unittest.TestCase):
    def test_data_api(self):
        from cast_planet import DataAPI
        from cast_planet.data import AssetFilter
        from cast_planet.data import AndFilter
        from cast_planet.data import GeometryFilter

    def test_orders_api(self):
        from cast_planet import OrdersApi
        from cast_planet.orders import OrderDetails

    def test_basemap_api(self):
        from cast_planet import BasemapApi, BaseMapAOISearch


if __name__ == '__main__':
    unittest.main()
