import pandas as pd
from typing import List, Dict, Union
from datetime import datetime
from cloverapi.helpers.date_helper import DateHelper
from cloverapi.helpers.http_helper import logger


class CashData:
    """
    Wrapper for raw cash data with summarization and cleaning capabilities.
    """

    def __init__(self, raw_cash_events: Dict, cash_type: str = "cash"):
        """
        Initialize the CashData with raw cash events' data.

        :param raw_cash_events: Dictionary containing raw cash events fetched from the API.
        :param cash_type: The type of cash event (e.g., cash).
        """
        self.raw_cash_events = raw_cash_events
        self.cash_type = cash_type

    def clean(self) -> List[Dict]:
        """
        Clean the raw cash events data for easier processing.

        :return: A list of cleaned cash event dictionaries.
        """
        return CashProcessor.clean_cash_events(self.raw_cash_events)

    def summarize(self, group_by: str = "day", period: Union[str, int] = "day") -> List[Dict]:
        """
        Summarize the cleaned cash events data.

        :param group_by: Grouping period ('day', 'week', 'month', 'quarter', 'year').
        :param period: Reporting period ('day', 'today', 'yesterday', 'week', 'month', 'quarter', 'year').
        :return: List of summaries containing total counts, amounts, and grouped data.
        """
        return CashProcessor.summarize_cash_events(
            cash_events=self.raw_cash_events,
            group_by=group_by,
            period=period,
            cash_type=self.cash_type,
        )

    def data(self) -> List[Dict]:
        """
        Retrieve the cleaned cash events data as a list of dictionaries.

        :return: A list of cleaned cash event dictionaries.
        """
        return CashProcessor.clean_cash_events(self.raw_cash_events)


class CashProcessor:
    """
    Processing layer to handle data aggregation, grouping, and calculations for cash events.
    """

    @staticmethod
    def clean_cash_event(event: Dict) -> Dict:
        """
        Clean and transform a raw cash event into a structured format.

        :param event: Raw cash event dictionary.
        :return: Cleaned cash event dictionary.
        """
        raw_timestamp = event.get("timestamp", 0)

        return {
            "type": event.get("type"),
            "amountChange": event.get("amountChange", 0) / 100,  # Convert cents to dollars
            "timestamp": raw_timestamp,  # Keep raw UNIX timestamp in milliseconds for grouping
            "readable_timestamp": datetime.fromtimestamp(raw_timestamp / 1000) if isinstance(raw_timestamp, int) else None,  # Human-readable format
            "order_id": CashProcessor.extract_order_id(event.get("note", "")),
            "employee_id": event.get("employee", {}).get("id"),
            "device_id": event.get("device", {}).get("id"),
            "cash_type": "cash",
        }

    @staticmethod
    def extract_order_id(note: str) -> str:
        """
        Extract the Payment ID or Order ID from the note field.

        :param note: Note field from the cash event.
        :return: Extracted Payment ID or Order ID, or None if not present.
        """
        if "Payment ID:" in note:
            return note.split("Payment ID:")[1].split("\n")[0].strip()
        elif "Order ID:" in note:
            return note.split("Order ID:")[1].split("\n")[0].strip()
        return None

    @staticmethod
    def clean_cash_events(raw_cash_events: Dict) -> List[Dict]:
        """
        Clean and transform a list of raw cash events.

        :param raw_cash_events: Dictionary containing raw cash events.
        :return: List of cleaned cash event dictionaries.
        """
        elements = raw_cash_events.get("elements", [])
        return [CashProcessor.clean_cash_event(event) for event in elements]

    @staticmethod
    def group_cash_events(cleaned_cash_events: List[Dict], group_by: str = "day") -> Dict:
        """
        Group cleaned cash events by a specified period (day, week, month, etc.).

        :param cleaned_cash_events: List of cleaned cash event dictionaries.
        :param group_by: Grouping period ('day', 'week', 'month', 'quarter', 'year').
        :return: Dictionary grouped by the specified period.
        """
        # Group using raw UNIX timestamp
        for event in cleaned_cash_events:
            # Replace readable timestamp with raw UNIX timestamp for grouping
            event["timestamp"] = event.get("timestamp")  # Ensure compatibility

        return DateHelper.group_by_period(
            data=cleaned_cash_events,
            group_by=group_by,
            date_key="timestamp",
            value_key="amountChange"  # Use amountChange for calculations
        )

    @staticmethod
    def summarize_cash_events(
        cash_events: Dict,
        group_by: str = "day",
        period: Union[str, int] = "daily",
        cash_type: str = "cash",
    ) -> List[Dict]:
        """
        Summarize cash events with aggregation and grouping.

        :param cash_events: Dictionary of raw cash events fetched from the API.
        :param group_by: Grouping period ('day', 'week', 'month', 'quarter', 'year').
        :param period: Reporting period ('day', 'today', 'yesterday', 'week', 'month', 'quarter', 'year').
        :param cash_type: The type of cash event (e.g., cash).
        :return: List of summaries containing cash_type, total_amount, total_count, and event_date.
        """
        # Clean the raw cash events
        cleaned_events = CashProcessor.clean_cash_events(cash_events)
        if not cleaned_events:
            logger.warning("No cleaned events available for summarization.")
            return []

        # Group cleaned cash events
        grouped_data = CashProcessor.group_cash_events(cleaned_events, group_by)

        # Prepare the summary list
        summary = []
        for event_key, data in grouped_data.items():
            event_date_field = CashProcessor.get_event_date_name(group_by)
            summary.append({
                "order_type": cash_type,
                "total_amount": data["total_amount"],  # Already in dollars
                "total_count": data["total_count"],
                event_date_field: datetime.fromtimestamp(event_key / 1000) if isinstance(event_key, int) else event_key,  # Convert back to readable datetime
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