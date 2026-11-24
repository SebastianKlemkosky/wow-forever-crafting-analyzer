## Live Website

[WoW Forever Market Analyzer](https://sebastianklemkosky.github.io/wow-forever-market-analyzer/)


# WoW Forever Market Analyzer

A web-based Auction House and crafting profitability analyzer for World of Warcraft Forever, built with Python and JavaScript.

The application retrieves Auction House prices and profession recipe data to identify profitable crafting opportunities across different markets.

## Features

- Automatic Auction House data retrieval
- Crafting material cost and profit calculations
- US and EU market selection
- PvP, Normal, Hardcore, RP, and RP-PvP market support
- Alliance, Horde, and Neutral Auction House support
- Profession and recipe name filtering
- Maximum profession skill filtering
- Profitable recipe filtering
- Gold, silver, and copper currency formatting
- Classic WoW-inspired interface
- Automated hourly market updates using GitHub Actions
- Static website deployment through GitHub Pages

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend and market analysis |
| JavaScript | Frontend functionality |
| HTML | Website structure |
| CSS | Website styling |
| JSON | Data storage and transfer |
| Requests | API integration |
| uv | Python dependency management |
| GitHub Actions | Automated market updates |
| GitHub Pages | Website hosting |

## How It Works

1. Retrieve and cache profession recipe data.
2. Retrieve Auction House data for each configured market.
3. Calculate the total material cost for each recipe.
4. Calculate the market value of the crafted product.
5. Calculate estimated crafting profit.
6. Export market-specific results into JSON files.
7. Display the results through a static website.

GitHub Actions is configured to run the Python backend every hour and deploy the updated website automatically.

## Project Structure

```text
wow-forever-market-analyzer/
├── .github/
│   └── workflows/
│       └── update_market.yml
├── data/
│   ├── recipes.json
│   └── recipe_metadata.json
├── docs/
│   ├── markets/
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── analyzer.py
├── config.py
├── item.py
├── main.py
├── market.py
├── recipes.py
├── utils.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Running Locally

### Install dependencies

```bash
uv sync
```

### Generate market data

```bash
uv run main.py
```

### Start the local website

```bash
uv run python -m http.server 8000 --directory docs
```

Open http://localhost:8000 in your browser.

## Data Sources

- [Warcraft Forever](https://warcraftforever.com/) — Profession recipes and game data.
- [Auction House API](https://auctionhouse.tk.gg/) — Auction House market data.

## Future Improvements

- [ ] Complete missing profession skill requirements
- [ ] Display material costs and product values
- [ ] Display market update timestamps
- [ ] Account for Auction House fees
- [ ] Calculate return on investment (ROI)
- [ ] Display individual recipe reagents
- [ ] Compare crafting versus purchasing intermediate materials
- [ ] Track historical market prices
- [ ] Analyze market supply and demand
- [ ] Add automated unit tests

## Disclaimer

Crafting profits are estimates based on available Auction House prices. Actual profits may vary depending on market demand, item availability, price fluctuations, and Auction House fees.

This is an unofficial community project and is not affiliated with Blizzard Entertainment.
