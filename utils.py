from recipes import Recipe
from pathlib import Path
import json
from datetime import datetime, timezone

def format_currency(copper: int) -> str:
    sign = "-" if copper < 0 else ""
    copper = abs(copper)

    gold = copper // 10000
    remaining = copper % 10000

    silver = remaining // 100
    remaining = remaining % 100

    return f"{sign}{gold}g {silver}s {remaining}c"


def export_results(
    results: list[tuple[Recipe, int]],
    region: str,
    ruleset: str,
    faction: str
) -> None:

    export = []

    for recipe, profit in results:
        export.append({
            "recipe_id": recipe.recipe_id,
            "name": recipe.name,
            "profession": recipe.profession,
            "required_skill": recipe.required_skill,
            "profit": profit
        })

    file_path = Path("docs/markets") / region / ruleset / f"{faction}.json"

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