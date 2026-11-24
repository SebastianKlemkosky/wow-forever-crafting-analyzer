from market import Market

class Item:
    def __init__(self, item_id: int, name: str) -> None:
        self.item_id = item_id
        self.name = name

    def get_price(self, market: Market) -> int | None:
        item_data = market.get_item_by_id(self.item_id)

        if item_data is None:
            return None

        stats = market.get_item_stats(item_data)

        return stats.get("ask")

    def __repr__(self) -> str:
        return f"Item(id={self.item_id}, name='{self.name}')"



class ItemCatalog:
    def __init__(self) -> None:
        self.items_by_id: dict[int, Item] = {}
        self.items_by_name: dict[str, Item] = {}

    def add_item(self, item_id: int, name: str) -> None:
        item = Item(item_id, name)

        self.items_by_id[item_id] = item
        self.items_by_name[name.lower()] = item

    def get_item_by_id(self, item_id: int) -> Item | None:
        return self.items_by_id.get(item_id)

    def get_item_by_name(self, name: str) -> Item | None:
        return self.items_by_name.get(name.lower())

    def get_item_name(self, item_id: int) -> str | None:
        item = self.get_item_by_id(item_id)

        if item is None:
            return None

        return item.name

    def get_item_id(self, name: str) -> int | None:
        item = self.get_item_by_name(name)

        if item is None:
            return None

        return item.item_id

    def load_market_items(self, items: list[dict]) -> None:
        for item in items:
            self.add_item(item["id"], item["name"])
