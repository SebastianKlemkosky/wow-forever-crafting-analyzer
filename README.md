# WoW Forever Crafting Market Analyzer

## Live Website

[WoW Forever Crafting Market Analyzer](https://sebastianklemkosky.github.io/wow-forever-crafting-analyzer/)

## Overview

# WoW Forever Market Analyzer

A web-based Auction House and crafting profitability analyzer for World of Warcraft Forever, built with Python and JavaScript.

The application retrieves Auction House prices and profession recipe data to identify profitable crafting opportunities across different markets.

## Features

### Market Analysis

- Automatic Auction House data retrieval
- Crafting material cost and profit calculations
- US and EU market selection
- PvP, Normal, Hardcore, RP, and RP-PvP market support
- Alliance, Horde, and Neutral Auction House support
- Profession and recipe name filtering
- Maximum profession skill filtering
- Unknown skill requirement filtering
- Profitable recipe filtering
- Gold, silver, and copper currency formatting
- Responsive website layout

### Automation and Data Management

- Automated hourly market updates using GitHub Actions
- Static website deployment through GitHub Pages

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend and financial analysis |
| JavaScript | Frontend functionality |
| HTML | Website structure |
| CSS | Website styling |
| JSON | Data storage and transfer |
| Requests | REST API integration |
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
wow-forever-crafting-analyzer/
├── .github/
│   └── workflows/
│       └── update_market.yml
├── data/
│   ├── recipes.json
│   ├── recipe_metadata.json
│   ├── items.json
│   └── item_metadata.json
├── docs/
│   ├── markets/
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── acquisition.py
├── analysis.py
├── analyzer.py
├── config.py
├── item.py
├── main.py
├── market.py
├── material.py
├── recipes.py
├── utils.py
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## Running Locally

### Install dependencies

```bash
uv sync
```

### Generate Market Data

```bash
uv run main.py
```

### Start the local website

```bash
uv run python -m http.server 8000 --directory docs
```

Open http://localhost:8000 in your browser.

## Automated Deployment

The application uses GitHub Actions to automate data retrieval, financial analysis, and website deployment.

The workflow performs the following operations:

1. Check out the repository.
2. Configure Python and uv.
3. Install project dependencies.
4. Execute the Python backend.
5. Generate market-specific JSON files.
6. Validate generated market data.
7. Upload the website files.
8. Deploy the website to GitHub Pages.

The workflow is configured to execute hourly and can also be triggered manually.

## Data Sources

- [Warcraft Forever](https://warcraftforever.com/) — Profession recipes, item metadata, icons, and game data.
- [Auction House API](https://auctionhouse.tk.gg/) — Auction House market prices.

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

Crafting profits are estimates based on available Auction House prices and configured Auction House sale fees.

Actual profits may vary depending on market demand, item availability, price fluctuations, listing quantities, and lost auction deposits.

This is an unofficial community project and is not affiliated with Blizzard Entertainment.