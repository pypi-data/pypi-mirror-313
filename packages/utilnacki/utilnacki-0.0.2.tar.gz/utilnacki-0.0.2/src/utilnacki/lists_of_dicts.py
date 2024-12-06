from datetime import date, datetime
from collections import Counter
from operator import itemgetter
from typing import Any, Sequence

import pandas as pd

def add_running_total_item(data: list[dict], sorts: list[str | tuple[str, bool]], value_key: str) -> list[dict]:
    """For a list of dictionaries, return a list of dicts with an added key called running_total
    whose value is the summed value_key.
    Sorts is a list whose members can be either a string e.g. 'my_col' or a tuple e.g. ('my_col', True).
    The boolean True will return that key in the reverse/descending order.
    The value for the provided value_key must be an integer or float."""
    data = sort_data(data, sorts)
    running_total = 0
    for d in data:
        for k, v in d.items():
            if k == value_key:
                d.setdefault(k, 0)
                running_total += v
                d['running_total'] = running_total
                break
    return data

def filter_data(incoming_data: list[dict], filters: dict) -> list[dict]:
    """Filters is a dict whose values are a sequence. If a value is a tuple of two dates/date-times, then the value
    must fall between the two dates/date-times. If a value is ['All', 'all', 'ALL'], it is not filtered."""
    all_terms = ['All', 'all', 'ALL']

    def is_special_date_parameter(seq: Sequence) -> bool:
        return all([isinstance(seq, tuple), len(seq) == 2, all(isinstance(elem, (date, datetime)) for elem in seq)])

    # TODO: evaluate if i should backport this to disc golf project (if it works)
    if not filters:
        return incoming_data
    filtered = incoming_data
    for key, value in filters.items():
        if value and value not in all_terms:
            if is_special_date_parameter(value):
                filtered = [entry for entry in filtered if value[0] <= entry[key] <= value[1]]
            else:
                filtered = [entry for entry in filtered if entry[key] in value]
    return filtered


def group_data(data: list[dict], grouper_keys: list[str], value_key: str) -> list[dict]:
    """ Grouper_keys is a list of keys, so multi-key grouping is supported.
    The value_key's value must be an int or float. """
    # TODO: backport to Disc Golf project, if this works
    counter = Counter()

    def is_summable(val):
        return isinstance(val, (int, float))

    for item in data:
        if not is_summable(item[value_key]):
            raise ValueError('The value of the value_col must be an integer or float')

        key = tuple(item[grouper] for grouper in grouper_keys)
        value = item[value_key]
        counter[key] += value

    result = []
    for key, total in counter.items():
        group_dict = dict(zip(grouper_keys, key))
        group_dict[value_key] = total
        result.append(group_dict)

    return result

def sort_data(data: list[dict], sorts: list[str | tuple[str, bool]]) -> list[dict]:
    """Sorts is a list whose members can be either a string e.g. 'my_col' or a tuple e.g. ('my_col', True).
    The boolean True will return that key in the reverse/descending order"""
    # for each sort item, if the value is a string (the column name), convert it to a tuple (col_name, True))
    sort_tuples = [s if isinstance(s, tuple) else (s, False) for s in sorts]
    # iterate backwards through the sort tuples & perform each sort
    for key, reverse in reversed(sort_tuples):
        data.sort(key=itemgetter(key), reverse=reverse)
    return data

def to_df(data: list[dict[str, Any]]) -> pd.DataFrame:
    return pd.DataFrame(data)

def unique_sorted(values: list[dict], key: str) -> list[Any]:
    """From a list of dicts, return a list of unique sorted values for a given key.
    The key doesn't have to be present in any or all of the dicts."""
    return sorted({v for d in values for k, v in d.items() if k == key and v})
