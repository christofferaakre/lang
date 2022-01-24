#!/usr/bin/env python3
import sys

from ops import *
from lex import lex_program
from utils import print_usage
from simulation import simulate_program
from compilation import compile_program

def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print_usage(1)

    program_filename = args[0]
    mode = args[1]

    args = args[2:]

    program = lex_program(program_filename)

    if mode == "simulate":
        simulate_program(program, args)

    elif mode == "compile":
        compile_program(program, args)

    else:
        print_usage(1)

if __name__ == "__main__":
    main()
