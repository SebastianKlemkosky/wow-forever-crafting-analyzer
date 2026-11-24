from analysis import RecipeAnalysis
from pathlib import Path
from datetime import datetime, timezone
import json


def format_currency(copper: int) -> str:
    sign = "-" if copper < 0 else ""
    copper = abs(copper)

    gold = copper // 10000
    remaining = copper % 10000

    silver = remaining // 100
    remaining = remaining % 100

    return f"{sign}{gold}g {silver}s {remaining}c"


def export_results(
    results: list[RecipeAnalysis],
    region: str,
    ruleset: str,
    faction: str
) -> None:

    export = []

    for analysis in results:

        recipe = analysis.recipe

        materials = []

        for material in analysis.materials:
            materials.append({
                "item_id": material.item.item_id,
                "name": material.item.name,
                "url": material.item.url,
                "icon_url": material.item.icon_url,
                "quantity": material.quantity,
                "unit_price": material.unit_price,
                "total_cost": material.total_cost
            })

        acquisitions = []

        for acquisition in analysis.acquisitions:
            acquisitions.append({
                "item_id": acquisition.item_id,
                "name": acquisition.name,
                "url": acquisition.url,
                "icon_url": (
                    acquisition.item.icon_url
                    if acquisition.item is not None
                    else None
                ),
                "price": acquisition.price
            })

        export.append({
            "recipe_id": recipe.recipe_id,
            "name": recipe.name,
            "profession": recipe.profession,
            "required_skill": recipe.required_skill,
            "icon_url": recipe.icon_url,
            "recipe_url": recipe.url,
            "cast_time": recipe.cast_time,
            "cooldown": recipe.cooldown,

            "product": {
                "item_id": analysis.product.item_id,
                "name": analysis.product.name,
                "url": analysis.product.url,
                "icon_url": analysis.product.icon_url,
                "quantity": recipe.product_count,
                "unit_price": analysis.product_unit_price,
                "total_value": analysis.product_value
            },

            "materials": materials,
            "acquisitions": acquisitions,
            "acquisition_cost": analysis.acquisition_cost,
            "break_even_crafts": analysis.break_even_crafts,

            "material_cost": analysis.material_cost,
            "fee_percentage": analysis.fee_percentage,
            "auction_house_fee": analysis.auction_house_fee,
            "net_revenue": analysis.net_revenue,
            "gross_profit": analysis.gross_profit,
            "profit": analysis.profit,
            "roi": analysis.roi
        })

    file_path = (
        Path("docs/markets")
        / region
        / ruleset
        / f"{faction}.json"
    )

    file_path.parent.mkdir(parents=True, exist_ok=True)

    market_data = {
        "region": region,
        "ruleset": ruleset,
        "faction": faction,
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "recipes": export
    }

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(market_data, file, indent=2)

    print(f"Exported {len(export)} recipes to {file_path}")