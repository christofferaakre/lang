#!/usr/bin/env python3
import pathlib
import sys
import subprocess

# 'root directory' is location of the main.py script
# this way, we can use relative paths no matter where
# the script is executed from
root_directory = str(pathlib.Path(__file__).parent.resolve())

# implementing golang style enumeration
# because python enum is kinda cringe
IOTA_COUNTER = 0
def iota(reset=False):
    global IOTA_COUNTER
    if reset:
        IOTA_COUNTER = 0
    num = IOTA_COUNTER
    IOTA_COUNTER += 1
    return num

# operations
OP_PUSH = iota()
OP_ADD = iota()
OP_SUB = iota()
OP_MULTIPLY = iota()
OP_DIVIDE = iota()
OP_DUMP = iota()
OP_DUP = iota()
OP_SWAP = iota()
OP_IF = iota()
OP_ELSE = iota()
OP_END = iota()
OP_WHILE = iota()
OP_EQUAL = iota()
OP_GREATER_THAN = iota()
OP_LESS_THAN = iota()
OP_GREATER_THAN_OR_EQUAL = iota()
OP_LESS_THAN_OR_EQUAL = iota()
OP_COUNT = iota()

def get_contents_of_file(filename):
    contents = ''
    with open(root_directory + "/" + filename, "r") as file:
        contents = file.read()
    return contents

# this function parses a program file
# and splits up into individual operations
def lex_program(program_filename: str) -> list:
    program = []
    ip_stack = []
    with open(program_filename, "r") as program_file:
        lines = program_file.readlines()
        instruction_pointer = 0
        for line_number, line in enumerate(lines):
            # ignore whitespace
            line = ' '.join(line.split())
            # skip empty lines
            if len(line) == 0:
                continue
            instructions = line.replace('\n', '').split(' ')


            for instruction in instructions:
                #print(instruction_pointer, instruction)
                assert OP_COUNT == 17, "Must handle alll instructions in lex_program"
                if instruction == "#":
                    break


                elif instruction == "+":
                   op = (OP_ADD, )
                   program.append(op)
                elif instruction == "-":
                   op = (OP_SUB, )
                   program.append(op)

                elif instruction == "*":
                    op = (OP_MULTIPLY, )
                    program.append(op)

                elif instruction == "/":
                    op = (OP_DIVIDE, )
                    program.append(op)

                elif instruction == "dump":
                   op = (OP_DUMP, )
                   program.append(op)

                elif "dup" in instruction:
                    op = None
                    if instruction == "dup":
                        op = (OP_DUP, )
                    else:
                        op = (OP_DUP, int(instruction.replace("dup", "")))
                    program.append(op)

                elif instruction == "if":
                   op = (OP_IF, )
                   ip_stack.append({"type": OP_IF, "ip": instruction_pointer})
                   program.append(op)

                elif instruction == "swap":
                    op = (OP_SWAP, )
                    program.append(op)

                elif instruction == "else":
                    op = (OP_ELSE, )
                    # make previous if instruction jump
                    # to just after this else if condition
                    # is false
                    start_of_block = ip_stack.pop()["ip"]

                    program[start_of_block] = (program[start_of_block][0],instruction_pointer + 1)
                    program.append(op)

                    ip_stack.append({"type": OP_ELSE, "ip": instruction_pointer})

                elif instruction == "end":
                   op = None

                   # make else jump directly to end
                   reference = ip_stack.pop()
                   ip = reference["ip"]
                   if reference["type"] == OP_WHILE:
                       # if end closes a while loop, connect the while to the
                       # end and the end to the while
                       program[ip] = (program[ip][0], instruction_pointer + 1)
                       op = (OP_END, ip)
                       program.append(op)
                   else:
                       # if end closes a if or else, simply connect the if or
                       # else to the end
                       program[ip] = (program[ip][0], instruction_pointer + 1)
                       op = (OP_END, )
                       program.append(op)

                elif instruction == "while":
                    op = (OP_WHILE, )
                    ip_stack.append({"type": OP_WHILE, "ip": instruction_pointer})
                    program.append(op)


                elif instruction == "=":
                    op = (OP_EQUAL, )
                    program.append(op)

                elif instruction == ">":
                    op = (OP_GREATER_THAN, )
                    program.append(op)

                elif instruction == "<":
                    op = (OP_LESS_THAN, )
                    program.append(op)

                elif instruction == ">=":
                    op = (OP_GREATER_THAN_OR_EQUAL, )
                    program.append(op)

                elif instruction == "<=":
                    op = (OP_LESS_THAN_OR_EQUAL, )
                    program.append(op)


                else:
                   try:
                       number = int(instruction)
                       op = (OP_PUSH, number)
                       program.append(op)
                   except ValueError as error:
                       print(f"Error on line {line_number+1}: Invalid operator {instruction}. Error: {error}. Exiting with code 1")
                       exit(1)

                instruction_pointer += 1



    # print(program)
    return program

