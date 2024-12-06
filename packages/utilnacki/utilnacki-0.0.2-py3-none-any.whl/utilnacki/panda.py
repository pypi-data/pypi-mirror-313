from typing import Any

import pandas as pd

def to_df(data: list[dict[str, Any]]) -> pd.DataFrame:
    return pd.DataFrame(data)

def color_value_map(val: Any, colors: tuple[str, str, str] = ('green', 'red', 'white')) -> str:
    """Use with df.style.map.  For any column with a value of int or float, return the colored text string.
    Example usage: colored_df = df.style.map(color_value_map)"""
    positive, negative, neutral = colors
    if isinstance(val, (int, float)):
        color = negative if val < 0 else positive if val > 0 else neutral
        return f'color: {color}'
