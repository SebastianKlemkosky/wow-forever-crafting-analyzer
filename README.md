# WoW Forever Crafting Market Analyzer

## Live Website

[WoW Forever Crafting Market Analyzer](https://sebastianklemkosky.github.io/wow-forever-crafting-analyzer/)

## Overview

A web-based crafting profitability and market analysis tool for World of Warcraft Forever, built with Python and JavaScript.

The application combines Auction House prices, profession recipes, and item metadata to identify profitable crafting opportunities, calculate material costs, and evaluate recipe acquisition investments across 30 Auction House markets.

## Features

### Market Analysis

- Automatic Auction House data retrieval
- US and EU market selection
- PvP, Normal, Hardcore, RP, and RP-PvP market support
- Alliance, Horde, and Neutral Auction House support
- Market update timestamps
- Market profitability summaries

### Crafting Analysis

- Crafting material cost calculations
- Crafted product market values
- Estimated profit per craft
- Return on investment (ROI)
- Individual material quantities and unit prices
- Recipe acquisition costs
- Break-even crafting calculations

### Filtering and Sorting

- Profession filtering
- Recipe name searching
- Maximum profession skill filtering
- Unknown skill requirement filtering
- Profitable recipe filtering
- Sorting by profit, recipe name, and skill requirement

### User Interface

- Classic WoW-inspired interface
- Expandable recipe details
- Recipe, material, and acquisition item icons
- Clickable item and recipe database links
- Gold, silver, and copper currency formatting
- Responsive website layout

### Automation and Data Management

- Automated hourly market updates using GitHub Actions
- Static website deployment through GitHub Pages
- Version-based recipe and item metadata caching
- Batched item metadata retrieval
- Missing data handling
- Market-specific JSON exports

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend and market analysis |
| JavaScript | Frontend functionality |
| HTML | Website structure |
| CSS | Website styling |
| JSON | Data storage and transfer |
| Requests | REST API integration |
| uv | Python dependency management |
| Git | Version control |
| GitHub Actions | Automated market updates |
| GitHub Pages | Website hosting |

## How It Works

1. Retrieve the latest game data manifest.
2. Retrieve and cache profession recipe data.
3. Identify all unique items required by the recipes.
4. Retrieve and cache item names and icons.
5. Retrieve Auction House prices for each configured market.
6. Calculate crafting material costs and product values.
7. Calculate estimated profit and return on investment.
8. Determine available recipe acquisition costs and break-even requirements.
9. Export market-specific results into JSON files.
10. Display the results through an interactive static website.

GitHub Actions is configured to run the Python backend every hour and automatically deploy the updated market data through GitHub Pages.

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

## Financial Calculations

### Material Cost

The combined Auction House cost of all materials required to craft a recipe.

### Product Value

The estimated market value of the total quantity produced by a recipe.

### Profit per Craft

```text
Profit = Product Value - Material Cost
```

### Return on Investment

```text
ROI = (Profit / Material Cost) × 100
```

### Recipe Acquisition Cost

The lowest available Auction House price among known items that teach the recipe.

### Break-Even Crafts

The number of successful crafts and sales required to recover the recipe acquisition cost.

```text
Break-Even Crafts = ceil(Acquisition Cost / Profit per Craft)
```

Break-even calculations are only available when the acquisition cost is known and the recipe has a positive estimated profit.

## Running Locally

### Requirements

- Python 3.13 or newer
- uv
- Internet connection

### Install Dependencies

```bash
uv sync
```

### Generate Market Data

```bash
uv run main.py
```

### Start the Local Website

```bash
uv run python -m http.server 8000 --directory docs
```

Open http://localhost:8000 in your browser.

## Data Sources

- [Warcraft Forever](https://warcraftforever.com/) — Profession recipes, item metadata, icons, and game data.
- [Auction House API](https://auctionhouse.tk.gg/) — Auction House market prices.

## Limitations

- Recipes without sufficient market pricing data are excluded from profitability calculations.
- Some profession skill requirements and item names may be unavailable.
- Recipe acquisition costs are based on available Auction House prices.
- Estimated profits do not account for Auction House fees.
- Market prices do not guarantee that an item will sell.
- Some markets may have insufficient data to analyze crafting opportunities.

## Disclaimer

Crafting profits are estimates based on available Auction House prices. Actual profits may vary depending on market demand, item availability, price fluctuations, and Auction House fees.

This is an unofficial community project and is not affiliated with Blizzard Entertainment.
