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

