import requests
from config import AH_BASE_URL, API_TIMEOUT, MARKETS, REGIONS

class Market:
    def __init__(self, region: str, ruleset: str, faction: str,) -> None:
        self.region = region
        self.ruleset = ruleset
        self.faction = faction
        self.market_key: str = self.resolve_market()
        self.data: dict | None = None
        

    def resolve_market(self) -> str:
        region: str = REGIONS[self.region]
        auction_house_id: int = MARKETS[self.ruleset][self.faction]

        return f"{region}-2-{auction_house_id}"

    @property
    def market_name(self) -> str:
        return f"{self.region.upper()} {self.ruleset.upper()} {self.faction.capitalize()}"

    def fetch_data(self) -> None:
        url: str = f"{AH_BASE_URL}/m/{self.market_key}"

        response = requests.get(url, timeout=API_TIMEOUT)
        response.raise_for_status()

        self.data = response.json()

    def get_item_stats(self, item: dict) -> dict:
        if self.data is None:
            raise ValueError("Market data has not been loaded.")

        fields = self.data["f"]
        values = item["o"]

        result = dict(zip(fields, values, strict=True))

        return result
    
    def get_item_by_id(self, item_id: int) -> dict | None:
        if self.data is None:
            raise ValueError("Market data has not been loaded.")

        items = self.data["items"]

        for item in items:
            if item["id"] == item_id:
                return item

        return None

    def get_item_by_name(self, item_name: str) -> dict | None:
        if self.data is None:
            raise ValueError("Market data has not been loaded.")

        items = self.data["items"]

        for item in items:
            if item["name"].lower() == item_name.lower():
                return item

        return None

