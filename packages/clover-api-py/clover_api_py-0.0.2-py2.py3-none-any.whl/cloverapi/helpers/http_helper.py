import requests
from cloverapi.helpers.logging_helper import setup_logger

# Create a logger for the BaseService
logger = setup_logger("BaseService")


class HttpServiceBase:
    def __init__(self, headers: dict, base_url, merchant_id):
        """
        Initialize the HttpServiceBase.

        :param api_authorization: Authorization token as a string (e.g., "Bearer YOUR_API_KEY").
        :param base_url: API base URL (e.g., "https://api.clover.com").
        :param merchant_id: Merchant ID for the Clover API.
        """
        self.url = f"{base_url.rstrip('/')}/v3/merchants/{merchant_id}"
        self.headers = headers

    def _get_data(self, endpoint: str, params: dict = None, limit: int = 100, paginated: bool = True) -> dict:
        """
        Generic GET method to handle both paginated and non-paginated API responses.

        :param endpoint: API endpoint to call (relative to "/v3/merchants/{MERCHANT_ID}").
        :param params: Query parameters for the request.
        :param limit: Number of records per page (default: 100).
        :param paginated: Whether the endpoint uses pagination (default: True).
        :return: Dictionary containing all data retrieved.
        """
        offset = 0
        all_data = []

        while True:
            payload = params or {}
            # Add pagination parameters if the endpoint supports pagination
            if paginated:
                payload.update({"offset": offset, "limit": limit})
            full_url = f"{self.url}/{endpoint}"
            logger.debug(f"GET Request to: {full_url}")
            logger.debug(f"Headers: {self.headers}")
            logger.debug(f"Payload: {payload}")

            response = requests.get(full_url, headers=self.headers, params=payload, timeout=30)
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response body: {response.text}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    logger.debug(f"Parsed JSON response: {data}")

                    if paginated:
                        if isinstance(data, dict):
                            elements = data.get("elements", [])
                            all_data.extend(elements)
                            logger.debug(f"Fetched {len(elements)} records (offset: {offset}, limit: {limit})")

                            # Check if more data exists
                            if len(elements) < limit:
                                break
                            offset += limit
                        else:
                            logger.error(f"Unexpected response format for paginated call: {data}")
                            break
                    else:
                        return data  # For single-object endpoints
                except ValueError:
                    logger.error(f"Failed to parse JSON response: {response.text}")
                    break
            else:
                logger.error(f"Failed GET {endpoint}: {response.status_code} - {response.text}")
                break

        return {"elements": all_data} if paginated else all_data

    def _post_data(self, endpoint: str, payload: dict) -> dict:
        """
        Generic POST method for Clover API.

        :param endpoint: API endpoint to call.
        :param payload: JSON payload to send in the request.
        :return: JSON response or error message.
        """
        full_url = f"{self.url}/{endpoint}"
        logger.debug(f"POST Request to: {full_url}")
        logger.debug(f"Headers: {self.headers}")
        logger.debug(f"Payload: {payload}")

        try:
            response = requests.post(full_url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            logger.info(f"POST request successful for {endpoint}: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"POST request to {endpoint} failed: {e}")
            return {}

    def _put_data(self, endpoint: str, payload: dict) -> dict:
        """
        Generic PUT method for Clover API.

        :param endpoint: API endpoint to call.
        :param payload: JSON payload to send in the request.
        :return: JSON response or error message.
        """
        full_url = f"{self.url}/{endpoint}"
        logger.debug(f"PUT Request to: {full_url}")
        logger.debug(f"Headers: {self.headers}")
        logger.debug(f"Payload: {payload}")

        try:
            response = requests.put(full_url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            logger.info(f"PUT request successful for {endpoint}: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"PUT request to {endpoint} failed: {e}")
            return {}

    def _delete_data(self, endpoint: str) -> dict:
        """
        Generic DELETE method for Clover API.

        :param endpoint: API endpoint to call.
        :return: JSON response or error message.
        """
        full_url = f"{self.url}/{endpoint}"
        logger.debug(f"DELETE Request to: {full_url}")
        logger.debug(f"Headers: {self.headers}")

        try:
            response = requests.delete(full_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            logger.info(f"DELETE request successful for {endpoint}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"DELETE request to {endpoint} failed: {e}")
            return {}