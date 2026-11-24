from dataclasses import dataclass
from recipes import Recipe
from item import Item
from material import MaterialCost
from acquisition import RecipeAcquisition
import math


@dataclass
class RecipeAnalysis:
    recipe: Recipe
    product: Item
    product_unit_price: int
    materials: list[MaterialCost]
    acquisitions: list[RecipeAcquisition]

    @property
    def material_cost(self) -> int:
        return sum(
            material.total_cost
            for material in self.materials
        )

    @property
    def product_value(self) -> int:
        return self.recipe.product_count * self.product_unit_price

    @property
    def profit(self) -> int:
        return self.product_value - self.material_cost

    @property
    def roi(self) -> float | None:
        if self.material_cost == 0:
            return None

        return round(
            self.profit / self.material_cost * 100,
            2
        )

    @property
    def acquisition_cost(self) -> int | None:
        prices = [
            acquisition.price
            for acquisition in self.acquisitions
            if acquisition.price is not None
        ]

        if not prices:
            return None

        return min(prices)

    @property
    def break_even_crafts(self) -> int | None:
        cost = self.acquisition_cost

        if cost is None or self.profit <= 0:
            return None

        return math.ceil(cost / self.profit)