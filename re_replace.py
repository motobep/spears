import re
from consts import *

def format_regex(pattern: str, string: str) -> str:
    return pattern.format(string.replace('.', r'\.'))
    

def print_diff(line: str, new_line: str) -> None:
    print(line[:-1], ' -->', new_line[:-1])

def replace_with(data: str, regex: str, target: str) -> str:
    lines = data.splitlines(True)
    new_data = ''
    for line in lines:
        if re.search(regex, line):
            new_line = re.sub(regex, target, line)
            new_data += new_line
            print_diff(line, new_line)
        else:
            new_data += line

    return new_data


def replace_keyword_import(data: str, to_str: str, regex: str) -> str:
    target = TARGET_KEYWORD_PATTERN.format(to_str)
    lines = data.splitlines(True)
    new_data = ''
    for line in lines:
        searched = re.search(regex, line)
        if searched and ' as ' in line:
            raise Exception('Found "as" in non-as-import')
        elif searched:
            new_line = re.sub(regex, target, line)
            new_data += new_line
            print_diff(line, new_line)
        else:
            new_data += line
    return new_data


def replace_namespace_of_import(data: str, to_str: str, regex: str, regex_in_string: str) -> str:
    target = fr'{to_str}.'
    lines = data.splitlines(True)
    new_data = ''
    for line in lines:
        if re.search(regex, line):
            if "'" in line or '"' in line:
                if not re.search(regex_in_string, line):
                    new_line = re.sub(regex, target, line)
                    new_data += new_line
                    print_diff(line, new_line)
                else:
                    new_data += line
                    raise Exception('Can\'t handle quotes problem')
            else:
                new_line = re.sub(regex, target, line)
                new_data += new_line
                print_diff(line, new_line)
        else:
            new_data += line

    return new_data


def replace_as_import(data: str, to_str: str, regex: str) -> str:
    target = fr'import {to_str} as \2'
    return replace_with(data, regex, target)


def replace_from_import(data: str, to_str: str, regex: str) -> str:
    target = f'from {to_str} import '
    return replace_with(data, regex, target)
