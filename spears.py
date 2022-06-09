#!/bin/python
import os
import sys
import subprocess
import re
from argparse import ArgumentParser
import re_replace as rrep
from consts import *
from ReplaceImports import ReplaceImports


def init_parser_args():
    parser = ArgumentParser(description='Move python file and change imports')
    parser.add_argument('-f', '--source-file', dest='file',
                        help='Source file', metavar='filename')
    parser.add_argument('-d', '--source-dir', dest='dir',
                        help='Source directory', metavar='directory name')
    parser.add_argument('-t', '--target-dir', dest='target_dir', required=True,
                        help='Target directory', metavar='directory name')
    parser.add_argument('--is-test', dest='is_test', action='store_true',
                        help='Should be a test')
    return parser.parse_args()


def get_directory(path: str) -> str:
    arr = path.split('/')[:-1]
    return '/'.join(arr)


def convert_to_python_path(string: str) -> str:
    s = string.split('.')[0].replace('.', '') # drop extension and delete trailing '.'
    return s.replace('/', '.')


def search_files_grep(pattern) -> list[str]:
    result = subprocess.run(['egrep', '-rl', './', '-e', pattern, '--include=*.py'], stdout=subprocess.PIPE)
    s = result.stdout.decode('utf-8')
    return s[:-1].split('\n')


def remove_empty_strings(arr: list[str]) -> list[str]:
    return [s for s in arr if s != '']

def find_files(string: str) -> list[str]:
    return remove_empty_strings(search_files_grep(string))


def add_slash_or_not(string: str) -> str:
    return string if string[-1] == '/' else f'{string}/'


def check_intersection(a, b, c):
    l2 = list(set(a).intersection(c))
    l3 = list(set(c).intersection(b))
    if l2 != [] or l3 != []:
        raise Exception('Found intersection')


def make_relative_imports_versions(python_import):
    arr = []
    spi_arr = python_import.split('.')
    # print('Possible relative paths:')
    for i in range(1, len(spi_arr) + 1):
        substr = '.'.join(spi_arr[-i:])
        arr.append('.' + substr)
        # print(arr[-1])
    return arr


def check_relative_imports(python_import: str) -> bool:
    imports = make_relative_imports_versions(python_import)

    for pimport in imports:
        regex_import = rrep.format_regex(FROM_IMPORT_PATTERN, pimport)
        arr = find_files(regex_import)
        if arr != []:
            return True

    return False


def check_relative_imports_of_target(source_path: str) -> bool:
    with open(source_path, 'r') as fin:
        for line in fin:
            if re.search(LOCAL_FROM_IMPORT_REGEX, line):
                return True

    return False


def get_files_of_dir(directory: str) -> list[str]:
    """ Returns list of python filenames in the directory """
    return [(directory + f) for f in os.listdir(
        directory) if os.path.isfile(os.path.join(directory, f)) and '.py' == f[-3:]]


def move_file(file, target_dir, is_test):
    source_path = file
    is_init_file = INIT_FILE == source_path[-len(INIT_FILE):]
    if is_init_file:
        # Handle init file
        source_dir_path = get_directory(source_path)
        source_python_import = convert_to_python_path(source_dir_path)
        print('Handling __init__.py')
        print(f'{source_python_import=}')
    else:
        source_python_import = convert_to_python_path(source_path)

    if check_relative_imports(source_python_import):
        print('There are relative imports of target file')
        print('Aborting')
        exit(-1)

    if check_relative_imports_of_target(source_path):
        print('Relative imports inside target file')
        print('Aborting')
        exit(-1)

    # print(f'{source_python_import=}')
    target_path = target_dir + source_path.split('/')[-1]
    if is_init_file:
        target_python_import = convert_to_python_path(target_dir[:-1]) # remove /
    else:
        target_python_import = convert_to_python_path(target_path)
    print(f'-------\nTarget python import: {target_python_import}\n-------')

    # exit()

    ''' Change imports '''
    regex_import = rrep.format_regex(IMPORT_PATTERN, source_python_import)
    found_usual_imports = find_files(regex_import)
    # print(f'{found_usual_imports=}')

    regex_as_import = rrep.format_regex(AS_IMPORT_PATTERN, source_python_import)
    found_as_imports = find_files(regex_as_import)

    regex_from_import = rrep.format_regex(FROM_IMPORT_PATTERN, source_python_import)
    found_from_imports = find_files(regex_from_import)

    regex_namespace_import = rrep.format_regex(NAMESPACE_OF_IMPORT, source_python_import)
    regex_in_string = rrep.format_regex(IMPORT_IN_STRING, source_python_import)

    check_intersection(found_usual_imports, found_as_imports, found_from_imports)


    replace_imports = ReplaceImports(is_test, target_python_import)

    '''As-imports'''
    print('\n\nAs-imports:')
    replace_imports.change(found_as_imports, 
        {'func': rrep.replace_as_import, 'args': [regex_as_import]},
    )

    '''Ordinary imports'''
    print('\n\nUsual imports:')
    replace_imports.multichange(found_usual_imports, [
        {'func': rrep.replace_keyword_import, 'args': [regex_import]},
        {'func': rrep.replace_namespace_of_import, 'args': [regex_namespace_import, regex_in_string]},
    ])

    '''From imports'''
    print('\n\nFrom-imports:')
    replace_imports.change(found_from_imports, 
        {'func': rrep.replace_from_import, 'args': [regex_from_import]},
    )

    ''' Move file '''
    if not is_test:
        os.rename(source_path, target_path)



def main():
    args = init_parser_args()
    if not (3 >= len(sys.argv[1:]) >= 2):
        print('Specify source path and target directory!')
        exit(-1)

    # print(args)
    IS_TEST = args.is_test
    print('is_test:', IS_TEST)

    if args.file is None and args.dir is None:
        print('Specify source!')
        exit()

    target_dir = add_slash_or_not(args.target_dir)

    if args.file is not None:
        move_file(args.file, target_dir, IS_TEST)
    elif args.dir is not None:
        files = get_files_of_dir(args.dir)
        print('Directory files:', files)
        for file in files:
            move_file(file, target_dir, IS_TEST)
        
if __name__ == '__main__':
    main()


# Rubbish
# return r'^from .* import +(\w+, *)*' + f'({result})' + '(,|$)'
"""

    line = 'from test import     test0,       tesst, test2'
    regex = r'^from ' + f'({source_python_import})' + r' +import *'
    target = f'from {target_python_import} import '
    new_data = ''
    new_data += re.sub(regex, target, line)
    # print(new_data)
    # exit()
"""
