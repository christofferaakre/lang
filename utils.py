import pathlib

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
