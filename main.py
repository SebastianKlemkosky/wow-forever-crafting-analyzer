
from recipes import RecipeCatalog
from market import Market
from item import ItemCatalog
from utils import format_currency


def main() -> None:
    # Load recipes
    recipes = RecipeCatalog()
    recipes.update_recipes()

    print(f"\nTotal recipes available: {len(recipes.recipes)}")

    # Load Auction House data
    market = Market("us", "pvp", "horde")
    market.fetch_data()

    if market.data is None:
        raise ValueError("Market data has not been loaded.")

    print(f"Market: {market.market_name}")

    # Build item catalog
    items = ItemCatalog()
    items.load_market_items(market.data["items"])

    print(f"Items loaded: {len(items.items_by_id)}")

    # Find a recipe
    recipe = recipes.get_recipe_by_name("Smelt Bronze")

    if recipe is None:
        print("Recipe not found.")
        return

    # Recipe information
    print("\n--- Recipe Information ---")
    print(f"Name: {recipe.name}")
    print(f"Recipe ID: {recipe.recipe_id}")
    print(f"Profession ID: {recipe.profession}")
    print(f"Category ID: {recipe.category}")
    print(f"Skill: {recipe.skill}")
    print(f"Cast Time: {recipe.cast_time} ms")
    print(f"Cooldown: {recipe.cooldown}")
    print(f"Recipe URL: {recipe.url}")

    # Material information
    print("\n--- Materials ---")

    total_material_cost = 0
    missing_prices = False

    for item_id, quantity in recipe.reagents:
        item = items.get_item_by_id(item_id)

        if item is None:
            print(f"Unknown item ({item_id}) x{quantity}")
            missing_prices = True
            continue

        price = item.get_price(market)

        if price is None:
            print(f"{item.name} x{quantity}: No price available")
            missing_prices = True
            continue

        cost = price * quantity
        total_material_cost += cost

        print(f"{item.name} x{quantity}")
        print(f"  Unit price: {format_currency(price)}")
        print(f"  Total cost: {format_currency(cost)}")

    if not missing_prices:
        print(f"\nTotal Material Cost: {format_currency(total_material_cost)}")
    else:
        print("\nTotal Material Cost: Unavailable (missing prices)")

    # Product information
    print("\n--- Product ---")

    if recipe.product_id is not None:
        product = items.get_item_by_id(recipe.product_id)

        if product is not None:
            price = product.get_price(market)

            print(f"Product: {product.name}")
            print(f"Quantity Produced: {recipe.product_count}")

            if price is not None:
                total_value = price * recipe.product_count

                print(f"Unit Price: {format_currency(price)}")
                print(f"Total Value: {format_currency(total_value)}")

                # Preliminary profit calculation (before AH fees)
                if not missing_prices:
                    profit = total_value - total_material_cost

                    print("\n--- Crafting Profit ---")
                    print(f"Material Cost: {format_currency(total_material_cost)}")
                    print(f"Product Value: {format_currency(total_value)}")
                    print(f"Gross Profit: {format_currency(profit)}")
            else:
                print("No product price available.")
        else:
            print(f"Product ID {recipe.product_id} not found.")
    else:
        print("This recipe does not produce a standard item.")

    # Reverse item lookup
    print("\n--- Item Lookup Test ---")
    print(items.get_item_by_id(2840))
    print(items.get_item_by_name("Tin Bar"))
    print(f"Copper Bar ID: {items.get_item_id('Copper Bar')}")
    print(f"Bronze Bar Name: {items.get_item_name(2841)}")


if __name__ == "__main__":
    main()
