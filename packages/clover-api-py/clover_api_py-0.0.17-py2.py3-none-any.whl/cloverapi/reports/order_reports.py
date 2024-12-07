from typing import Union
from cloverapi.helpers.logging_helper import setup_logger
from cloverapi.helpers.date_helper import DateHelper
from cloverapi.processor.order_processor import OrderData
from cloverapi.services.order_service import OrderServiceBase
from cloverapi.services.cash_service import CashService

logger = setup_logger("OrderReporter")


class OrderReporter:
    def __init__(self, order_service: OrderServiceBase, cash_service: CashService):
        """
        Initialize the OrderReporter.

        :param order_service: Instance of OrderServiceBase to fetch orders.
        :param cash_service: Instance of CashService to fetch cash events.
        """
        self.order_service = order_service
        self.cash_service = cash_service

    def fetch_orders(self, order_type: str, period: Union[str, int] = "day") -> OrderData:
        """
        Fetch orders based on type (open, complete, or all) and wrap the results in an OrderData object.

        :param order_type: Type of orders to fetch ('open', 'complete', or 'all').
        :param period: Reporting period ('day', 'today', 'yesterday', 'week', 'month', 'quarter', 'year', or an integer for last n days).
        :return: An OrderData instance containing the fetched orders.
        """
        filters = []
        if order_type == "open":
            filters.append("state=open")
        elif order_type == "complete":
            filters.append("state=locked")
        elif order_type != "all":
            raise ValueError(f"Invalid order type: {order_type}. Use 'open', 'complete', or 'all'.")

        # Fetch raw orders
        orders = self.order_service.get_orders(filters=filters, period=period)
        if not orders.get("elements"):
            logger.warning(f"No {order_type} orders found for the given period '{period}'.")
            return OrderData({"elements": []})

        return OrderData(raw_orders=orders, service=self.order_service, order_type=order_type)

    def fetch_order_by_id(self, order_id: str) -> OrderData:
        """
        Fetch a single order by its ID and wrap it in an OrderData object.
        :param order_id: The ID of the order to fetch.
        :return: An OrderData object containing the fetched order.
        """
        logger.info(f"Fetching order by ID: {order_id}")
        try:
            # Fetch raw order by ID
            single_order = self.order_service.get_order_by_id(order_id)

            # Return as an OrderData object for further processing
            return single_order
        except Exception as e:
            logger.error(f"Error fetching order by ID {order_id}: {e}")
            return OrderData({"elements": []})

    def cash_report(self, period: Union[str, int] = "day", group_by: str = "day") -> dict:  # Changed default to "day"
        """
        Generate a report for cash transactions, grouped by the specified period.

        :param period: Reporting period ('day', 'today', 'yesterday', 'week', 'month', 'quarter', 'year', or an integer for last n days).
        :param group_by: Grouping option ('day', 'week', 'quarter', 'year').
        :return: Summarized cash transaction data.
        """
        try:
            # Fetch cash events
            cash_events_response = self.cash_service.get_cash_events(period=period)
            cash_events = cash_events_response.get("elements", [])
            if not cash_events:
                logger.warning(f"No cash transactions found for the period '{period}'.")
                return {}

            # Process and summarize cash events
            summary = self.cash_service.summarize_cash_events(cash_events)
            grouped_data = DateHelper.group_by_period(
                cash_events, group_by=group_by, date_key="timestamp"
            )

            # Add time range for the report
            start_time, end_time = DateHelper.filters_period(period)

            return {
                "summary": summary,
                "start_time": DateHelper.ms_to_date(start_time),
                "end_time": DateHelper.ms_to_date(end_time),
                "grouped_data": grouped_data,
            }
        except Exception as e:
            logger.error(f"Error generating cash report: {e}")
            return {"error": str(e)}