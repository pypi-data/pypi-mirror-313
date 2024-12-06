def color_value(value: int | float, colors: tuple[str, str, str] = ('green', 'red', 'white')):
    positive, negative, neutral = colors
    if isinstance(value, (int, float)):
        value_color = negative if value < 0 else positive if value > 0 else neutral
        return value_color
