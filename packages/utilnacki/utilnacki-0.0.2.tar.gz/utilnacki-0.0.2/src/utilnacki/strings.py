def list_items_in_english(items: list) -> str | None:
    """[] -> None, ['Alice'] -> 'Alice', ['Alice', 'Bob'] -> 'Alice and Bob',
    ['Alice', 'Bob', 'Charlie'] -> 'Alice, Bob, and Charlie'
    ['Alice', 'Bob', 'Charlie', 'David'] -> 'Alice, Bob, and 2 others'"""
    item_cnt = len(items)
    if item_cnt == 0:
        return None
    elif item_cnt == 1:
        return f'{items[0]}'
    elif item_cnt == 2:
        return f'{items[0]} and {items[1]}'
    elif item_cnt == 3:
        return f'{items[0]}, {items[1]} and {items[2]}'
    else:
        return f'{items[0]}, {items[1]} and {len(items) - 2} others'
