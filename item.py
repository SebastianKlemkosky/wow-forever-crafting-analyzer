from market import Market
from config import RECIPE_BASE_URL, API_TIMEOUT
from pathlib import Path
import requests
import json

class Item:
    def __init__(
        self,
        item_id: int,
        name: str,
        icon_url: str | None = None
    ) -> None:

        self.item_id = item_id
        self.name = name
        self.icon_url = icon_url

    @property
    def url(self) -> str:
        return f"{RECIPE_BASE_URL}/items/{self.item_id}"
    
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

    def add_item(
        self,
        item_id: int,
        name: str | None,
        icon_url: str | None = None
    ) -> None:

        if not name:
            print(f"Warning: Item {item_id} has no name.")
            name = f"Item #{item_id}"

        item = Item(item_id, name, icon_url)

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

            item_id = item["id"]

            existing = self.get_item_by_id(item_id)

            if existing is None:
                self.add_item(item_id, item["name"])

            elif existing.name == f"Item #{item_id}" and item.get("name"):

                self.items_by_name.pop(existing.name.lower(), None)

                self.add_item(
                    item_id,
                    item["name"],
                    existing.icon_url
                )


    def fetch_items(
        self,
        manifest: dict,
        item_ids: set[int]
    ) -> None:

        channel = manifest["defaultChannel"]

        dataset = manifest["channels"][channel]["datasets"]["items"]

        url = f"{RECIPE_BASE_URL}/api/data/v1/{dataset}/enUS/items"

        ids = sorted(item_ids)
        batch_size = 50

        self.items_by_id.clear()
        self.items_by_name.clear()

        missing_ids: list[int] = []

        for i in range(0, len(ids), batch_size):

            batch = ids[i:i + batch_size]

            params = {
                "ids": ",".join(str(item_id) for item_id in batch)
            }

            response = requests.get(
                url,
                params=params,
                timeout=API_TIMEOUT
            )

            response.raise_for_status()

            data = response.json()

            for item in data["data"]:

                self.add_item(
                    item_id=item["id"],
                    name=item["name"],
                    icon_url=item.get("iconUrl")
                )

            missing_ids.extend(data.get("missingIds", []))

            print(
                f"Processed {min(i + batch_size, len(ids))}"
                f"/{len(ids)} item IDs."
            )

        print(f"Downloaded {len(self.items_by_id)} items.")
        print(f"Missing items: {len(missing_ids)}")

                
    def save_items(self) -> None:

        file_path = Path("data/items.json")

        file_path.parent.mkdir(parents=True, exist_ok=True)

        item_data = []

        for item in self.items_by_id.values():

            item_data.append({
                "id": item.item_id,
                "name": item.name,
                "iconUrl": item.icon_url
            })

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(item_data, file, indent=2)
            
            
    def load_items(self) -> None:

        file_path = Path("data/items.json")

        if not file_path.exists():
            raise FileNotFoundError("No saved items found.")

        with file_path.open("r", encoding="utf-8") as file:
            item_data = json.load(file)

        self.items_by_id.clear()
        self.items_by_name.clear()

        for item in item_data:

            self.add_item(
                item_id=item["id"],
                name=item["name"],
                icon_url=item.get("iconUrl")
            )

    def save_metadata(
        self,
        manifest: dict,
        item_ids: set[int]
    ) -> None:

        channel = manifest["defaultChannel"]

        dataset = manifest["channels"][channel]["datasets"]["items"]

        file_path = Path("data/item_metadata.json")

        file_path.parent.mkdir(parents=True, exist_ok=True)

        metadata = {
            "dataset": dataset,
            "item_count": len(self.items_by_id),
            "requested_ids": sorted(item_ids)
        }

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(metadata, file, indent=2)
            
    def update_items(
        self,
        manifest: dict,
        item_ids: set[int],
        force: bool = False
    ) -> None:

        channel = manifest["defaultChannel"]

        current_dataset = (
            manifest["channels"][channel]["datasets"]["items"]
        )

        metadata_path = Path("data/item_metadata.json")
        items_path = Path("data/items.json")

        if not force and metadata_path.exists() and items_path.exists():

            with metadata_path.open("r", encoding="utf-8") as file:
                metadata = json.load(file)

            saved_dataset = metadata.get("dataset")
            saved_ids = set(metadata.get("requested_ids", []))

            if saved_dataset == current_dataset and saved_ids == item_ids:

                self.load_items()

                if len(self.items_by_id) == metadata.get("item_count"):
                    print("Item database is up to date.")
                    return

                print("Local item count mismatch. Downloading again.")

        print("Downloading latest item metadata...")

        self.fetch_items(manifest, item_ids)

        if not self.items_by_id:
            raise ValueError("No items were downloaded.")

        self.save_items()
        self.save_metadata(manifest, item_ids)

        print(f"Item database updated: {len(self.items_by_id)} items.")