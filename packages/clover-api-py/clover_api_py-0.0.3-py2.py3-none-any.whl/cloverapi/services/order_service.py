from cloverapi.helpers.http_helper import HttpServiceBase
from cloverapi.helpers.logging_helper import setup_logger
from cloverapi.helpers.date_helper import DateHelper
from cloverapi.processor.order_processor import OrderData

# Setup logger for OrderService
logger = setup_logger("OrderService")

class OrderServiceBase(HttpServiceBase):
    def get_orders(self, filters=None, offset=0, limit=100, period=None, open_only=False):
        """
        Retrieve orders with optional filters, limiting results to a specific time range.

        :param period:
        :param filters: List of filter strings, e.g., ["total>1000", "payType!=FULL"].
        :param offset: Pagination offset.
        :param limit: Number of records per request.
        :param period: Time period for filtering orders (e.g., 'daily', 'weekly', 7 for last 7 days, etc.)
        :param open_only: Boolean to filter only open orders.
        :return: List of orders.
        """
        if filters is None:
            filters = []

        # Apply the date range filter
        if period:
            start, end = DateHelper.filters_period(period)
            filters.append(f"createdTime>={start}")
            filters.append(f"createdTime<={end}")

        # Add filter for open orders if requested
        if open_only:
            filters.append("state=open")


        params = {'offset': offset, 'limit': limit, 'filter': filters}

        logger.info(f"Fetching orders with filters: {filters}")
        return self._get_data("orders", params)

    def create_order(self, order_data):
        """
        Create a new order.
        :param order_data: Order details as a dictionary.
        :return: Created order details.
        """
        logger.info(f"Creating a new order: {order_data}")
        return self._post_data("orders", order_data)

    def get_order_by_id(self, order_id):
        """
        Retrieve details for a specific order.
        :param order_id: Order ID.
        :return: Order details.
        """
        logger.info(f"Fetching order with ID: {order_id}")
        return self._get_data(f"orders/{order_id}")

    def update_order_by_id(self, order_id, order_data):
        """
        Update an existing order.
        :param order_id: Order ID.
        :param order_data: Updated order details.
        :return: Updated order details.
        """
        logger.info(f"Updating order {order_id} with data: {order_data}")
        return self._post_data(f"orders/{order_id}", order_data)

    def delete_order_by_id(self, order_id):
        """
        Delete a specific order.
        :param order_id: Order ID.
        :return: Response from delete operation.
        """
        logger.warning(f"Deleting order with ID: {order_id}")
        return self._delete_data(f"orders/{order_id}")

    def get_discounts_for_order(self, order_id):
        """
        Retrieve discounts for a specific order.
        :param order_id: Order ID.
        :return: List of discounts.
        """
        logger.info(f"Fetching discounts for order ID: {order_id}")
        return self._get_data(f"orders/{order_id}/discounts")

    def create_discount_for_order(self, order_id, discount_data):
        """
        Add a discount to a specific order.
        :param order_id: Order ID.
        :param discount_data: Discount details.
        :return: Created discount response.
        """
        logger.info(f"Creating discount for order ID: {order_id} with data: {discount_data}")
        return self._post_data(f"orders/{order_id}/discounts", discount_data)

    def delete_discount_for_order(self, order_id, discount_id):
        """
        Remove a discount from a specific order.
        :param order_id: Order ID.
        :param discount_id: Discount ID.
        :return: Response from delete operation.
        """
        logger.warning(f"Deleting discount ID: {discount_id} for order ID: {order_id}")
        return self._delete_data(f"orders/{order_id}/discounts/{discount_id}")

    def get_line_items_by_order(self, order_id):
        """
        Retrieve line items for a specific order.
        :param order_id: Order ID.
        :return: List of line items.
        """
        logger.info(f"Fetching line items for order ID: {order_id}")
        return self._get_data(f"orders/{order_id}/line_items")

    def create_line_item(self, order_id, line_item_data):
        """
        Add a line item to a specific order.
        :param order_id: Order ID.
        :param line_item_data: Line item details.
        :return: Created line item response.
        """
        logger.info(f"Creating line item for order ID: {order_id} with data: {line_item_data}")
        return self._post_data(f"orders/{order_id}/line_items", line_item_data)

    def void_line_item_by_id(self, order_id, line_item_id):
        """
        Void a line item from a specific order.
        :param order_id: Order ID.
        :param line_item_id: Line Item ID.
        :return: Response from delete operation.
        """
        logger.warning(f"Voiding line item ID: {line_item_id} for order ID: {order_id}")
        return self._delete_data(f"orders/{order_id}/line_items/{line_item_id}")

    def create_payment_record_for_order(self, order_id, payment_data):
        """
        Add a payment record to a specific order.
        :param order_id: Order ID.
        :param payment_data: Payment details.
        :return: Created payment response.
        """
        logger.info(f"Creating payment record for order ID: {order_id} with data: {payment_data}")
        return self._post_data(f"orders/{order_id}/payments", payment_data)

    def create_service_charge_for_order(self, order_id, service_charge_data):
        """
        Add a service charge to a specific order.
        :param order_id: Order ID.
        :param service_charge_data: Service charge details.
        :return: Created service charge response.
        """
        logger.info(f"Creating service charge for order ID: {order_id} with data: {service_charge_data}")
        return self._post_data(f"orders/{order_id}/service_charge", service_charge_data)

    def delete_service_charge_for_order(self, order_id, service_charge_id):
        """
        Remove a service charge from a specific order.
        :param order_id: Order ID.
        :param service_charge_id: Service Charge ID.
        :return: Response from delete operation.
        """
        logger.warning(f"Deleting service charge ID: {service_charge_id} for order ID: {order_id}")
        return self._delete_data(f"orders/{order_id}/service_charge/{service_charge_id}")


