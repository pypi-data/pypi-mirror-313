def get_value_by_key_path(dct, key_path, default_value=None):
    """Given a dict, get value from key path.

    >>> dct = {
    ...     'Beijing': {
    ...         'Haidian': {
    ...             'ZipCode': '110108',
    ...         }
    ...     }
    ... }
    >>> get_value_by_key_path(dct, 'Beijing/Haidian/ZipCode')
    '110108'
    """
    if not key_path:
        raise ValueError("key_path must not be empty")

    segments = key_path.split('/')
    final_flag = object()
    segments.append(final_flag)

    walked = []

    cur_obj = dct
    for seg in segments:
        # If current segment is final_flag,
        # the cur_obj is the object that the given key path points to.
        # Simply return it as result.
        if seg is final_flag:
            # return default_value if cur_obj is None
            return default_value if cur_obj is None else cur_obj

        # If still in the middle of key path, when cur_obj is not a dict,
        # will fail to locate the values
        if not isinstance(cur_obj, dict):
            # TODO: maybe add options to raise exceptions here in the future
            return default_value

        # Move to next segment
        cur_obj = cur_obj.get(seg)
        walked.append(seg)

    raise RuntimeError("Should never go here")


def sorted_dict(dct):
    """Given a dict, get a result dict with keys sorted, recursively.

    >>> dct = {
    ...     'c': {
    ...         'c2': 3.2,
    ...         'c1': 3.1,
    ...     },
    ...     'b': 2,
    ...     'a': 1,
    ...     'd': [
    ...         {
    ...             'd-d': 414,
    ...             'd-c': 413,
    ...         },
    ...         {
    ...             'd-b': 402,
    ...             'd-a': 401,
    ...         },
    ...     ]
    ... }
    >>> sorted_dict(dct)
    {'a': 1, 'b': 2, 'c': {'c1': 3.1, 'c2': 3.2}, 'd': [{'d-c': 413, 'd-d': 414}, {'d-a': 401, 'd-b': 402}]}
    """
    if isinstance(dct, dict):
        return {k: sorted_dict(dct[k]) for k in sorted(dct)}
    elif isinstance(dct, list):
        return [sorted_dict(d) for d in dct]
    else:
        return dct
