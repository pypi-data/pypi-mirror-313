import unittest

from cast_planet.orders.models.order_new import CreateOrder
from cast_planet.orders.models.tools import BasemapClipObject, MergeObject, CouldHaveToolsList

class MyTestCase(unittest.TestCase):
    def test_something(self):
        tools = [MergeObject(), BasemapClipObject()]

        sut = CouldHaveToolsList(tools=tools)

        self.assertEqual(2, len(sut.tools))

    def test_create_order_with_tools(self):
        tools = [MergeObject(), BasemapClipObject()]
        order = CreateOrder(name='Test', tools=tools)

if __name__ == '__main__':
    unittest.main()
