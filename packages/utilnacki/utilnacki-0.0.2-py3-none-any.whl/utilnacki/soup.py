import bs4

def list_of_dicts_from_soup_table(soup_table: bs4.element.Tag) -> list[dict]:
    """Accepts a BS table (a list of values for every row, including the header).
    Converts & returns a list of dicts where the headers are keys & the row data are values."""
    table_of_dicts = []
    rows = soup_table.find_all("tr")
    # Iterate over rows and extract cells (td or th tags), extracting the data from each cell in the row
    table_data = [[cell.get_text(strip=True) for cell in row.find_all(["td", "th"])] for row in rows]
    headers = [col for col in table_data[0]]
    for idx, row in enumerate(table_data[1:]):
        table_of_dicts.append({header: r for header, r in zip(headers, row)})
    return table_of_dicts
