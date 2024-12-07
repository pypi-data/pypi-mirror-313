from cloverapi.helpers.http_helper import HttpServiceBase
from cloverapi.helpers.logging_helper import setup_logger
from cloverapi.helpers.date_helper import DateHelper
from cloverapi.processor.cash_processor import CashData

logger = setup_logger("CashService")


class CashService(HttpServiceBase):
    def get_cash_events(self, period=None, date_range='day'):
        """
        Fetch all cash events for the merchant, optionally filtered by a period or a date range.

        :param period: Reporting period (e.g., 'daily', 'weekly', 'monthly', etc.).
        :param date_range: Tuple of (start_time, end_time) in milliseconds.
        :return: JSON response containing cash events.
        """
        # Validate date range or period
        if period:
            start_time, end_time = DateHelper.filters_period(period)
        elif date_range:
            start_time, end_time = date_range
        else:
            raise ValueError("Either 'period' or 'date_range' must be provided.")

        # Prepare query parameters
        params = {
            "filter": [
                f"timestamp>={start_time}",
                f"timestamp<={end_time}"
            ]
        }

        logger.info(f"Fetching cash events for period: {period}, date_range: {start_time}-{end_time}")
        raw_cash_events = self._get_data("cash_events", params=params)

        # Return a CashData object for easier summarization
        return CashData(raw_cash_events)

    @staticmethod
    def summarize_cash_events(cash_events):
        """
        Summarize cash events to calculate totals for added, removed, and net cash.

        :param cash_events: List of cash event dictionaries.
        :return: Dictionary with total added, removed, and net cash.
        """
        total_added = sum(
            event.get("amount", 0) for event in cash_events if event.get("eventType") == "ADD_CASH"
        )
        total_removed = sum(
            event.get("amount", 0) for event in cash_events if event.get("eventType") == "REMOVE_CASH"
        )
        net_cash = total_added - total_removed

        logger.info(
            f"Summarized cash events: Total Added: {total_added}, Total Removed: {total_removed}, Net Cash: {net_cash}"
        )

        return {
            "total_added": total_added,
            "total_removed": total_removed,
            "net_cash": net_cash,
        }

    def get_cash_event_report(self, period=None, date_range=None):
        """
        Fetch and summarize cash events for a specific period or custom date range.

        :param period: Reporting period ('daily', 'weekly', 'monthly', etc.).
        :param date_range: Tuple of (start_time, end_time) in milliseconds.
        :return: Dictionary with summarized cash events and raw data.
        """
        # Fetch cash events
        cash_events_response = self.get_cash_events(period=period, date_range=date_range)

        # Extract the list of cash events
        cash_events = cash_events_response.get("elements", [])

        # Summarize the cash events
        summary = self.summarize_cash_events(cash_events)

        # Add date range information to the summary
        if period:
            start_time, end_time = DateHelper.filters_period(period)
        else:
            start_time, end_time = date_range

        summary.update({
            "start_time": DateHelper.ms_to_date(start_time),
            "end_time": DateHelper.ms_to_date(end_time),
            "events": cash_events,
        })

        return summary