from cloverapi.helpers.http_helper import HttpServiceBase
from cloverapi.helpers.logging_helper import setup_logger

# Setup logger for TaxService
logger = setup_logger("TaxService")

class TaxServiceBase(HttpServiceBase):
    """
    Service for managing and retrieving tax rates from the Clover API.
    """

    def get_tax_rates(self, offset: int = 0, limit: int = 100) -> dict:
        """
        Retrieve all tax rates for the merchant with pagination support.

        :param offset: Pagination offset.
        :param limit: Number of records per request.
        :return: Dictionary containing tax rates.
        """
        logger.info("Fetching all tax rates.")
        return self._get_data("tax_rates", params={"offset": offset, "limit": limit})

    def associate_tax_to_item(self, item_id, tax_rate_id):
        """
        Associate a tax rate with an item.
        :param item_id: ID of the item.
        :param tax_rate_id: ID of the tax rate to associate.
        :return: Response from the API.
        """
        logger.info(f"Associating tax rate {tax_rate_id} with item {item_id}.")
        endpoint = f"items/{item_id}/tax_rates"
        payload = {"id": tax_rate_id}
        return self._post_data(endpoint, payload)

    def disassociate_tax_from_item(self, item_id, tax_rate_id):
        """
        Disassociate a tax rate from an item.
        :param item_id: ID of the item.
        :param tax_rate_id: ID of the tax rate to disassociate.
        :return: Response from the API.
        """
        logger.info(f"Disassociating tax rate {tax_rate_id} from item {item_id}.")
        endpoint = f"items/{item_id}/tax_rates/{tax_rate_id}"
        return self._delete_data(endpoint)

    def get_taxes_by_item(self, item_id):
        """
        Retrieve taxes associated with a specific item.
        :param item_id: ID of the item.
        :return: List of tax rates.
        """
        logger.info(f"Fetching tax rates for item {item_id}.")
        endpoint = f"items/{item_id}/tax_rates"
        return self._get_data(endpoint)