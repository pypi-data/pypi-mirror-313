from typing import List, Dict, Union
from cloverapi.helpers.date_helper import DateHelper


class OrderData:
    """
    Wrapper for raw order data with summarization capabilities.
    """

    def __init__(self, raw_orders: Dict, order_type: str = "all", service=None):
        """
        Initialize the OrderData with raw orders data.

        :param raw_orders: Dictionary containing raw order data fetched from the API.
        :param order_type: The type of order (open, complete, or all).
        """
        self.service = service
        self.raw_orders = raw_orders
        self.order_type = order_type

    def summarize(self, group_by: str = "day", period: Union[str, int] = "day") -> List[Dict]:
        """
        Summarize the raw orders data.

        :param group_by: Grouping period ('day', 'week', 'month', 'quarter', 'year').
        :param period: Reporting period ('day', 'today', 'yesterday', 'week', 'month', 'quarter', 'year', or an integer for last n days).
        :return: List of summaries containing total counts, amounts, and grouped data.
        """
        return OrderProcessor.summarize_orders(
            orders=self.raw_orders,
            group_by=group_by,
            period=period,
            order_type=self.order_type,
        )

    def data(self) -> List[Dict]:
        """
        Retrieve the raw orders data as a list of dictionaries.

        :return: A list of raw order dictionaries.
        """
        return self.raw_orders.get("elements", [])

    def itemized(self) -> List[Dict]:
        """
        Retrieve itemized details for all orders with flattened structure,
        including 'orderRef_id', 'item_id', and a calculated 'quantity' field.

        :return: List of itemized details with flattened structure and all metadata.
        """
        detailed_items = []

        for order in self.raw_orders.get("elements", []):
            order_id = order.get("id")
            order_created_time = order.get("createdTime")
            employee_id = order.get("employee", {}).get("id", "unknown")
            device_id = order.get("device", {}).get("id", "unknown")

            if not order_id:
                continue

            # Fetch line items for the order
            line_items = self.service.get_line_items_by_order(order_id)

            # Track occurrences of each item to calculate quantity
            item_counts = {}
            for item in line_items.get("elements", []):
                item_id = item.get("item", {}).get("id", "unknown")
                if item_id in item_counts:
                    item_counts[item_id] += 1
                else:
                    item_counts[item_id] = 1

            for item in line_items.get("elements", []):
                # Flatten 'orderRef' and 'item' fields
                flattened_item = {
                    "order_id": order_id,
                    "order_created_time": order_created_time,
                    "employee_id": employee_id,
                    "device_id": device_id,
                    "orderRef_id": item.get("orderRef", {}).get("id", "unknown"),
                    "item_id": item.get("item", {}).get("id", "unknown"),
                    "quantity": item_counts[item.get("item", {}).get("id", "unknown")],
                }

                # Add all remaining fields from the line item
                for key, value in item.items():
                    if key not in ["orderRef", "item"]:  # Exclude nested fields already flattened
                        flattened_item[key] = value

                # Add the flattened item to the list
                detailed_items.append(flattened_item)

        return detailed_items


class OrderProcessor:
    """
    Processing layer to handle data aggregation, grouping, and calculations for orders.
    """

    @staticmethod
    def aggregate_orders(orders: Dict) -> Dict[str, int]:
        """
        Aggregate orders to calculate total count and total amount.

        :param orders: Dictionary of raw orders fetched from the API.
        :return: Dictionary with total count and total amount.
        """
        elements = orders.get("elements", [])
        total_count = len(elements)
        total_amount = sum(order.get("total", 0) for order in elements)

        return {"total_count": total_count, "total_amount": total_amount}

    @staticmethod
    def group_orders(orders: Dict, group_by: str = "day") -> Dict:
        """
        Group orders by a specified period (day, week, month, etc.).

        :param orders: Dictionary of raw orders fetched from the API.
        :param group_by: Grouping period ('day', 'week', 'month', 'quarter', 'year').
        :return: Dictionary grouped by the specified period.
        """
        elements = orders.get("elements", [])
        grouped = DateHelper.group_by_period(
            data=elements,
            group_by=group_by,
            date_key="createdTime",
            value_key="total"
        )
        return grouped

    @staticmethod
    def summarize_orders(
            orders: Dict,
            group_by: str = "day",
            period: Union[str, int] = "weekly",
            order_type: str = "all"
    ) -> List[Dict]:
        """
        Summarize orders with aggregation and grouping.

        :param orders: Dictionary of raw orders fetched from the API.
        :param group_by: Grouping period ('day', 'week', 'month', 'quarter', 'year').
        :param period: Reporting period ('day', 'today', 'yesterday', 'week', 'month', 'quarter', 'year', or an integer for last n days).
        :param order_type: The type of order (open, complete, or all).
        :return: List of summaries containing order_type, total_amount, total_count, and event_date.
        """
        # Group and aggregate orders
        grouped_data = OrderProcessor.group_orders(orders, group_by)

        # Prepare the summary list
        summary = []
        for event_key, data in grouped_data.items():
            event_date_field = OrderProcessor.get_event_date_name(group_by)
            summary.append({
                "order_type": order_type,
                "total_amount": data["total_amount"] / 100,  # Convert cents to dollars
                "total_count": data["total_count"],
                event_date_field: event_key
            })

        return summary

    @staticmethod
    def get_event_date_name(group_by: str) -> str:
        """
        Generate the dynamic field name for the grouped date.

        :param group_by: Grouping type ('day', 'week', 'month', etc.).
        :return: Dynamic field name for the event date.
        """
        field_mapping = {
            "day": "event_date",
            "week": "event_week",
            "month": "event_month",
            "quarter": "event_quarter",
            "year": "event_year"
        }
        return field_mapping.get(group_by, "event_date")


