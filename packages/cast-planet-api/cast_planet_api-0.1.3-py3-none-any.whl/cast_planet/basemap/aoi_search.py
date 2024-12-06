from typing import Union, List
from uuid import uuid4, UUID

from pydantic_geojson import PolygonModel, MultiPolygonModel

from cast_planet.basemap.api import BasemapApi
from cast_planet.basemap.models import OrderStatus
from cast_planet.orders.models.common import OrderSource, OrderType
from cast_planet.orders.models.order_new import CreateOrder
from cast_planet.orders.models.order_details import OrderDetails
from cast_planet.orders.models.order_notifications import OrderNotifications
from cast_planet.orders.models.order_products import BaseMapsGeometrySource
from cast_planet.orders.models.tools import MergeObject, BasemapClipObject, ReprojectObject
from cast_planet import OrdersApi


class BaseMapAOISearch:
    _basemapApi: BasemapApi
    _ordersApi: OrdersApi

    def __init__(self, api_key: str):
        """
        Initializes the BaseMapAOISearch class by setting up the Orders API and Basemap API instances.

        This class is responsible for interacting with the Planet API for creating basemap orders,
        listing mosaics, and handling the status of orders.

        :param api_key: The API key to authenticate with the Planet API. This key is used for
                        creating sessions in both the Basemap API and Orders API.
        """
        self._ordersApi = OrdersApi(api_key=api_key)
        self._basemapApi = BasemapApi(api_key=api_key)

    def list_mosaics(self):
        """
        Retrieves a list of available mosaics from the Basemap API.

        This method interacts with the Basemap API to fetch all available mosaics. It serves as
        a way to get a collection of mosaics that can later be used to create orders.

        :return: A list of mosaic names or objects as returned by the Basemap API.
        :rtype: List[str]
        """
        return self._basemapApi.list_mosaics()

    def order_mosaic_geojson(self, mosaic_names: List[str], aoi: Union[PolygonModel, MultiPolygonModel],
                             projection: str = None, email_notification: bool = False) -> OrderDetails:
        """
        Creates an order for mosaics based on a provided Area of Interest (AOI) in GeoJSON format,
        with optional projection settings and email notifications.

        This method prepares an order for one or more mosaics based on the given AOI. The order
        can include optional tools such as projection and clipping. If a projection is provided,
        the order is reprojected accordingly. An email notification can be sent to the address
        associated with the API key when the order is complete.

        :param mosaic_names: A list of mosaic names that should be included in the order.
                              Each name corresponds to a basemap mosaic available in the Basemap API.
        :param aoi: The Area of Interest (AOI) in GeoJSON format. This defines the geographic
                    area for which the mosaics are requested.
        :param projection: An optional string that specifies the coordinate reference system
                           (CRS) for the order, such as "EPSG:4326" (WGS84).
        :param email_notification: A boolean flag indicating whether an email notification
                                   should be sent to the address associated with the API key
                                   upon order completion. Default is False.
        :return: An OrderDetails object that contains information about the created order.
        :rtype: OrderDetails
        """
        order_name_id = uuid4()
        products: List[BaseMapsGeometrySource] = list()
        for n in mosaic_names:
            products.append(BaseMapsGeometrySource(mosaic_name=n, geometry=aoi))

        tools = [MergeObject(), BasemapClipObject()]
        if projection is not None:
            tools.append(ReprojectObject(projection=projection))

        request = CreateOrder(
            name=f"Basemap AOI Wizard: {order_name_id}",
            source_type=OrderSource.BASEMAP.value,
            order_type=OrderType.PARTIAL.value,
            products=products,
            tools=tools,
            notifications=OrderNotifications(email=email_notification))

        return self._ordersApi.create_order(request)

    def check_status(self, order: Union[OrderDetails, UUID, str]):
        """
        Checks the status of a specific order, either by its OrderDetails object, UUID, or string ID.

        This method queries the Orders API for the status of a particular order. It can accept
        either an OrderDetails instance, a UUID, or a string ID that represents the order.
        The status returned will reflect the current state of the order, such as whether it is
        queued, processing, or completed.

        :param order: The order identifier, which can be an OrderDetails object, UUID, or string
                      representation of the order ID.
        :return: An OrderStatus object representing the current status of the order.
        :rtype: OrderStatus
        """
        order_id = str(order) if isinstance(order, (str, UUID)) else order.id
        details = self._ordersApi.get_order_details_by_id(order_id)
        return OrderStatus(**details.model_dump())