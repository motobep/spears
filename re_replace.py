import re
from consts import *

def format_regex(pattern: str, string: str) -> str:
    return pattern.format(string.replace('.', r'\.'))
    

def replace_with(data: str, regex: str, target: str) -> str:
    lines = data.splitlines(True)
    new_data = ''
    for line in lines:
        new_data += re.sub(regex, target, line)

    return new_data


def replace_keyword_import(data: str, to_str: str, regex: str) -> str:
    target = fr'import \1{to_str}'
    lines = data.splitlines(True)
    new_data = ''
    for line in lines:
        if re.search(regex, line) and ' as ' in line:
            raise Exception('Found "as" in non-as-import')
        else:
            new_data += re.sub(regex, target, line)
    return new_data


def replace_namespace_of_import(data: str, to_str: str, regex: str, regex_in_string: str) -> str:
    target = fr'{to_str}.'
    lines = data.splitlines(True)
    new_data = ''
    for line in lines:
        if re.search(regex, line):
            if "'" in line or '"' in line:
                if not re.search(regex_in_string, line):
                    new_data += re.sub(regex, target, line)
                else:
                    new_data += line
                    raise Exception('Can\'t handle quotes problem')
            else:
                new_data += re.sub(regex, target, line)
        else:
            new_data += line

    return new_data


def replace_as_import(data: str, to_str: str, regex: str) -> str:
    target = fr'import {to_str} as \2'
    return replace_with(data, regex, target)


def replace_from_import(data: str, to_str: str, regex: str) -> str:
    target = f'from {to_str} import '
    return replace_with(data, regex, target)
