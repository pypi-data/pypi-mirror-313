from typing import Any

def unique_sorted(values: list[Any]) -> list[Any]:
    return sorted({v for v in values if v})

def unique_w_preserved_insertion_order(values: list[Any]) -> list[Any]:
    return list(dict.fromkeys(values))
