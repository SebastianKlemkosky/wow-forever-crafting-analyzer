from dataclasses import dataclass
from item import Item


@dataclass
class MaterialCost:
    item: Item
    quantity: int
    unit_price: int

    @property
    def total_cost(self) -> int:
        return self.quantity * self.unit_price