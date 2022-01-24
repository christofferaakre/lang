import pathlib
from typing import Tuple

def get_contents_of_file(filename):
    root_directory = str(pathlib.Path(__file__).parent.resolve())
    contents = ''
    with open(root_directory + "/" + filename, "r") as file:
        contents = file.read()
    return contents

def print_usage(exit_code=None):
        print("Usage: ./main.py <program> [simulate | compile <out-file>]")
        if exit_code:
            exit(exit_code)

def string_to_nasm_string(string: str) -> Tuple[str, int]:
    length = len(string)
    nasm_string = '"'
    for char in string:
        if char == '\n':
            nasm_string += '",10'
        else:
            if nasm_string.endswith('",10'):
                nasm_string += ',"'
            nasm_string += char
    if not nasm_string.endswith(',10'):
        nasm_string += '"'
    return nasm_string, length
