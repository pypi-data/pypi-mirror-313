from enum import Enum
from functools import cmp_to_key
from typing import List


def pluck_and_cast_properties(arr, fields):
    if fields == [] or fields is None:
        return arr

    new_arr = []
    orig_obj: object
    for orig_obj in arr:
        cast_obj = {}
        if fields:
            for f in fields:
                # Access the nested property using dot notation
                # TODO - allow both object and JSON dicts
                keys = f.split(".")
                o = orig_obj
                for key in keys:
                    o = getattr(o, key, "")
                cast_obj[f] = str(o) if o else ""

                # val = getattr(orig_obj, f, "")
                # cast_obj[f] = str(val) if val else ""
        else:
            if isinstance(orig_obj, dict):
                for f in orig_obj.keys():
                    val = orig_obj.get(f, "")
                    cast_obj[f] = str(val) if val else ""
            else:
                for f in dict(orig_obj):
                    val = getattr(orig_obj, f, "")
                    cast_obj[f] = str(val) if val else ""

        new_arr.append(cast_obj)
    return new_arr


def order_by_dict_keys(lst):
    def sort_dict_keys(dct):
        return {k: dct[k] for k in sorted(dct.keys())}

    return [sort_dict_keys(d) for d in lst]


def sort_objects(objects: List, sort_by: dict):
    def compare(item1, item2):
        for key, order in sort_by.items():
            val1 = getattr(item1, key)
            val2 = getattr(item2, key)
            # If values are strings or enums, convert to lower case for comparison
            if isinstance(val1, str):
                val1 = val1.lower()
            if isinstance(val1, Enum):
                val1 = val1.value

            if isinstance(val2, str):
                val2 = val2.lower()
            if isinstance(val2, Enum):
                val2 = val2.value

            if val1 is None:
                return 1
            if val2 is None:
                return -1
            if val1 < val2:
                return -1 if order in ["asc", "1"] else 1
            elif val1 > val2:
                return 1 if order in ["asc", "1"] else -1
        return 0

    if len(sort_by) == 0:
        return objects
    else:
        return sorted(objects, key=cmp_to_key(compare))
