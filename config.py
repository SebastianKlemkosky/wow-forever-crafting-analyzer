
# API Configuration
BASE_URL = "https://auctionhouse.tk.gg/api"
API_TIMEOUT = 30

# Supported Regions
REGIONS = {
    "us": "us",
    "eu": "eu",
}

# Auction House IDs by ruleset
MARKETS = {
    "pvp": {
        "alliance": 110,
        "horde": 113,
        "neutral": 116,
    },
    "normal": {
        "alliance": 111,
        "horde": 114,
        "neutral": 117,
    },
    "hardcore": {
        "alliance": 112,
        "horde": 115,
        "neutral": 118,
    },
    "rp": {
        "alliance": 119,
        "horde": 120,
        "neutral": 121,
    },
    "rp_pvp": {
        "alliance": 123,
        "horde": 124,
        "neutral": 125,
    },
}
