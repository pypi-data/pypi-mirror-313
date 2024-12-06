from typing import List, Dict
from cloverapi.helpers.logging_helper import setup_logger
from cloverapi.services.inventory_service import InventoryService
from cloverapi.processor.inventory_processor import InventoryProcessor

logger = setup_logger("InventoryReporter")


class InventoryReporter:
    def __init__(self, inventory_service: InventoryService):
        """
        Initialize the InventoryReporter.

        :param inventory_service: Instance of InventoryService.
        """
        self.inventory_service = inventory_service

    def fetch_inventory(self, offset=0, limit=100) -> List[Dict]:
        """
        Fetch inventory items.

        :param offset: Pagination offset.
        :param limit: Number of items per request.
        :return: List of raw inventory items.
        """
        raw_items = self.inventory_service.get_inventory_items(offset=offset, limit=limit)
        return raw_items.get("elements", [])

    def generate_report(
        self,
        offset=0,
        limit=100,
        export_csv: bool = False,
        file_name: str = "inventory_report.csv",
    ) -> Dict:
        """
        Generate a summarized report of inventory items.

        :param offset: Pagination offset.
        :param limit: Number of items per request.
        :param export_csv: Whether to export the report to a CSV file.
        :param file_name: Name of the CSV file to export.
        :return: Summary dictionary.
        """
        logger.info("Fetching inventory items...")
        raw_items = self.fetch_inventory(offset=offset, limit=limit)

        logger.info("Cleaning inventory data...")
        cleaned_items = InventoryProcessor.clean_inventory_items(raw_items)

        logger.info("Summarizing inventory data...")
        summary = InventoryProcessor.summarize_inventory(cleaned_items)

        if export_csv:
            logger.info(f"Exporting inventory data to {file_name}...")
            InventoryProcessor.export_inventory_to_csv(cleaned_items, file_name)

        return summary