from typing import List, Dict


class InventoryProcessor:
    """
    Processor to handle data aggregation, cleaning, and summarization for inventory.
    """

    @staticmethod
    def clean_inventory_item(item: Dict) -> Dict:
        """
        Clean and normalize an inventory item.

        :param item: Raw inventory item dictionary.
        :return: Cleaned inventory item dictionary.
        """
        return {
            "id": item.get("id"),
            "name": item.get("name"),
            "price": item.get("price", 0) / 100,  # Convert cents to dollars
            "stock": item.get("stockCount", 0),
            "category_id": item.get("category", {}).get("id"),
            "tag_ids": [tag.get("id") for tag in item.get("tags", [])],
        }

    @staticmethod
    def clean_inventory_items(raw_items: List[Dict]) -> List[Dict]:
        """
        Clean and normalize a list of inventory items.

        :param raw_items: List of raw inventory item dictionaries.
        :return: List of cleaned inventory item dictionaries.
        """
        return [InventoryProcessor.clean_inventory_item(item) for item in raw_items]

    @staticmethod
    def summarize_inventory(items: List[Dict]) -> Dict:
        """
        Summarize inventory items by calculating total stock and average price.

        :param items: List of cleaned inventory item dictionaries.
        :return: Summary dictionary with total stock, average price, and item count.
        """
        total_stock = sum(item.get("stock", 0) for item in items)
        total_value = sum(item.get("price", 0) * item.get("stock", 0) for item in items)
        item_count = len(items)
        avg_price = total_value / total_stock if total_stock > 0 else 0

        return {
            "total_stock": total_stock,
            "total_value": total_value,
            "average_price": avg_price,
            "item_count": item_count,
        }

