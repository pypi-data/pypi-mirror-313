from cloverapi.helpers.http_helper import HttpServiceBase
from cloverapi.reports.cash_reports import CashReporter
from cloverapi.services.merchant_service import MerchantService
from cloverapi.services.cash_service import CashService
from cloverapi.services.customer_service import CustomerService
from cloverapi.services.employee_service import EmployeeService
from cloverapi.services.inventory_service import InventoryService
from cloverapi.services.notification_service import NotificationService
from cloverapi.services.order_service import OrderServiceBase
from cloverapi.services.payment_service import PaymentService
from cloverapi.services.app_service import AppService
from cloverapi.services.tax_service import TaxServiceBase
from cloverapi.reports.order_reports import OrderReporter
from cloverapi.helpers.logging_helper import setup_logger

logger = setup_logger("CloverApiClient")


class CloverApiClient:
    BASE_URLS = {
        "us": "https://api.clover.com",
        "sandbox": "https://apisandbox.dev.clover.com",
        "ca": "https://api.clover.ca",
        "eu": "https://api.clover.eu",
        "latam": "https://api.clover.latam",
    }
    def __init__(self, auth_token, merchant_id, region: str = "us"):
        """
        Initialize the Clover API client with authentication, merchant ID, and region.

        :param auth_token: API authentication token.
        :param merchant_id: Merchant ID.
        :param region: Region for the API base URL (default: "us").
        """
        if region not in self.BASE_URLS:
            raise ValueError(f"Invalid region '{region}'. Valid regions are: {list(self.BASE_URLS.keys())}")
        self.url = self.BASE_URLS[region]
        self.merchant_id = merchant_id
        self.headers = {"Authorization": f"Bearer {auth_token}"}

        logger.info(f"Initializing CloverApiClient for region: {region}, merchant ID: {merchant_id}")

        # services
        self.merchant_service = MerchantService(self.headers, self.url, self.merchant_id)
        self.cash_service = CashService(self.headers, self.url, self.merchant_id)
        self.customer_service = CustomerService(self.headers, self.url, self.merchant_id)
        self.employee_service = EmployeeService(self.headers, self.url, self.merchant_id)
        self.inventory_service = InventoryService(self.headers, self.url, self.merchant_id)
        self.notification_service = NotificationService(self.headers, self.url, self.merchant_id)
        self.order_service = OrderServiceBase(self.headers, self.url, self.merchant_id)
        self.payment_service = PaymentService(self.headers, self.url, self.merchant_id)
        self.app_service = AppService(self.headers, self.url, self.merchant_id)
        self.tax_service = TaxServiceBase(self.headers, self.url, self.merchant_id)

        # reporters
        self.order_report = OrderReporter(self.order_service, self.cash_service)


    def get_service(self, service_name: str):
        """
        Dynamically fetch a service by its name.

        :param service_name: Name of the service (e.g., 'inventory_service').
        :return: The service instance.
        """
        service = getattr(self, service_name, None)
        if service is None:
            logger.error(f"Service '{service_name}' does not exist.")
            raise ValueError(f"Service '{service_name}' is not available.")
        return service