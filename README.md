# WoW Forever Crafting Market Analyzer

## Live Website

[WoW Forever Crafting Market Analyzer](https://sebastianklemkosky.github.io/wow-forever-crafting-analyzer/)

## Overview

A web-based crafting profitability and market analysis application for World of Warcraft Forever, built with Python and JavaScript.

The application combines Auction House prices, profession recipes, and item metadata to identify profitable crafting opportunities across 30 Auction House markets.

It calculates material costs, crafted product values, Auction House fees, estimated net profits, return on investment, and recipe acquisition break-even requirements.

## Features

### Market Analysis

- Automatic Auction House data retrieval
- Support for 30 Auction House markets
- US and EU region selection
- PvP, Normal, Hardcore, RP, and RP-PvP market support
- Alliance, Horde, and Neutral Auction House support
- Market update timestamps
- Market profitability summaries

### Crafting and Financial Analysis

- Total crafting material costs
- Individual material quantities and unit prices
- Crafted product market values
- Gross profit calculations
- Faction-specific Auction House sale fees
- Net revenue calculations
- Net profit per craft
- Fee-adjusted return on investment (ROI)
- Recipe acquisition costs
- Break-even crafting calculations

### Filtering and Sorting

- Profession filtering
- Recipe name searching
- Maximum profession skill filtering
- Unknown skill requirement filtering
- Profitable recipe filtering
- Sorting by net profit, recipe name, and skill requirement

### User Interface

- Classic WoW-inspired interface
- Expandable recipe details
- Detailed financial summaries
- Required materials tables
- Recipe acquisition tables
- Recipe, material, and acquisition item icons
- Clickable item and recipe database links
- Gold, silver, and copper currency formatting
- Responsive website layout

### Automation and Data Management

- Automated hourly market updates using GitHub Actions
- Automatic website deployment through GitHub Pages
- Version-based recipe and item metadata caching
- Batched item metadata retrieval
- Missing data handling
- Market-specific JSON exports

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
| Git | Version control |
| GitHub Actions | Automated market updates and deployment |
| GitHub Pages | Static website hosting |

## How It Works

1. Retrieve the latest game data manifest.
2. Retrieve and cache profession recipe data.
3. Identify all unique items required by profession recipes.
4. Retrieve and cache item metadata, including names and icons.
5. Retrieve Auction House prices for each configured market.
6. Calculate crafting material costs and product values.
7. Determine the applicable Auction House sale fee.
8. Calculate gross profit, net revenue, and net profit.
9. Calculate fee-adjusted return on investment.
10. Determine available recipe acquisition costs.
11. Calculate the number of crafts required to recover recipe acquisition costs.
12. Sort recipes by estimated net profit.
13. Export market-specific results into JSON files.
14. Display the results through an interactive static website.

GitHub Actions is configured to run the Python backend every hour and automatically deploy updated market data through GitHub Pages.

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

## Backend Components

| Module | Responsibility |
|---|---|
| `main.py` | Coordinates market data retrieval and recipe analysis |
| `config.py` | Stores API configuration, market mappings, professions, and fee rates |
| `market.py` | Retrieves Auction House data and resolves market-specific fees |
| `recipes.py` | Retrieves and caches profession recipe data |
| `item.py` | Manages item metadata and market prices |
| `material.py` | Represents crafting materials and calculates material costs |
| `acquisition.py` | Represents recipe acquisition items and prices |
| `analysis.py` | Calculates financial metrics for individual recipes |
| `analyzer.py` | Analyzes recipes and ranks crafting opportunities |
| `utils.py` | Formats currency and exports market analysis results |

## Financial Calculations

All monetary calculations are performed in copper to preserve currency precision and avoid floating-point currency rounding issues.

### Material Cost

The combined cost of all materials required to craft a recipe.

```text
Material Cost = Sum(Material Quantity × Unit Price)
```

### Product Value

The estimated market value of the total quantity produced by a recipe.

```text
Product Value = Product Quantity × Unit Price
```

### Auction House Fees

The application applies a sale fee based on the selected Auction House.

| Auction House | Sale Fee |
|---|---:|
| Alliance | 5% |
| Horde | 5% |
| Neutral | 15% |

```text
Auction House Fee = floor(Product Value × Fee Percentage / 100)
```

Fees are rounded down to the nearest copper.

Auction deposits are assumed to be refunded upon successful sales. Lost deposits from expired or cancelled auctions are not included.

### Gross Profit

Estimated crafting profit before Auction House fees.

```text
Gross Profit = Product Value - Material Cost
```

### Net Revenue

The estimated amount received after Auction House fees.

```text
Net Revenue = Product Value - Auction House Fee
```

### Net Profit

Estimated crafting profit after material costs and Auction House fees.

```text
Net Profit = Net Revenue - Material Cost
```

Net profit is used for recipe ranking, profitability filtering, market summaries, return on investment, and break-even calculations.

### Return on Investment (ROI)

The percentage return relative to the cost of crafting materials.

```text
ROI = (Net Profit / Material Cost) × 100
```

ROI is unavailable when the total material cost is zero.

### Recipe Acquisition Cost

The lowest known Auction House price among available items that teach a recipe.

Recipe acquisition costs are treated as a separate initial investment rather than a recurring crafting expense.

Unavailable acquisition prices are not treated as zero.

### Break-Even Crafts

The number of successful crafts and sales required to recover the initial recipe acquisition cost.

```text
Break-Even Crafts = ceil(Acquisition Cost / Net Profit)
```

Break-even calculations are only available when the acquisition cost is known and the recipe has a positive estimated net profit.

## Architecture

```text
Warcraft Forever API       Auction House API
         │                         │
         ▼                         ▼
 Recipe and Item Data         Market Data
         │                         │
         ▼                         │
   Local JSON Cache                │
         │                         │
         └────────────┬────────────┘
                      ▼
               Recipe Analyzer
                      │
                      ▼
              Financial Analysis
                      │
                      ▼
           Market-Specific JSON
                      │
                      ▼
            JavaScript Frontend
                      │
                      ▼
                GitHub Pages
```

The application separates data retrieval, item management, recipe analysis, financial calculations, and frontend presentation into independent components.

All financial calculations are performed by the Python backend. The JavaScript frontend handles filtering, sorting, formatting, and displaying the exported results.

This architecture allows the application to operate without a continuously running backend server or external database.

## Running Locally

### Requirements

- Python 3.13 or newer
- uv
- Internet connection

### Clone the Repository

```bash
git clone https://github.com/SebastianKlemkosky/wow-forever-crafting-analyzer.git
cd wow-forever-crafting-analyzer
```

### Install Dependencies

```bash
uv sync
```

### Generate Market Data

```bash
uv run main.py
```

Generated market analysis files are stored in:

```text
docs/markets/
```

### Start the Local Website

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

## Limitations

- Recipes without sufficient market pricing data are excluded from analysis.
- Some profession skill requirements and item names may be unavailable.
- Recipe acquisition costs depend on available Auction House listings.
- Material costs are based on Auction House prices rather than vendor prices or self-gathered materials.
- Market prices do not guarantee that an item will sell.
- Market availability and listing quantities may affect actual crafting costs.
- Auction House fees assume successful sales at the estimated product value.
- Lost deposits from expired or cancelled auctions are not included.
- Some markets may have insufficient data to calculate crafting opportunities.

## Disclaimer

Crafting profits are estimates based on available Auction House prices and configured Auction House sale fees.

Actual profits may vary depending on market demand, item availability, price fluctuations, listing quantities, and lost auction deposits.

This is an unofficial community project and is not affiliated with Blizzard Entertainment.