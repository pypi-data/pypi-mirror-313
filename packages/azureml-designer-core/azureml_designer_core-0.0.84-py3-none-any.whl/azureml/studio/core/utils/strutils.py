import re
import uuid
import zlib
from itertools import chain
from keyword import iskeyword
from string import Formatter
from collections import Iterable
import base64


def to_camel_case(input_str, lower_camel_case=False):
    """Given a string, convert it to CamelCase.

    >>> to_camel_case('hello_world')
    'HelloWorld'
    >>> to_camel_case('_hello_world')
    'HelloWorld'
    >>> to_camel_case('__hello_world')
    'HelloWorld'
    >>> to_camel_case('hello_world', lower_camel_case=True)
    'helloWorld'
    >>> to_camel_case('HelloWorld', lower_camel_case=True)
    'helloWorld'
    >>> to_camel_case('Hello, World!', lower_camel_case=True)
    'helloWorld'

    :param input_str: The input string.
    :param lower_camel_case: Generate lower camel case if True.
    :return: The converted camel case style string.
    """
    first, *others = split_to_words(input_str)
    return ''.join(chain(
        first.lower() if lower_camel_case else first.title(),
        map(str.title, others),
    ))


def to_lower_camel_case(input_str):
    """Given a string, convert to lower camel case.

    >>> to_lower_camel_case('hello_world')
    'helloWorld'
    >>> to_lower_camel_case('_hello_world')
    'helloWorld'
    >>> to_lower_camel_case('__hello_world')
    'helloWorld'
    >>> to_lower_camel_case('HelloWorld')
    'helloWorld'
    """
    return to_camel_case(input_str, lower_camel_case=True)


def to_snake_case(input_str):
    """Given a string, change it to snake case.

    >>> to_snake_case('CamelCase')
    'camel_case'
    >>> to_snake_case('CamelCamelCase')
    'camel_camel_case'
    >>> to_snake_case('Camel2Camel2Case')
    'camel2_camel2_case'
    >>> to_snake_case('getHTTPResponseCode')
    'get_http_response_code'
    >>> to_snake_case('get2HTTPResponseCode')
    'get2_http_response_code'
    >>> to_snake_case('HTTPResponseCode')
    'http_response_code'
    >>> to_snake_case('HTTPResponseCodeXYZ')
    'http_response_code_xyz'
    >>> to_snake_case('hello_world')
    'hello_world'
    >>> to_snake_case('__hello_world')
    'hello_world'

    :param input_str: Input string.
    :return: The converted snake case style string.
    """
    return '_'.join(s.lower() for s in split_to_words(input_str))


def split_to_words(input_str, break_underscores=True, break_camel_case_words=True):
    """Given a sentence, split to a list of words, removing any punctuations.

    >>> split_to_words('Hello, world!')
    ['Hello', 'world']
    >>> split_to_words('42: the answer to life, universe and everything')
    ['42', 'the', 'answer', 'to', 'life', 'universe', 'and', 'everything']
    >>> split_to_words('HelloWorld')
    ['Hello', 'World']
    >>> split_to_words('GetHTTPResponseCodeAsAString is a long function name.')
    ['Get', 'HTTP', 'Response', 'Code', 'As', 'A', 'String', 'is', 'a', 'long', 'function', 'name']
    >>> split_to_words('GetHTTPResponseCodeAsAString is a long function name.', break_camel_case_words=False)
    ['GetHTTPResponseCodeAsAString', 'is', 'a', 'long', 'function', 'name']
    >>> split_to_words('__hello__world__')
    ['hello', 'world']
    >>> split_to_words('__hello__world__', break_underscores=False)
    ['__hello__world__']

    :param input_str: The input string.
    :param break_underscores: break underscore connected words if specified.
    :param break_camel_case_words: break CamelCase word into multiple separated words.
    """
    # Replace punctuations and underscores to white spaces
    result = re.sub(r'\W', ' ', input_str)

    # Replace underscores if needed
    if break_underscores:
        result = re.sub(r'_', ' ', result)

    # Break CamelCase words if needed
    if break_camel_case_words:
        # Input Sample: 'GetHTTPResponseAsAString'
        # Step1: Add a space before '1 uppercase letter, with 1-n lowercase letters' pattern
        # Sample Result: 'GetHTTP ResponseCode AsA String'
        step1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1 \2', result)

        # Step2: Add a space between 'lowercase letter (or digit) and uppercase letter' pattern
        # Sample Result: 'Get HTTP Response As A String'
        result = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', step1)

    return result.split()


