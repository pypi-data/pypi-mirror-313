from cloverapi import CloverApiClient
from cloverapi.reports.cash_reports import CashReporter
from cloverapi.reports.order_reports import OrderReporter
from cloverapi.services.order_service import OrderServiceBase
from cloverapi.services.cash_service import CashService
from cloverapi.cloverapi_auth import CloverApiAuth
from cloverapi.helpers.logging_helper import setup_logger
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

logger = setup_logger("CloverAPI")

# Fetch API token and Merchant ID from environment variables
API_TOKEN = os.getenv("API_TOKEN")
MERCHANT_ID = os.getenv("MERCHANT_ID")
#
try:
#     # Initialize authentication and services
    client = CloverApiClient(auth_token=API_TOKEN, merchant_id=MERCHANT_ID, region="us")
#
#     # Initialize reporter
    order_reporter = client.order_report
    service = client.order_service
#
#     # ddp = order_reporter.fetch_order_by_id(order_id="DNBHSQZD4DW08")
#     # print(ddp.data())
#
#     service = order_serv.get_order_by_id(order_id="DNBHSQZD4DW08")
#     print(service)
    period="month"
    group_by="day"
#     # # Fetch open orders for the day
    saved_orders = order_reporter.fetch_orders(order_type="open", period=period)
    orders_sum = saved_orders.summarize(group_by=group_by)
    # for i in (orders_sum):
    #     print(i)
    #     break
#
#
#     # order_ser = client.order_service
#     # dd = order_ser.get_order_by_id("D4KHKB33V70WP").itemized()
#     # print(dd)
# # Cash
#
    cash_reporter = client.cash_service
    cash_orders = cash_reporter.get_cash_events(period=period)
    print(cash_orders.summarize())
#     # print(cash_orders.summarize(group_by=group_by))
#     # for order in cash_orders.summarize(group_by="day"):
#     #     print(order)
#     #     break
#     #
#     #
#     # # Summarize the fetched cash events grouped by day
#     # cash_summary = cash_orders.summarize(group_by="day")
#     # Example Output
#     # for record in cash_summary:
#     #     print(record)
#
except Exception as e:
    logger.error(f"An error occurred: {e}")

