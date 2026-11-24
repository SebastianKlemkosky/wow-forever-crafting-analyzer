from dataclasses import dataclass
from item import Item
from config import RECIPE_BASE_URL


@dataclass
class RecipeAcquisition:
    item_id: int
    item: Item | None
    price: int | None

    @property
    def name(self) -> str | None:
        if self.item is None:
            return None

        return self.item.name

    @property
    def url(self) -> str:
        return f"{RECIPE_BASE_URL}/items/{self.item_id}"