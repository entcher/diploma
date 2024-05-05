def find_dicts_difference(dict1: dict[str, int], dict2: dict[str, int]) -> dict[str, int]:
    difference = dict1.copy()
    intersection_keys = dict1.keys() & dict2.keys()
    for key in intersection_keys:
        difference[key] = dict1[key] - dict2[key]
    return difference
