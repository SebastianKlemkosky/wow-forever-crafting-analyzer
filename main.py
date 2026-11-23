
from market import Market
from utils import format_currency

def main() -> None:
    # Create US PvP Horde market
    market = Market(
        region="us",
        ruleset="pvp",
        faction="horde"
    )

    print(market.market_name)
    print(f"Market ID: {market.market_key}")

    # Retrieve Auction House data
    market.fetch_data()


    item = market.get_item_by_name("Burning Charm")

    if item is not None:
        stats = market.get_item_stats(item)

        print(f"Item: {item['name']}")
        print(f"Available Quantity: {stats['listed']}")
        print(f"24h Volume: {stats['vol24']}")
        print(f"Lowest Price: {format_currency(stats['ask'])}")
        print(f"Median Price: {format_currency(stats['median'])}")
    else:
        print("Item not found.")


if __name__ == "__main__":
    main()