def to_cli_option_str(input_str):
    """Given a human readable string, convert to an CLI command option string.

    >>> to_cli_option_str('Input Dataset')
    '--input-dataset'
    >>> to_cli_option_str('Input DataSet')
    '--input-data-set'
    >>> to_cli_option_str('Number of iterations')
    '--number-of-iterations'
    """
    hyphenated = '-'.join(split_to_words(input_str))
    return '--' + hyphenated.lower()


def to_variable_name(input_str, converter=None, separator=''):
    """Given a human readable string, convert to a string that is suitable to be a variable name.

    >>> to_variable_name('Input DataSet')
    'InputDataSet'
    >>> to_variable_name('Number of iterations', converter=str.title)
    'NumberOfIterations'
    >>> to_variable_name('Number of iterations', converter=str.upper, separator='_')
    'NUMBER_OF_ITERATIONS'

    :param input_str: Input string to be converted.
    :param converter: The preprocessor for each word of the input string.
    :param separator: The separator to join each word.
    :return: The result string that is suitable to be a variable name.
    """
    words = split_to_words(input_str)
    if converter:
        words = [converter(w) for w in words]
    return separator.join(words)


def int_str_to_int_list(string, sep=','):
    """
    Convert string in format of '1, 3, 4, ..., ' to integer list [1,2,3,4,....]
    :param string: str. After being split by sep, each item in list can be converted to integer.
    :param sep: str. Delimiter string.
    :return:
    """
    items = string.split(sep)
    try:
        ret = [int(x) for x in items]
    except ValueError:
        return None
    return ret


def float_str_to_float_list(string, sep=','):
    """
    Convert string in format of '1.0, 2.0, 3.0, ..., ' to float list [1.0,2.0,3.0,....]
    :param string: str. After being split by sep, each item in list can be converted to float.
    :param sep: str. Delimiter string.
    :return:
    """
    items = string.split(sep)
    try:
        ret = [float(x) for x in items if x != '']
    except ValueError:
        return None
    return ret


def join_stripped(*args, sep=' '):
    """
    Same as str.join, but strip each element, skipping empty strings or None

    >>> join_stripped('hello', 'world')
    'hello world'
    >>> join_stripped('  hello    ', ' world ')
    'hello world'
    >>> join_stripped('a', 'b', '', 'd')
    'a b d'
    >>> join_stripped('', 'b', '')
    'b'
    >>> join_stripped(None, 'b')
    'b'
    >>> join_stripped('a', None, None, '', ' ', 'f')
    'a f'

    :param args: strings to be joined
    :param sep: separator
    :return: joined string
    """
    return sep.join([a.strip() for a in args if a and a.strip()])


def quote(obj, quote_mark='"', skip_quote_if_empty=True):
    """
    Return a quoted string.

    >>> quote('a')
    '"a"'
    >>> quote('hello world')
    '"hello world"'
    >>> quote('single quote', quote_mark="'")
    "'single quote'"
    >>> quote(1)
    '"1"'
    >>> quote('')
    ''
    >>> quote(None) is None
    True
    >>> quote('', skip_quote_if_empty=False)
    '""'
    >>> quote(None, skip_quote_if_empty=False)
    '"None"'

    :param obj: obj to be quoted, usually is a string.
    :param quote_mark: quote mark.
    :param skip_quote_if_empty: do not quote if given obj is empty or None.
    :return: Quoted string.
    """
    if not obj and skip_quote_if_empty:
        return obj

    return f"{quote_mark}{obj}{quote_mark}"


def generate_cls_str(obj, *meta_segments, with_obj_id=True):
    """
    A utility method to generate a __str__ result for an given object.

    Output will in the following form:
        <ClassName Meta Segments at id_of_obj>

    Example:
        <DataTable "name" (205 Rows, 26 Cols) at 0x000000000B29A290>
        Where meta segment 1 is '"name"', meta segment 2 is '(205 Rows, 26 Cols)'.

    :param obj: the obj itself calling __str__().
    :param meta_segments: meta segments to be displayed in __str__() result.
    :param with_obj_id: include obj id if specified.
    :return: obj's __str__() result.
    """
    class_name = obj.__class__.__name__
    obj_id = f"at 0x{id(obj):016X}" if with_obj_id else None
    return f'<{join_stripped(class_name, *meta_segments, obj_id)}>'


