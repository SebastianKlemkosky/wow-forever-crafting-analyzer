from config import RECIPE_BASE_URL, API_TIMEOUT
import requests
import json
from pathlib import Path

class Recipe:
    def __init__(self, data: dict) -> None:
        self.data = data

    @property
    def name(self) -> str:
        return self.data["name"]

    @property
    def recipe_id(self) -> int:
        return self.data["id"]

    @property
    def profession(self) -> int:
        return self.data["profession"]

    @property
    def category(self) -> int:
        return self.data["category"]

    @property
    def reagents(self) -> list[list[int]]:
        return self.data["reagents"]

    @property
    def product(self) -> dict | None:
        return self.data.get("product")

    @property
    def product_id(self) -> int | None:
        if self.product is None:
            return None

        return self.product["item"]

    @property
    def product_count(self) -> int:
        if self.product is None:
            return 0

        return self.product["count"]

    @property
    def skill(self) -> dict:
        return self.data["skill"]

    @property
    def required_skill(self) -> int | None:
        return self.skill.get("learn")

    @property
    def cast_time(self) -> int:
        return self.data["castMs"]

    @property
    def cooldown(self) -> int | None:
        cooldown = self.data.get("cooldown")

        if cooldown is None:
            return None

        return cooldown["ms"]

    @property
    def taught_by(self) -> list[int]:
        return self.data.get("taughtBy", [])

    @property
    def icon_url(self) -> str | None:
        return self.data.get("iconUrl")

    @property
    def url(self) -> str:
        return self.data["url"]


class RecipeCatalog:
    def __init__(self) -> None:
        self.manifest: dict | None = None
        self.data: dict | None = None
        self.recipes: list[Recipe] = []

    def fetch_manifest(self) -> None:
        url: str = f"{RECIPE_BASE_URL}/api/data/v1/manifest"

        response = requests.get(url, timeout=API_TIMEOUT)
        response.raise_for_status()

        self.manifest = response.json()

    def fetch_recipes(self) -> None:
        if self.manifest is None:
            raise ValueError("Manifest has not been loaded.")

        channel = self.manifest["defaultChannel"]
        dataset = self.manifest["channels"][channel]["datasets"]["recipes"]

        url = f"{RECIPE_BASE_URL}/api/data/v1/{dataset}/enUS/recipes"

        cursor: str | None = None
        all_recipes: list[dict] = []

        params = {
            "query": "",
            "limit": 100,
        }

        while True:
            if cursor is not None:
                params["cursor"] = cursor

            response = requests.get(
                url,
                params=params,
                timeout=API_TIMEOUT,
            )

            response.raise_for_status()

            data: dict = response.json()

            all_recipes.extend(data["data"])

            cursor = data.get("nextCursor")

            if cursor is None:
                break

        self.recipes = [Recipe(data) for data in all_recipes]

    def save_recipes(self) -> None:
        file_path = Path("data/recipes.json")

        file_path.parent.mkdir(parents=True, exist_ok=True)

        recipe_data = [recipe.data for recipe in self.recipes]

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(recipe_data, file, indent=2)
            
    def load_recipes(self) -> None:
        file_path = Path("data/recipes.json")

        if not file_path.exists():
            raise FileNotFoundError("No saved recipes found.")

        with file_path.open("r", encoding="utf-8") as file:
            recipe_data = json.load(file)

        self.recipes = [Recipe(data) for data in recipe_data]
        
    def save_metadata(self) -> None:
        if self.manifest is None:
            raise ValueError("Manifest has not been loaded.")

        channel = self.manifest["defaultChannel"]
        dataset = self.manifest["channels"][channel]["datasets"]["recipes"]

        file_path = Path("data/recipe_metadata.json")
        file_path.parent.mkdir(parents=True, exist_ok=True)

        metadata = {
            "dataset": dataset,
            "recipe_count": len(self.recipes),
        }

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(metadata, file, indent=2)
            
    def update_recipes(self, force: bool = False) -> None:
        # Get the latest dataset information
        self.fetch_manifest()

        if self.manifest is None:
            raise ValueError("Manifest has not been loaded.")

        channel = self.manifest["defaultChannel"]
        current_dataset = self.manifest["channels"][channel]["datasets"]["recipes"]

        metadata_path = Path("data/recipe_metadata.json")
        recipes_path = Path("data/recipes.json")

        # Check whether both local files exist
        if not force and metadata_path.exists() and recipes_path.exists():
            with metadata_path.open("r", encoding="utf-8") as file:
                metadata = json.load(file)

            saved_dataset = metadata.get("dataset")

            # Use cached recipes if the dataset has not changed
            if saved_dataset == current_dataset:
                self.load_recipes()

                # Verify the cached recipe count
                if len(self.recipes) == metadata.get("recipe_count"):
                    print("Recipe database is up to date.")
                    return

                print("Local recipe count mismatch. Downloading again.")

        # Download recipes if forced, missing, or outdated
        print("Downloading latest recipes...")

        self.fetch_recipes()

        if not self.recipes:
            raise ValueError("No recipes were downloaded.")

        self.save_recipes()
        self.save_metadata()

        print(f"Recipe database updated: {len(self.recipes)} recipes.")

    def get_recipe_by_name(self, name: str) -> Recipe | None:
        for recipe in self.recipes:
            if recipe.name.lower() == name.lower():
                return recipe

        return None
    
    def get_recipes_by_profession(self, profession: int) -> list[Recipe]:
        results: list[Recipe] = []
        for recipe in self.recipes:
            if recipe.profession == profession:
                results.append(recipe)
        return results