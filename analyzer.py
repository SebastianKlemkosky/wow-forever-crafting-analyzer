from recipes import RecipeCatalog, Recipe
from market import Market
from item import ItemCatalog


class Analyzer:
    def __init__(self, market: Market, items: ItemCatalog) -> None:
        self.market = market
        self.items = items

    def calculate_material_cost(self, recipe: Recipe) -> int | None:
        total_cost = 0

        for item_id, quantity in recipe.reagents:
            item = self.items.get_item_by_id(item_id)
            if item is None:
                return None
            
            price = item.get_price(self.market)
            if price is None:
                return None
            
            total_cost += price * quantity
        return total_cost
        
    def calculate_product_value(self, recipe: Recipe) -> int | None:
        if recipe.product_id is None:
            return None
        
        item = self.items.get_item_by_id(recipe.product_id)
        if item is None:
            return None
        
        price = item.get_price(self.market)
        if price is None:
            return None
        
        return recipe.product_count * price

    def calculate_profit(self, recipe: Recipe) -> int | None:
        material_cost = self.calculate_material_cost(recipe)
        product_value = self.calculate_product_value(recipe)
        
        if material_cost is None or product_value is None:
            return None
        
        return product_value - material_cost

    def analyze_recipes(self, recipes: list[Recipe]) -> list[tuple[Recipe, int]]:
        results = []
        for recipe in recipes:
            profit = self.calculate_profit(recipe)
            if profit is None:
                continue
            results.append((recipe, profit))
            
        results.sort(key=lambda x: x[1], reverse=True)
        return results