def truncate_lines(long_str: str, max_line_count=2,
                   trim_start_empty_lines=True, trim_end_empty_lines=True, max_line_length=-1):
    """
    Truncate multi line strings to a limited lines.
    Lines in the middle will be truncated and replaced with a placeholder.
    Truncate long lines to limited length.
    Chars in the middle of a line will truncated and replaced with a placeholder.

    >>> truncate_lines('''first line
    ... second line
    ... third line
    ... fourth line
    ... fifth abcdefghijklmnopqrstuvwxyz1234 line''', max_line_length=11)
    'first line\\n... (omitted 3 lines) ...\\nfifth ... (omitted 30 chars) ... line'

    :param long_str: multi line string to be truncated.
    :param max_line_count: max line count after truncate. only for content, placeholder is not counted.
    :param trim_start_empty_lines: trim start empty lines if specified.
    :param trim_end_empty_lines: trim end empty lines if specified.
    :param max_line_length: max length of line after truncate. only for content, placeholder is not counted.
    :return: truncated lines string.
    """
    if not long_str:
        return long_str

    if not isinstance(long_str, str):
        raise TypeError(f"Expected <str> but got {type(long_str)}")

    if max_line_count < 2:
        raise ValueError(f"max_line_count is not supposed to be less than 2. (got {max_line_count})")

    lines = long_str.splitlines()

    if trim_start_empty_lines:
        while len(lines) > 0 and not lines[0].strip():
            lines.pop(0)

    if trim_end_empty_lines:
        while len(lines) > 0 and not lines[-1].strip():
            lines.pop(-1)

    valid_line_count = len(lines)

    line_placeholder = f"... (omitted {valid_line_count - max_line_count} lines) ..."
    bottom_line_count = max_line_count // 2
    top_line_count = max_line_count - bottom_line_count

    def inner_truncate_line(line, length_limit):
        if length_limit <= 0:
            return line
        return truncate_string(line, length_limit)

    if valid_line_count <= max_line_count:
        truncated_lines = (inner_truncate_line(line, max_line_length) for line in lines)
    else:
        truncated_lines = chain((inner_truncate_line(line, max_line_length) for line in lines[:top_line_count]),
                                (line_placeholder,),
                                (inner_truncate_line(line, max_line_length) for line in lines[-bottom_line_count:]))

    result = '\n'.join(truncated_lines)
    return result