# simulate program in python
def simulate_program(program, args):
    #return
    stack = []
    instruction_pointer = 0
    while instruction_pointer < len(program):
        op = program[instruction_pointer]

        verbose = False
        if verbose:
            print(f"stack: {stack}")
            print(f"instruction: {op}")
            print(f"instruction pointer: {instruction_pointer}")
            print("\n")

        assert OP_COUNT == 17, "Must handle all instructions in simulate_program"
        if op[0] == OP_PUSH:
            assert len(op) >= 2, "Operation OP_PUSH needs an argument to push onto the stack"
            stack.append(int(op[1]))
            instruction_pointer += 1
        elif op[0] == OP_ADD:
            a = stack.pop()
            b = stack.pop()
            stack.append(b + a)
            instruction_pointer += 1
        elif op[0] == OP_SUB:
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)
            instruction_pointer += 1

        elif op[0] == OP_MULTIPLY:
            a = stack.pop()
            b = stack.pop()
            stack.append(b * a)
            instruction_pointer += 1

        elif op[0] == OP_DIVIDE:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(b / a))
            instruction_pointer += 1

        elif op[0] == OP_DUMP:
            a = stack.pop()
            print(a)
            instruction_pointer += 1

        elif op[0] == OP_DUP:
            index = -op[1] if len(op) >= 2 else -1
            a = stack[index]
            stack.append(a)
            instruction_pointer += 1

        elif op[0] == OP_SWAP:
            a = stack.pop()
            b = stack.pop()

            stack.append(a)
            stack.append(b)

            instruction_pointer += 1

        elif op[0] == OP_IF:
            assert len(op) >= 2, "Operation OP_IF must have a label to jump to in case the condition is false"
            a = stack.pop()
            if a != 0:
                instruction_pointer += 1
            else:
                instruction_pointer = op[1]

        elif op[0] == OP_ELSE:
            assert len(op) >= 2, "Operation OP_ELSE, must have a label to jump to when it is reached"

            instruction_pointer = op[1]

        elif op[0] == OP_END:
            # if OP_END has a label to jump to, jump to it,
            # else just go to the next instruction
            if len(op) >= 2:
                instruction_pointer = op[1]
            else:
                instruction_pointer += 1

        elif op[0] == OP_WHILE:
            assert len(op) >= 2, "Operation OP_WHILE must have a label to jump to when the condition is false"
            condition = stack[-1]
            if condition == 0:
                instruction_pointer = op[1]
            else:
                instruction_pointer += 1

        elif op[0] == OP_EQUAL:
            a = stack.pop()
            b = stack.pop()
            if (b == a):
                stack.append(1)
            else:
                stack.append(0)
            instruction_pointer += 1

        elif op[0] == OP_GREATER_THAN:
            a = stack.pop()
            b = stack.pop()
            if (b > a):
                stack.append(1)
            else:
                stack.append(0)
            instruction_pointer += 1

        elif op[0] == OP_LESS_THAN:
            a = stack.pop()
            b = stack.pop()
            if (b < a):
                stack.append(1)
            else:
                stack.append(0)
            instruction_pointer += 1

        elif op[0] == OP_GREATER_THAN_OR_EQUAL:
            a = stack.pop()
            b = stack.pop()
            if (b >= a):
                stack.append(1)
            else:
                stack.append(0)
            instruction_pointer += 1

        elif op[0] == OP_LESS_THAN_OR_EQUAL:
            a = stack.pop()
            b = stack.pop()
            if (b <= a):
                stack.append(1)
            else:
                stack.append(0)
            instruction_pointer += 1

