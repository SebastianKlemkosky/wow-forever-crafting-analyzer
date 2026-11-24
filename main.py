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

                    # Build item catalog
                    items = ItemCatalog()
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