def truncate_string(string: str, max_str_length: int):
    """
    Truncate long string to limited length.

    >>> truncate_string('''123 abcdefghijklmnopqrstuvwxyz12 456''', max_str_length=6)
    '123... (omitted 30 chars) ...456'

    :param string: string to be truncated.
    :param max_str_length: max length of string after truncate. only for content, placeholder is not counted.
    :return: truncated string
    """

    if not isinstance(string, str):
        raise TypeError(f"Expected <str> but got {type(string)}")

    if max_str_length <= 0:
        raise ValueError(f"max_str_length is not supposed to be less than 1. Got {max_str_length}")

    omit_count = len(string) - max_str_length
    char_placeholder = f"... (omitted {omit_count} chars) ..."

    if omit_count <= len(char_placeholder):
        return string

    rear_char_count = max(max_str_length // 2, 1)
    head_char_count = max_str_length - rear_char_count
    string = string[:head_char_count] + char_placeholder + string[-rear_char_count:]
    return string


def is_multi_lined(string: str):
    """
    Given a string, judge if the string is multi-lined.

    >>> is_multi_lined('single line')
    False
    >>> is_multi_lined('''multi
    ... line''')
    True

    :param string: string to be judged.
    :return: True if string is multi-lined, False otherwise.
    """

    if not string:
        return False

    if not isinstance(string, str):
        raise TypeError(f"Expected <str> but got type{string}")

    lines = string.splitlines()
    return len(lines) > 1


def indent_block(str_to_indent: str, prefix='', subsequent_prefix=None):
    """
    Given a string, add prefix for each lines to get the string block indented.

    First line prefix and subsequent line prefix can be differ.
    if no subsequent prefix specified, defaults to have the same value as first line prefix.

    >>> a = '''multi
    ... lined
    ... string'''
    >>> print(a)
    multi
    lined
    string
    >>> print(indent_block(a, prefix=' >  '))
     >  multi
     >  lined
     >  string
    >>> print(indent_block(a, prefix=' >  ', subsequent_prefix=' .  '))
     >  multi
     .  lined
     .  string
    >>> b = 'single line'
    >>> indent_block(b, prefix=' >  ')
    ' >  single line'

    Note:
     1) We did not use `textwrap.indent()` because we want to be able to specify
        different prefixes for first line and subsequent lines.
     2) We did not use `textwrap.TextWrapper()` because `TextWrapper` will wrap up
        long lines (exceeds 70 characters by default), which is not our intent.

    So we 'invented' this `indent_block()`.

    :param str_to_indent: string to be indented, either single line or multiple line.
    :param prefix: prefix to be added to each lines.
    :param subsequent_prefix: if we want to have a different prefix for first line and subsequent lines,
                              specify subsequent prefix here. if not specified, take the same value from `prefix`.
    :return: the indented string.
    """
    if not str_to_indent:
        return str_to_indent

    if not isinstance(str_to_indent, str):
        raise TypeError(f"Expected <str> but got type{str_to_indent}")

    if subsequent_prefix is None:
        subsequent_prefix = prefix

    lines = str_to_indent.splitlines()

    def _prefix(line_no):
        return prefix if line_no == 0 else subsequent_prefix

    indented_lines = [_prefix(line_no) + line for line_no, line in enumerate(lines)]

    return '\n'.join(indented_lines)


def get_args_from_template(template):
    """
    Given a string template, return a tuple represents the args inside the template.
    Only named arguments are supported.

    >>> get_args_from_template('{hello} {world}')
    ('hello', 'world')
    >>> get_args_from_template('How are you, {name}?')
    ('name',)
    >>> get_args_from_template('Not supported for positional arguments {0}')
    Traceback (most recent call last):
    ...
    ValueError: Invalid identifier "0" in template "Not supported for positional arguments {0}"
    >>> get_args_from_template('Not supported for invalid parameters {1a}')
    Traceback (most recent call last):
    ...
    ValueError: Invalid identifier "1a" in template "Not supported for invalid parameters {1a}"
    >>> get_args_from_template('Not supported for python keywords {if}')
    Traceback (most recent call last):
    ...
    ValueError: Identifier "if" cannot be python keyword in template "Not supported for python keywords {if}"

    :param template:
    :return:
    """
    parsed = Formatter().parse(template)
    names = tuple(p[1] for p in parsed if p[1] is not None)
    for name in names:
        if not name.isidentifier():
            raise ValueError(f"Invalid identifier {quote(name)} in template {quote(template)}")
        if iskeyword(name):
            raise ValueError(f"Identifier {quote(name)} cannot be python keyword in template {quote(template)}")
    return names


def remove_prefix(text, prefix=None):
    """
    Given a string, removes specified prefix, if it has.

    >>> remove_prefix('hello world', 'world')
    'hello world'
    >>> remove_prefix('hello world', 'hello ')
    'world'
    >>> remove_prefix('alghost_0.0.67', 'alghost_')
    '0.0.67'

    :param text: string from which prefix will be removed.
    :param prefix: prefix to be removed.
    :return: string removed prefix.
    """
    if not text or not prefix:
        return text

    if not text.startswith(prefix):
        return text

    return text[len(prefix):]


def remove_suffix(text, suffix=None):
    """
    Given a string, removes specified suffix, if it has.

    >>> remove_suffix('hello world', 'world')
    'hello '
    >>> remove_suffix('hello world', 'hello ')
    'hello world'
    >>> remove_suffix('NoColumnFoundError', 'Error')
    'NoColumnFound'

    :param text: string from which prefix will be removed.
    :param suffix: suffix to be removed.
    :return: string removed suffix.
    """
    if not text or not suffix:
        return text

    if not text.endswith(suffix):
        return text

    return text[:-len(suffix)]


def parse_version_str(version: str):
    """
    Parse a version string into a value tuple.

    >>> parse_version_str('0.0.50')
    (0, 0, 50)
    >>> parse_version_str('1.0.0')
    (1, 0, 0)

    :param version: Version string
    :return: Version value tuple
    """
    if not version:
        raise ValueError(f"Input version cannot be empty.")

    if not isinstance(version, str):
        raise TypeError(f"Expected version to be a string but got a {type(version)}.")

    parts = version.split('.')
    if len(parts) not in (3, 4):
        raise ValueError(f"Version string '{version}' must be in 3 or 4 digital segments.")

    if not all(p.isdigit() for p in parts):
        raise ValueError(f"Version string '{version}' must contains only digits in each segment.")

    return tuple(int(p) for p in parts)


def generate_random_string():
    return str(uuid.uuid4().hex)


def profile_column_names(column_names_list, n=16):
    """Build a string contains first n column names.

    :param column_names_list: list-like object
    :param n: int, first n column
    :return: str, first n column names are joint with ','.
                  If the list has more than n items, an ellipsis will be added to the end of the string.
    """
    if not hasattr(column_names_list, '__getitem__'):
        raise ValueError(f"column_names_list should be subscriptable.")
    if isinstance(column_names_list, dict):
        raise ValueError(f"column_names_list could not be dict")
    string = ','.join(column_names_list[:n])
    if column_names_list[n:]:
        # If the column_names list has more than n items, add an ellipsis.
        string = string + ',...'
    return string


def add_suffix_number_to_avoid_repetition(input_str: str, existed_str_lst, starting_suffix_number: int = 0):
    """
    Add a number as suffix to input string to avoid repetition if it is in a list.
    After adding suffix number, if the new string is still in the list, suffix number will be auto-incremented by 1.

    >>> add_suffix_number_to_avoid_repetition('a', ['b', 'a'], 0)
    'a_0'
    >>> add_suffix_number_to_avoid_repetition('a', ['a', 'a_1'], 1)
    'a_2'
    >>> add_suffix_number_to_avoid_repetition('a', ['b', 'c'], 0)
    'a'

    :param input_str: input string
    :param existed_str_lst: input string lst to check if input string is included
    :param starting_suffix_number: int, suffix integer to begin with
    """
    if not isinstance(input_str, str):
        raise TypeError('Input parameter "input_str" must be string type.')

    if not isinstance(existed_str_lst, list):
        raise TypeError('Input parameter "existed_str_lst" must be a list.')

    if not isinstance(starting_suffix_number, int):
        raise TypeError('Input parameter "starting_suffix_number" must be integer type.')

    suffix_number = starting_suffix_number
    if input_str in existed_str_lst:
        str_with_suffix_number = input_str + f'_{suffix_number}'
        while str_with_suffix_number in existed_str_lst:
            suffix_number += 1
            str_with_suffix_number = input_str + f'_{suffix_number}'
        return str_with_suffix_number

    else:
        return input_str


def add_suffix_number_to_avoid_repetition_by_batch(input_strs: Iterable, existed_strs: Iterable,
                                                   starting_suffix_number: int = 0):
    """
    Add a number as suffix to input strings to avoid repetition if any input string in the existed strings.
    After adding suffix number, if the new strings are still in the existed strings, suffix number will be
    auto-incremented by 1.

    >>> add_suffix_number_to_avoid_repetition_by_batch(['a','b'],['a','c'],1)
    ['a_1', 'b_1']
    >>> add_suffix_number_to_avoid_repetition_by_batch(['a'],['b','c'],1)
    ['a']
    >>> add_suffix_number_to_avoid_repetition_by_batch(('a','c'),('c','b'),0)
    ['a_0', 'c_0']

    :param input_strs: input strings
    :param existed_strs: existed strings to check if any input strings are included
    :param starting_suffix_number: int, suffix integer to begin with
    """
    if not isinstance(input_strs, Iterable):
        raise TypeError('Input parameter "input_strs" must be iterable type.')
    if not isinstance(existed_strs, Iterable):
        raise TypeError('Input parameter "existed_strs" must be iterable type.')
    if not isinstance(starting_suffix_number, int):
        raise TypeError('Input parameter "starting_suffix_number" must be integer type.')

    existed_str_set = set(existed_strs)
    suffix_number = starting_suffix_number

    new_input_strs = input_strs
    while not existed_str_set.isdisjoint(new_input_strs):
        new_input_strs = [f"{s}_{suffix_number}" for s in input_strs]
        suffix_number += 1

    return new_input_strs


def decode_base64_string(base64_string: str):
    """
    Decode a base64-encoded string into bytes.

    >>> decode_base64_string('YmFzZTY0IGVuY29kZWQgc3RyaW5n')
    b'base64 encoded string'

    :param base64_string: base64-encoded string
    :return: Bytes object
    """
    return base64.b64decode(base64_string, validate=True)


def compress_string_to_bytes(input_str: str):
    """  Encode input string into bytes with utf-8 encoding and compress. """
    return zlib.compress(input_str.encode('utf-8'))


def compress_and_base64_encode_string(input_str: str):
    """ Compress string into bytes and encode the bytes into base64 string. """
    return base64.b64encode(compress_string_to_bytes(input_str)).decode('utf-8')


def decompress_base64_string(input_str: str):
    """ Decode base64-encoded string into bytes and decompress the bytes into string. """
    return zlib.decompress(decode_base64_string(input_str)).decode('utf-8')


def decode_script_string(input_str: str):
    """
    Script string might be directly passing without special handling,
    or be zipped and base64-encoded before passing.
    Either way, this function returns the original string.

    >>> decode_script_string('SimpleString')
    'SimpleString'
    >>> decode_script_string(compress_and_base64_encode_string('Compressed and encoded string!'))
    'Compressed and encoded string!'
    >>> decode_script_string('')
    ''
    >>> decode_script_string(compress_and_base64_encode_string(''))
    ''
    """
    # noinspection PyBroadException
    try:
        return decompress_base64_string(input_str)
    except Exception:
        return input_str
