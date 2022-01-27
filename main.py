#!/usr/bin/env python3
import argparse

from ops import *
from lex import lex_program
from utils import print_usage
from simulation import simulate_program
from compilation import compile_program

def print_usage():
    print("Run the script with the -h flag for information on how to use it")

def main():
    parser = argparse.ArgumentParser(description="Simulate or compile code written in the lang language")
    parser.add_argument('input_file', metavar='input-file', type=str, help='File containing the program you want to simulate or compile')
    parser.add_argument('-c', '--compile', help="Compile the input file", action='store_true')
    parser.add_argument('-s', '--simulate', help="Simulate the input file", action='store_true')
    parser.add_argument('-v', '--verbose', help="Verbose mode", action='store_true')
    parser.add_argument('-o', '--out_file', metavar='out-file', help="Output file for compiled binary")
    parser.add_argument('-r', '--run', help="immediately run the compiled file", action='store_true')
    args = parser.parse_args()

    program_filename = args.input_file
    sim = args.simulate
    com = args.compile
    verbose = args.verbose
    out_file = args.out_file
    run = args.run

    arguments = {
            'verbose': verbose,
            'out_file': out_file,
            'run': run
            }

    if sim and com:
        print("Can't simulate and compile the program at the same time. Please provide only one of these options.")
        print_usage()
        exit(1)

    if (not sim) and (not com):
        print("Please specify whether you want to simulate (-s | --s) or compile (-c --c) the program")
        print_usage()
        exit(1)

    mode = 'sim' if sim else 'com'

    program = lex_program(program_filename)

    if mode == 'sim':
        simulate_program(program, arguments)

    elif mode == 'com':
        assert arguments['out_file'], "You must provide an output file for the compiler"
        compile_program(program, arguments)

if __name__ == "__main__":
    main()
