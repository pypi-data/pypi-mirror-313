from typing import Union
from cloverapi.helpers.logging_helper import setup_logger
from cloverapi.processor.cash_processor import CashData, CashProcessor
from cloverapi.services.cash_service import CashService

logger = setup_logger("CashReporter")


class CashReporter:
    def __init__(self, cash_service: CashService):
        """
        Initialize the CashReporter.

        :param cash_service: Instance of CashService to fetch cash events.
        """
        self.cash_service = cash_service

    def fetch_cash_orders(self, period: Union[str, int] = "day") -> CashData:
        """
        Fetch cash events for the specified period and wrap the results in a CashData object.

        :param period: Reporting period ('day', 'week', 'month', 'quarter', 'year').
        :return: A CashData instance containing the fetched cash events.
        """
        # Fetch raw cash events
        cash_events = self.cash_service.get_cash_events(period=period)
        if not cash_events.get("elements"):
            logger.warning(f"No cash events found for the given period '{period}'.")
            return CashData({"elements": []})

        return CashData(raw_cash_events=cash_events)

    def generate_summary(
        self,
        period: Union[str, int] = "day",
        group_by: str = "day",
        export_csv: bool = False,
        file_name: str = "cash_summary.csv",
    ) -> list:
        """
        Fetch, summarize, and optionally export a summary of cash events.

        :param period: Reporting period ('day', 'week', 'month', 'quarter', 'year').
        :param group_by: Grouping period ('day', 'week', 'month', 'quarter', 'year').
        :param export_csv: Whether to export the summary to a CSV file.
        :param file_name: Name of the CSV file to create if export_csv is True.
        :return: A list of summarized cash events.
        """
        # Fetch cash events
        logger.info(f"Fetching cash events for period: {period}")
        cash_data = self.fetch_cash_orders(period=period)

        # Summarize events
        summary = cash_data.summarize(group_by=group_by, period=period)

        # Optionally export the summary
        if export_csv:
            logger.info(f"Exporting summary to {file_name}")
            CashProcessor.export_to_csv(summary, file_name=file_name)

        return summary