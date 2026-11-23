
def format_currency(copper: int) -> str:
    gold = copper // 10000
    remaining = copper % 10000

    silver = remaining // 100
    remaining = remaining % 100

    return f"{gold}g {silver}s {remaining}c"
