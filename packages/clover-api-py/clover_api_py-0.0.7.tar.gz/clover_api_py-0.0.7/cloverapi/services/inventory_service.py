from cloverapi.helpers.http_helper import HttpServiceBase
from cloverapi.helpers.logging_helper import setup_logger
from typing import Union, Dict

# Setup logger for InventoryService
logger = setup_logger("InventoryService")


class InventoryService(HttpServiceBase):

    def get_all_inventory(self, offset=0, limit=100, filter=None, expand=None):
        """
        Retrieve all inventory items with optional filters.

        :param offset: Pagination offset.
        :param limit: Number of items per request.
        :param filter: Filter criteria for items.
        :param expand: Additional details to expand in response.
        :return: List of all inventory items.
        """
        params = {'offset': offset, 'limit': limit}
        if filter:
            params['filter'] = filter
        if expand:
            params['expand'] = expand

        logger.info("Fetching all inventory items...")
        return self._get_data("items", params)

    def get_item_detail(self, item_id: str, expand: str = None) -> dict:
        """
        Fetch details for a specific inventory item by its ID.

        :param item_id: The ID of the inventory item.
        :param expand: Optional parameter to include additional details (e.g., itemStock).
        :return: Dictionary containing item details.
        """
        logger.info(f"Fetching details for item ID: {item_id} with expansion: {expand}")
        params = {"expand": expand} if expand else {}
        return self._get_data(f"items/{item_id}", params=params, paginated=False)

    def update_item_detail(self, item_id: str, item_data: dict) -> dict:
        """
        Update an existing inventory item.

        :param item_id: The ID of the inventory item to update.
        :param item_data: Dictionary containing the item details to update.
        :return: Updated item details or error message.
        """
        logger.info(f"Updating item ID: {item_id} with data: {item_data}")
        endpoint = f"items/{item_id}"
        return self._post_data(endpoint, item_data)

    def get_item_stock(self, item_id: str) -> Dict:
        """
        Fetch stock details for a specific inventory item by its ID.

        :param item_id: The ID of the inventory item.
        :return: Dictionary containing stock details (stockCount and quantity).
        """
        logger.info(f"Fetching stock details for item ID: {item_id}")
        stock_details = self._get_data(f"item_stocks/{item_id}", paginated=False)
        if stock_details:
            logger.debug(f"Stock details fetched: {stock_details}")
        else:
            logger.warning(f"No stock details found for item ID: {item_id}")
        return stock_details

    def update_item_stock(self, item_id: str, stock_count: int):
        """
        Update the stock count for a specific item.

        :param item_id: ID of the inventory item.
        :param stock_count: New stock count to set.
        :return: Response from the API.
        """
        logger.info(f"Updating stock for item ID {item_id} to {stock_count}")
        return self._post_data(f"item_stocks/{item_id}", {"quantity": stock_count})