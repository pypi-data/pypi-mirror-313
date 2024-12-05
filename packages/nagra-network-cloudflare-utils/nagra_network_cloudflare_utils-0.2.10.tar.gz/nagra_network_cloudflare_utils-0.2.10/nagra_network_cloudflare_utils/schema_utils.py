from itertools import islice, tee


def is_sorted(list, /, comparator=None, key=lambda x: x):
    if comparator is None:

        def comparator(lhs, rhs):
            return key(lhs) <= key(rhs)

    l1, l2 = tee(list, 2)
    l2 = islice(l2, 1, None)
    return all(comparator(r1, r2) for r1, r2 in zip(l1, l2))


def is_unique(list, /, key=lambda x: x):
    res = set()
    for x in list:
        k = key(x)
        if k in res:
            return False
        res.add(k)
    return True


def find_duplicates(list, /, key=lambda x: x):
    res = set()
    duplicates = set()
    for x in list:
        k = key(x)
        if k in res:
            if k not in duplicates:
                yield k
                duplicates.add(k)
        else:
            res.add(k)


def group(list, /, key=lambda x: x):
    groups = {}
    for x in list:
        k = key(x)
        records = groups.setdefault(k, [])
        records.append(x)
    return groups


def remap_keys(data, mapping):
    if isinstance(mapping, dict):
        mapping = mapping.items()
    return {new: data[old] for old, new in mapping if old in data}


def extract_keys(data, keys):
    return {k: data.get(k) for k in keys}
