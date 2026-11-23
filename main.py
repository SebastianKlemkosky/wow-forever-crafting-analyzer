
from recipes import RecipeCatalog


def main() -> None:
    catalog = RecipeCatalog()

    catalog.update_recipes()

    print(f"Total recipes available: {len(catalog.recipes)}")


if __name__ == "__main__":
    main()
