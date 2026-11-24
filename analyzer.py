from recipes import Recipe
from market import Market
from item import ItemCatalog
from material import MaterialCost
from analysis import RecipeAnalysis
from acquisition import RecipeAcquisition

class Analyzer:
    def __init__(self, market: Market, items: ItemCatalog) -> None:
        self.market = market
        self.items = items

    def calculate_materials(
        self, recipe: Recipe
    ) -> list[MaterialCost] | None:

        materials: list[MaterialCost] = []

        for item_id, quantity in recipe.reagents:

            item = self.items.get_item_by_id(item_id)

            if item is None:
                return None

            price = item.get_price(self.market)

            if price is None:
                return None

            material = MaterialCost(
                item=item,
                quantity=quantity,
                unit_price=price
            )

            materials.append(material)

        return materials

    def calculate_acquisitions(
        self, recipe: Recipe
    ) -> list[RecipeAcquisition]:

        acquisitions: list[RecipeAcquisition] = []

        for item_id in recipe.taught_by:

            item = self.items.get_item_by_id(item_id)

            price = None

            if item is not None:
                price = item.get_price(self.market)

            acquisition = RecipeAcquisition(
                item_id=item_id,
                item=item,
                price=price
            )

            acquisitions.append(acquisition)

        return acquisitions


    def analyze_recipe(
        self, recipe: Recipe
    ) -> RecipeAnalysis | None:

        if recipe.product_id is None:
            return None

        product = self.items.get_item_by_id(recipe.product_id)

        if product is None:
            return None

        product_price = product.get_price(self.market)

        if product_price is None:
            return None

        materials = self.calculate_materials(recipe)

        if materials is None:
            return None

        acquisitions = self.calculate_acquisitions(recipe)

        return RecipeAnalysis(
            recipe=recipe,
            product=product,
            product_unit_price=product_price,
            materials=materials,
            acquisitions=acquisitions
        )

    def analyze_recipes(
        self, recipes: list[Recipe]
    ) -> list[RecipeAnalysis]:

        results: list[RecipeAnalysis] = []

        for recipe in recipes:

            analysis = self.analyze_recipe(recipe)

            if analysis is None:
                continue

            results.append(analysis)

        results.sort(
            key=lambda analysis: analysis.profit,
            reverse=True
        )

        return results