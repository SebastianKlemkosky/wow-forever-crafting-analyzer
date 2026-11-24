from recipes import RecipeCatalog
from market import Market
from item import ItemCatalog
from analyzer import Analyzer
from utils import export_results
from config import REGIONS, MARKETS


def main() -> None:

    # Load recipes once
    recipes = RecipeCatalog()
    recipes.update_recipes()

    print(f"\nTotal recipes available: {len(recipes.recipes)}")

    # Verify manifest is available
    if recipes.manifest is None:
        raise ValueError("Manifest has not been loaded.")

    # Collect required item IDs
    item_ids = recipes.get_required_item_ids()

    print(f"Required unique items: {len(item_ids)}")

    # Load item metadata once
    items = ItemCatalog()
    items.update_items(recipes.manifest, item_ids)

    print(f"Item metadata loaded: {len(items.items_by_id)}")

    # Iterate through all available markets
    for region in REGIONS:
        for ruleset in MARKETS:
            for faction in MARKETS[ruleset]:

                print(f"\nProcessing: {region} | {ruleset} | {faction}")

                try:
                    # Load Auction House data
                    market = Market(region, ruleset, faction)
                    market.fetch_data()

                    if market.data is None:
                        raise ValueError("Market data has not been loaded.")

                    # Add market items missing from the catalog
                    items.load_market_items(market.data["items"])

                    print(f"Items loaded: {len(items.items_by_id)}")

                    # Initialize analyzer
                    analyzer = Analyzer(market, items)

                    # Analyze all recipes
                    results = analyzer.analyze_recipes(recipes.recipes)

                    # Export market-specific results
                    export_results(results, region, ruleset, faction)

                except Exception as e:
                    print(f"Failed to process {region}/{ruleset}/{faction}: {e}")


if __name__ == "__main__":
    main()