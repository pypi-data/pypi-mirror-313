# Initialize the TaxService
from cloverapi import CloverApiClient
from cloverapi.helpers.logging_helper import setup_logger
from cloverapi.services.tax_service import TaxServiceBase
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

logger = setup_logger("CloverAPI")

# Fetch API token and Merchant ID from environment variables
API_TOKEN = os.getenv("API_TOKEN")
MERCHANT_ID = os.getenv("MERCHANT_ID")

client = CloverApiClient(auth_token=API_TOKEN, merchant_id=MERCHANT_ID, region="us")
# Initialize the TaxService
tax_services = client.tax_service

# Fetch all tax rates
tax_rates = tax_services.get_tax_rates()

print("Tax Rates:", tax_rates)



