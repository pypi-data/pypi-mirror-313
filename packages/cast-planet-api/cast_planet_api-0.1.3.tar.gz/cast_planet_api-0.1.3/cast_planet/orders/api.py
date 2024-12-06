from typing import List, Any, Dict, Union
from uuid import UUID

from cast_planet.orders.models.common import OrderSource
from cast_planet.orders.models.order_new import CreateOrder
from cast_planet.orders.models.order_details import OrderDetails, OrderState, ResultState
from cast_planet.orders.models.orders_list import OrdersResponse
from cast_planet.orders.models.orders_stats import OrdersStats
from cast_planet._utils import download_file, BaseApi


class OrdersApi(BaseApi):
    """
    A wrapper for interfacing with the Orders API

    Args:
        api_key: The planet API key for your subscription.
        base_url: ase_url: The base URL of the Planet Data API (default: 'https://api.planet.com/data/v1')
        logging_filepath: If supplied, class will log to file.
        log_level: If supplied, sets the log level for the class. Default logging level is logging.ERROR.
    """
    _page_size = 100

    def __init__(self, api_key: str, base_url: str = "https://api.planet.com/compute/ops", log_filename: str = None):
        super().__init__(api_key=api_key, base_url=base_url, log_filename=log_filename)

    def __gather_orders_from_response__(self, orders_response: OrdersResponse) -> List[OrderDetails]:
        """
        Collects all orders by following 'next' links from the response.

        :param orders_response: The initial response containing orders and pagination links.
        :return: A list of all orders across multiple pages.
        """
        orders: List[OrderDetails] = orders_response.orders
        while orders_response.links.next is not None:
            response_data = self._get(orders_response.links.next)
            orders_response = OrdersResponse(**response_data)
            orders.extend(orders_response.orders)
        return orders

    def list_all_account_orders(self, state: OrderState = None, source_type: OrderSource = None) -> List[OrderDetails]:
        """
        Retrieves a list of all orders with optional filters.

        :param state: Filter by the state of the orders (optional).
        :param source_type: Filter by the source type of the orders (optional).
        :return: A list of order details.
        """
        self._logger.info('Fetching all account orders.')

        request_params = {'source_type': 'all' if source_type is None else source_type.value}
        if state is not None:
            request_params['state'] = state.value

        response_data = self._get('/orders/v2', params=request_params)
        return self.__gather_orders_from_response__(OrdersResponse(**response_data))

    def get_order_details_by_id(self, order_id: Union[UUID, str]) -> OrderDetails:
        """
        Retrieves the details of a specific order by ID.

        :param order_id: The unique identifier of the order.
        :return: Details of the specified order.
        """
        self._logger.info(f'Fetching order details for order ID: {order_id}')
        response_data = self._get(f'/orders/v2/{str(order_id)}')
        return OrderDetails(**response_data)

    def create_order(self, order_information: CreateOrder) -> OrderDetails:
        """
        Creates a new order with the provided information.

        :param order_information: The data required to create the order.
        :return: Details of the newly created order.
        """
        self._logger.info('Creating new order.')
        response_data = self._post('/orders/v2', data=order_information.model_dump())
        return OrderDetails(**response_data)

    def cancel_order(self, order_id: Union[UUID, str]) -> OrderDetails:
        """
        Cancels an existing order.

        :param order_id: The ID of the order to cancel.
        :return: The updated order details after cancellation.
        """
        self._logger.info(f'Canceling order with ID: {order_id}')
        response_data = self._post(f'/orders/v2/{str(order_id)}/cancel')
        return OrderDetails(**response_data)

    def order_stats(self) -> OrdersStats:
        """
        Retrieves statistics about the current orders.

        :return: Statistics on queued and running orders.
        """
        self._logger.info('Fetching order stats.')
        response_data = self._get('/stats/orders/v2')
        return OrdersStats(**response_data)

    def download_order_results(self, order: Union[UUID, str, OrderDetails], folder: str = None) -> List[str]:
        """
        Download the results of an order and save them to the specified folder using the download_file helper.

        :param order: The order whose results to download. Can be an ID, UUID, or OrderDetails object.
        :param folder: The folder to save the downloaded files.
        :return: A list of file paths to the downloaded results.
        """
        if isinstance(order, (str, UUID)):
            order = self.get_order_details_by_id(order)

        if not order.links.results:
            self._logger.info("No results to download.")
            return []

        files = []
        for r in order.links.results:
            if r.delivery != ResultState.SUCCESS:
                self._logger.warning(f'{r.name}: Cannot download result because of {r.delivery} status.')
                continue

            if not r.location:
                self._logger.error(f'Failed to Download. {r.name} has no location.')
                continue

            try:
                local_filename = download_file(self._session, r.location, folder, r.name)
                files.append(local_filename)
            except Exception as e:
                self._logger.error(str(e))

        return files

    def view_api_spec(self) -> Dict[str, Any]:
        """
        Retrieves the OpenAPI specification for the Orders API.

        :return: A dictionary representing the API spec.
        """
        self._logger.info('Fetching OpenAPI spec.')
        return self._get('/spec')
