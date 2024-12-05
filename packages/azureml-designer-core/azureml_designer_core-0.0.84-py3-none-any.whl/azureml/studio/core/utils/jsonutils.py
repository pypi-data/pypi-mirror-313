import json
import os

from azureml.studio.core.utils.fileutils import ensure_folder


INDENT = 2


def dump_to_json(obj, stream, indent=INDENT, sort_keys=False):
    json.dump(obj, stream, indent=indent, sort_keys=sort_keys)


def dump_to_json_file(obj, filename, indent=INDENT, sort_keys=False):
    ensure_folder(os.path.dirname(os.path.abspath(filename)))
    with open(filename, 'w') as fout:
        dump_to_json(obj, fout, indent=indent, sort_keys=sort_keys)


def load_json(stream):
    return json.load(stream)


def load_json_file(filename):
    with open(filename, 'r') as fin:
        return load_json(fin)


def load_json_lines(filename):
    with open(filename, 'r') as fin:
        return [json.loads(line) for line in fin]


def dump_to_json_lines(json_list, filename):
    lines = [json.dumps(val) + '\n' for val in json_list]
    ensure_folder(os.path.dirname(os.path.abspath(filename)))
    with open(filename, 'w') as fout:
        fout.writelines(lines)


JSON_TYPES = {int, float, str, bool, type(None), dict, list}


def json_equals(data1, data2, precision=0, raise_error_for_inequality=False):
    """
    Compare two json objects at a certain precision threshold to avoid floating number precision error.

    >>> data1 = {'floatval': 1.0010}
    >>> data2 = {'floatval': 1.0014}
    >>> json_equals(data1, data2)
    False
    >>> json_equals(data1, data2, 0.001)
    True
    """
    if not type(data1) in JSON_TYPES:
        raise TypeError(f"Object of type {data1.__class__.__name__} is not JSON serializable")
    if not type(data2) in JSON_TYPES:
        raise TypeError(f"Object of type {data2.__class__.__name__} is not JSON serializable")

    # Both int and float are "number type" in json
    if type(data1) != type(data2) and {type(data1), type(data2)} != {float, int}:
        if raise_error_for_inequality:
            raise AssertionError(f"Type '{type(data1)}' is not equal to type {type(data2)}")
        return False

    if isinstance(data1, list):
        if len(data1) != len(data2):
            if raise_error_for_inequality:
                raise AssertionError(f"List '{data1}' is not equal to list '{data2}'")
            return False
        for item1, item2 in zip(data1, data2):
            if not json_equals(item1, item2, precision, raise_error_for_inequality):
                return False

    elif isinstance(data1, dict):
        if len(data1) != len(data2):
            if raise_error_for_inequality:
                raise AssertionError(f"Dict '{data1}' is not equal to dict '{data2}'")
            return False
        for k, item1 in data1.items():
            if k not in data2:
                if raise_error_for_inequality:
                    raise AssertionError(f"Dict '{data1}' is not equal to dict '{data2}'")
                return False
            if not json_equals(item1, data2[k], precision, raise_error_for_inequality):
                return False

    elif data1 is None or isinstance(data1, (str, bool)):
        if not data1 == data2:
            if raise_error_for_inequality:
                raise AssertionError(f"Value '{data1}' is not equal to value '{data2}'")
            return False

    # Comparing numbers
    else:
        if not abs(data1 - data2) <= precision:
            if raise_error_for_inequality:
                raise AssertionError(f"Number '{data1}' is not equal to number '{data2}' with precision '{precision}'")
            return False

    return True
