# clover-api-py

[![PyPI version](https://badge.fury.io/py/clover-py.svg)](https://badge.fury.io/py/clover-py)  
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)  

An unofficial Python client for the Clover API v3. This library enables seamless interaction with the Clover API for managing inventory, orders, taxes, cash transactions, and more.

---

## Features

- Fetch inventory details and stock levels.
- Update inventory items, including names, SKUs, and prices.
- Manage orders and summarize order data.
- Fetch and manage cash transactions.
- Retrieve tax rates and other merchant-specific details.
- Handles API pagination automatically for large datasets.

---

## Installation

Install the package using pip:

```bash
pip install clover-api-py
```

---

## Usage

### Initialize the Client

To get started, initialize the client with your Clover API credentials.

```python
from cloverapi.cloverapi_client import CloverApiClient

# Your Clover API credentials
API_TOKEN = "your_api_token"
MERCHANT_ID = "your_merchant_id"
REGION = "us"  # Options: 'us', 'ca', 'eu', 'latam'

# Initialize the Clover API Client
client = CloverApiClient(auth_token=API_TOKEN, merchant_id=MERCHANT_ID, region=REGION)
```

---

## Supported Regions

When initializing the client, specify the `region` parameter:

| Region         | Code   | Base URL                   |
|----------------|--------|----------------------------|
| United States  | `us`   | https://api.clover.com     |
| Canada         | `ca`   | https://ca.api.clover.com  |
| Europe         | `eu`   | https://eu.api.clover.com  |
| Latin America  | `latam`| https://latam.api.clover.com|

---

### Examples

#### Fetch All Inventory Items

```python
inventory_items = client.inventory_service.get_all_inventory()
for item in inventory_items.get("elements", []):
    print(item)
```

#### Fetch Details for a Specific Item

```python
item_id = "ITEM_ID"
item_details = client.inventory_service.get_item_detail(item_id)
print(item_details)
```

#### Update Item Details

```python
item_id = "ITEM_ID"
updated_item = client.inventory_service.update_item_detail(
    item_id,
    name="Updated Item Name",
    sku="NEW_SKU123",
    price=1500  # Price in cents (e.g., $15.00)
)
print(updated_item)
```

#### Retrieve Item Stock

```python
item_id = "ITEM_ID"
item_stock = client.inventory_service.get_item_stock(item_id)
print(item_stock)
```

#### Update Item Stock

```python
item_id = "ITEM_ID"
new_stock = client.inventory_service.update_item_stock(item_id, stock_count=20)
print(new_stock)
```

#### Fetch Tax Rates

```python
tax_rates = client.tax_service.get_tax_rates()
for tax in tax_rates.get("elements", []):
    print(tax)
```

---

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push to your branch (`git push origin feature-name`).
5. Create a pull request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