def compile_program(program, args):
    out_filename = None
    if len(args) >= 1:
        if '.asm' in args[0]:
            out_filename = args[0].replace('.asm', '')
        else:
            print_usage(1)

    if not out_filename:
        out_filename = "out"

    with open(out_filename + ".asm", "w") as out_file:
        # boiler plate for assembly code
        out_file.write("BITS 64\n")
        out_file.write(get_contents_of_file("inc/printint.inc"))
        out_file.write("\n")
        out_file.write("\n")
        out_file.write("\n")

        out_file.write("section .bss\n")
        out_file.write("    digitSpace resb 100\n")
        out_file.write("    digitSpacePos resb 8\n")
        out_file.write("\n")

        out_file.write("section .text\n")

        out_file.write("    global _start:\n")
        out_file.write("\n")

        out_file.write("_start:\n")

        instruction_pointer = 0
        while instruction_pointer < len(program):
            op = program[instruction_pointer]
            out_file.write(f"_addr{instruction_pointer}:\n")
            instruction_pointer += 1

            assert OP_COUNT == 16, "Must handle all instructions in compile_program"
            if op[0] == OP_PUSH:
                assert len(op) >= 2, "Operation OP_PUSH needs an argument to push onto the stack"
                out_file.write(f"    ;; PUSH {op[1]} ;;\n")
                out_file.write(f"    push {op[1]}\n\n")

            elif op[0] == OP_ADD:
                out_file.write(f"    ;; ADD ;;\n")
                out_file.write(f"    pop rax\n")
                out_file.write(f"    pop rbx\n")
                out_file.write(f"    add rbx, rax\n")
                out_file.write(f"    push rbx\n\n")
            elif op[0] == OP_SUB:
                out_file.write(f"    ;; SUB ;;\n")
                out_file.write(f"    pop rax\n")
                out_file.write(f"    pop rbx\n")
                out_file.write(f"    sub rbx, rax\n")
                out_file.write(f"    push rbx\n\n")
            elif op[0] == OP_MULTIPLY:
                out_file.write(f"    ;; MULTIPLY ;;\n")
                out_file.write(f"    pop rax\n");
                out_file.write(f"    pop rbx\n");
                out_file.write(f"    mul rbx\n");
                out_file.write(f"    push rax\n\n");
            elif op[0] == OP_DUMP:
                out_file.write(f"    ;; DUMP ;;\n")
                out_file.write(f"    pop rax\n")
                out_file.write(f"    call _printRAX\n")
                out_file.write("\n")

            elif op[0] == OP_DUP:
                if len(op) >= 2 and op[1] > 1:
                    # if op[1] is e.g. 2, we want to duplicate the second element
                    print(f"compiling dup{op[1]}")
                    out_file.write(f"    mov rax, [rsp+{8 * (op[1] - 1)}]\n")
                    out_file.write(f"    push rax\n\n")
                    # raise NotImplementedError

                else:
                    print(f"compiling regular dup")
                    out_file.write("    pop rax\n")
                    out_file.write("    push rax\n")
                    out_file.write("    push rax\n")
                    # out_file.write("    push rax\n")

            elif op[0] == OP_SWAP:
                out_file.write("    ;; swap ;;\n")
                out_file.write("    pop rax\n")
                out_file.write("    pop rbx\n")
                out_file.write("    push rax\n")
                out_file.write("    push rbx\n")

            elif op[0] == OP_IF:
                assert len(op) >= 2, "Operation OP_IF must have a label to jump to if the condition is false"
                out_file.write("    ;; if ;;\n")
                out_file.write("    pop rax\n")
                out_file.write("    test rax, rax\n")
                out_file.write(f"   jz _addr{op[1]}\n")

            elif op[0] == OP_ELSE:
                assert len(op) >= 2, "Operation OF_ELSE must have a label to jump to if the instruction is reached"
                out_file.write(f"    ;; else ;; \n")
                out_file.write(f"    jmp _addr{op[1]}\n")

            elif op[0] == OP_END:
                out_file.write("    ;; end ;;\n")
                if len(op) >= 2:
                    out_file.write(f"    jmp _addr{op[1]}\n")

            elif op[0] == OP_WHILE:
                out_file.write(f"    ;; while ;; \n")
                out_file.write(f"    mov rax, [rsp]\n")
                out_file.write(f"    test rax, rax\n")
                out_file.write(f"    jz _addr{op[1]}\n")

            elif op[0] == OP_EQUAL:
                out_file.write("    ;; = ;;\n")
                out_file.write("    pop rax\n")
                out_file.write("    pop rbx\n")
                out_file.write("    cmp rbx, rax\n")

                out_file.write("    mov rbx, 1\n")
                out_file.write("    mov rdx, 0\n")
                out_file.write("    cmove rdx, rbx\n")
                out_file.write("    push rdx\n")

            elif op[0] == OP_GREATER_THAN:
                out_file.write("    ;; > ;;\n")
                out_file.write("    pop rax\n")
                out_file.write("    pop rbx\n")
                out_file.write("    cmp rbx, rax\n")

                out_file.write("    mov rbx, 1\n")
                out_file.write("    mov rdx, 0\n")
                out_file.write("    cmovg rdx, rbx\n")
                out_file.write("    push rdx\n")


            elif op[0] == OP_LESS_THAN:
                out_file.write("    ;; < ;;\n")
                out_file.write("    pop rax\n")
                out_file.write("    pop rbx\n")
                out_file.write("    cmp rbx, rax\n")

                out_file.write("    mov rbx, 1\n")
                out_file.write("    mov rdx, 0\n")
                out_file.write("    cmovl rdx, rbx\n")
                out_file.write("    push rdx\n")

            elif op[0] == OP_GREATER_THAN_OR_EQUAL:
                out_file.write("    ;; >= ;;\n")
                out_file.write("    pop rax\n")
                out_file.write("    pop rbx\n")
                out_file.write("    cmp rbx, rax\n")

                out_file.write("    mov rbx, 1\n")
                out_file.write("    mov rdx, 0\n")
                out_file.write("    cmovge rdx, rbx\n")
                out_file.write("    push rdx\n")

            elif op[0] == OP_LESS_THAN_OR_EQUAL:
                out_file.write("    ;; <= ;;\n")
                out_file.write("    pop rax\n")
                out_file.write("    pop rbx\n")
                out_file.write("    cmp rbx, rax\n")

                out_file.write("    mov rbx, 1\n")
                out_file.write("    mov rdx, 0\n")
                out_file.write("    cmovle rdx, rbx\n")
                out_file.write("    push rdx\n")

        # address after last instruciton
        out_file.write(f"_addr{len(program)}:\n")

        # boilerplate code to exit
        out_file.write("    ;; EXIT ;; \n")
        out_file.write("    mov rax, 60\n")
        out_file.write("    mov rdi, 0\n")
        out_file.write("    syscall\n")

    # calling nasm
    subprocess.run(["nasm", "-f", "elf64", "-o", out_filename + ".o",
        out_filename + ".asm"])
    print(f"$ nasm -f elf64 -o {out_filename}.o {out_filename}.asm")

    # calling ld
    subprocess.run(["ld", out_filename + ".o", "-o", out_filename])
    print(f"$ ld {out_filename}.o -o {out_filename}")

    print(f"Compiled succesfully. Run with ./{out_filename}")


def print_usage(exit_code=None):
        print("Usage: ./main.py <program> [simulate | compile <out-file>]")
        if exit_code:
            exit(exit_code)

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
