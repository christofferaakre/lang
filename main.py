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
OP_PUSH_VAR = iota()
OP_POP = iota()
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
OP_NOT = iota()
OP_EXIT = iota()
OP_MACRO = iota()
OP_RET = iota()
OP_CALL = iota()
#
OP_COUNT = iota()
#

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
                assert OP_COUNT == 24, "Must handle alll instructions in lex_program"
                if instruction == "#":
                    break

                if 'pop' in instruction:
                    split = instruction.split(':')
                    if len(split) == 1:
                        op = (OP_POP, )
                        program.append(op)
                    if len(split) == 2:
                        var_name = split[1]
                        op = (OP_POP, var_name)
                        program.append(op)

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

                elif 'macro:' in instruction:
                    split = instruction.split(':')
                    assert len(split) == 2, "OP_MACRO must have name of macro"
                    macro_name = split[1]
                    op = (OP_MACRO, macro_name)
                    program.append(op)


                elif instruction == 'ret':
                    op = (OP_RET, )
                    program.append(op)

                elif 'call:' in instruction:
                    split = instruction.split(':')
                    assert len(split) == 2, "OP_CALL must have name of macro to call"
                    macro_name = split[1]
                    op = (OP_CALL, macro_name)
                    program.append(op)

                elif instruction == "exit":
                    op = (OP_EXIT, )
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

                elif instruction == "not":
                    op = (OP_NOT, )
                    program.append(op)

                elif instruction.startswith("$"):
                    var_name = instruction[1:]
                    op = (OP_PUSH_VAR, var_name)
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
    stack = []
    ip_stack = []
    vars_dict = {}
    # This dict stores the location of the definition
    # of each macro
    macros_dict = {}

    # keeps track of whether or not we should immediately
    # execute instructions
    execute = True
    instruction_pointer = 0
    while instruction_pointer < len(program):
        op = program[instruction_pointer]

        verbose = False
        if verbose:
            print(f"execute: {execute}")
            print(f"instruction: {op}")
            print(f"stack: {stack}")
            # print(f"Vars: {vars_dict}")
            print(f"Macros: {macros_dict}")
            print(f"instruction pointer: {instruction_pointer}")
            print()

        assert OP_COUNT == 24, "Must handle all instructions in simulate_program"

        if op[0] == OP_MACRO:
            assert len(op) == 2, "OP_MACRO must have name of macro"
            macro_name = op[1]
            location = instruction_pointer + 1
            macros_dict[macro_name] = location
            instruction_pointer += 1
            execute = False

        elif op[0] == OP_RET:
            if execute:
                # jump to the return address on the stack
                instruction_pointer = ip_stack.pop()
            else:
                # if not executing, the ret is the end of the macro
                # definition, so we set execute to True and increment the
                # instruction pointer
                instruction_pointer += 1
                execute = True

        # if we are not defining a macro and execute is False,
        # we dont need to do anything
        elif not execute:
            instruction_pointer += 1
            continue

        elif op[0] == OP_CALL:
            assert len(op) == 2, "OP_CALL must have name of macro to call"
            macro_name = op[1]
            return_address = instruction_pointer + 1
            ip_stack.append(return_address)
            jump_location = macros_dict[macro_name]
            instruction_pointer = jump_location


        elif op[0] == OP_PUSH:
            assert len(op) >= 2, "Operation OP_PUSH needs an argument to push onto the stack"
            stack.append(int(op[1]))
            instruction_pointer += 1
        if op[0] == OP_POP:
            value = stack.pop()
            if len(op) == 2:
                var_name = op[1]
                vars_dict[var_name] = value

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
            ratio = b // a
            remainder = b % a
            # put remainder on top of stack,
            # and ratio just below
            stack.append(ratio)
            stack.append(remainder)
            instruction_pointer += 1

        elif op[0] == OP_DUMP:
            a = stack.pop()
            print(a)
            instruction_pointer += 1

        elif op[0] == OP_EXIT:
            exit_code = 0
            if len(stack) > 0:
                exit_code = stack.pop()

            exit(exit_code)


        elif op[0] == OP_DUP:
            index = -op[1] if len(op) >= 2 else -1
            a = stack[index]
            stack.append(a)
            instruction_pointer += 1

        elif op[0] == OP_SWAP:
            if len(stack) >= 2:
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

        elif op[0] == OP_NOT:
            a = stack.pop()
            if a == 0:
                stack.append(1)
            else:
                stack.append(0)
            instruction_pointer += 1

        elif op[0] == OP_PUSH_VAR:
            assert len(op) == 2, "OP_PUSH_VAR must have name of variable"
            var_name = op[1]
            value = vars_dict[var_name]
            stack.append(value)
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

    # this dict maps string variable names to integer
    # indices. For example, the first variable allocated
    # gets index 0, the second one gets index 1, etc.
    # These indices are used to know where to read
    # and write memory
    vars_dict = {}
    index = 0

    with open(out_filename + ".asm", "w") as out_file:

        # string to hold subroutine definitions
        subroutine_instructions = ''
        # string to hold all other instructions
        instructions = ''
        # keep track of whether we are currently defining
        # a subroutine or executing instructions
        subroutine = False

        def write(instruction: str) -> None:
            nonlocal subroutine_instructions, instructions, subroutine
            if subroutine:
                subroutine_instructions += instruction
            else:
                instructions += instruction

        instruction_pointer = 0
        while instruction_pointer < len(program):
            op = program[instruction_pointer]
            write(f"_addr{instruction_pointer}:\n")
            instruction_pointer += 1

            assert OP_COUNT == 24, "Must handle all instructions in compile_program"

            if op[0] == OP_MACRO:
                assert not subroutine, "Nested subroutines are not allowed for this language"
                assert len(op) == 2, "OP_MACRO must have name of macro"
                macro_name = op[1]
                subroutine = True
                write(f"_{macro_name}:\n")
                # we use the r14 variable to keep track of
                # the return address that automatically gets pushed onto the
                # stack when a subroutine is called. This way, we can modify
                # the stack in any way we like inside the subroutine
                write(f"    add r10, 8\n")
                write(f"    pop r14\n")
                write(f"    mov [returnstack+r10], r14\n")

            elif op[0] == OP_RET:
                assert subroutine, "Can only return from inside a subroutine"
                # push the return address back onto the stack just before
                # returning out of the subroutine
                write(f"mov r14, [returnstack+r10]\n")
                write(f"push r14\n")
                write(f"sub r10, 8\n")
                write(f"ret\n")
                subroutine = False

            elif op[0] == OP_CALL:
                assert len(op) == 2, "OP_CALL must have name of macro to call"
                macro_name = op[1]
                write(f"call _{macro_name}\n")

            elif op[0] == OP_PUSH:
                assert len(op) >= 2, "Operation OP_PUSH needs an argument to push onto the stack"
                write(f"    ;; PUSH {op[1]} ;;\n")
                write(f"    push {op[1]}\n\n")

            elif op[0] == OP_POP:
                if len(op) == 1:
                    write(f"    ;; POP ;;\n")
                    write(f"    pop r13\n\n")
                elif len(op) == 2:
                    var_name = op[1]
                    # give the variable the right index
                    # if it is a new variable. If it is an
                    # old variable being redefined, we don't
                    # need to do anything

                    write(f"    ;; POP:{var_name} ;;\n")
                    write(f"    pop r13\n")
                    write(f"    mov [memory+{8*index}], r13\n")

                    if not var_name in vars_dict:
                        vars_dict[var_name] = index
                        index += 1

            elif op[0] == OP_ADD:
                write(f"    ;; ADD ;;\n")
                write(f"    pop rax\n")
                write(f"    pop rbx\n")
                write(f"    add rbx, rax\n")
                write(f"    push rbx\n\n")
            elif op[0] == OP_SUB:
                write(f"    ;; SUB ;;\n")
                write(f"    pop rax\n")
                write(f"    pop rbx\n")
                write(f"    sub rbx, rax\n")
                write(f"    push rbx\n\n")
            elif op[0] == OP_MULTIPLY:
                write(f"    ;; MULTIPLY ;;\n")
                write(f"    pop rax\n");
                write(f"    pop rbx\n");
                write(f"    imul rbx\n");
                write(f"    push rax\n\n");
            elif op[0] == OP_DIVIDE:
                write(f"    ;; DIVIDE ;;\n")
                write(f"    pop rbx\n")
                write(f"    pop rax\n")
                # Required to avoid SIGFPE
                write(f"    mov rdx, 0\n")
                write(f"    idiv rbx\n")
                # ratio goes in rax and remainder goes in rdx
                write(f"    push rax\n")
                write(f"    push rdx\n")
            elif op[0] == OP_DUMP:
                write(f"    ;; DUMP ;;\n")
                write(f"    pop rax\n")
                write(f"    call _printRAX\n")
                write("\n")
            elif op[0] == OP_EXIT:
                write("    ;; EXIT ;;\n")
                write("    mov rax, 60\n")
                write("    pop rdi\n")
                write("    syscall\n\n")

            elif op[0] == OP_DUP:
                if len(op) >= 2 and op[1] > 1:
                    # if op[1] is e.g. 2, we want to duplicate the second element
                    print(f"compiling dup{op[1]}")
                    write(f"    mov rax, [rsp+{8 * (op[1] - 1)}]\n")
                    write(f"    push rax\n\n")
                    # raise NotImplementedError

                else:
                    print(f"compiling regular dup")
                    write("    pop rax\n")
                    write("    push rax\n")
                    write("    push rax\n")
                    # write("    push rax\n")

            elif op[0] == OP_SWAP:
                write("    ;; swap ;;\n")
                write("    pop rax\n")
                write("    pop rbx\n")
                write("    push rax\n")
                write("    push rbx\n")

            elif op[0] == OP_IF:
                assert len(op) >= 2, "Operation OP_IF must have a label to jump to if the condition is false"
                write("    ;; if ;;\n")
                write(f"    pop rax\n")
                write("    test rax, rax\n")
                write(f"   jz _addr{op[1]}\n")

            elif op[0] == OP_ELSE:
                assert len(op) >= 2, "Operation OF_ELSE must have a label to jump to if the instruction is reached"
                write(f"    ;; else ;; \n")
                write(f"    jmp _addr{op[1]}\n")

            elif op[0] == OP_END:
                write("    ;; end ;;\n")
                if len(op) >= 2:
                    write(f"    jmp _addr{op[1]}\n")

            elif op[0] == OP_WHILE:
                write(f"    ;; while ;; \n")
                write(f"    mov rax, [rsp]\n")
                write(f"    test rax, rax\n")
                write(f"    jz _addr{op[1]}\n")

            elif op[0] == OP_EQUAL:
                write("    ;; = ;;\n")
                write("    pop rax\n")
                write("    pop rbx\n")
                write("    cmp rbx, rax\n")

                write("    mov rbx, 1\n")
                write("    mov rdx, 0\n")
                write("    cmove rdx, rbx\n")
                write("    push rdx\n")

            elif op[0] == OP_GREATER_THAN:
                write("    ;; > ;;\n")
                write("    pop rax\n")
                write("    pop rbx\n")
                write("    cmp rbx, rax\n")

                write("    mov rbx, 1\n")
                write("    mov rdx, 0\n")
                write("    cmovg rdx, rbx\n")
                write("    push rdx\n")


            elif op[0] == OP_LESS_THAN:
                write("    ;; < ;;\n")
                write("    pop rax\n")
                write("    pop rbx\n")
                write("    cmp rbx, rax\n")

                write("    mov rbx, 1\n")
                write("    mov rdx, 0\n")
                write("    cmovl rdx, rbx\n")
                write("    push rdx\n")

            elif op[0] == OP_GREATER_THAN_OR_EQUAL:
                write("    ;; >= ;;\n")
                write("    pop rax\n")
                write("    pop rbx\n")
                write("    cmp rbx, rax\n")

                write("    mov rbx, 1\n")
                write("    mov rdx, 0\n")
                write("    cmovge rdx, rbx\n")
                write("    push rdx\n")

            elif op[0] == OP_LESS_THAN_OR_EQUAL:
                write("    ;; <= ;;\n")
                write("    pop rax\n")
                write("    pop rbx\n")
                write("    cmp rbx, rax\n")

                write("    mov rbx, 1\n")
                write("    mov rdx, 0\n")
                write("    cmovle rdx, rbx\n")
                write("    push rdx\n")

            elif op[0] == OP_NOT:
                write(f"    ;; NOT ;;\n")
                write(f"    pop rax\n")
                write(f"    cmp rax, 0\n")
                write(f"    je _push1_{instruction_pointer}\n")
                write(f"    _push0_{instruction_pointer}:\n")
                write(f"        push 0\n")
                write(f"        jmp _finally_{instruction_pointer}\n")
                write(f"    _push1_{instruction_pointer}:\n")
                write(f"        push 1\n")
                write(f"        jmp _finally_{instruction_pointer}\n")
                write(f"_finally_{instruction_pointer}:\n")


            elif op[0] == OP_PUSH_VAR:
                assert len(op) == 2, "OP_PUSH_VAR must have name of variable"
                var_name = op[1]
                index = vars_dict[var_name]
                write(f"    ;; PUSH_VAR {var_name} ;;\n")
                write(f"    mov rax, [memory+{8 * index}]\n")
                write(f"    push rax\n")


        # boiler plate for assembly code
        out_file.write("BITS 64\n")
        out_file.write(get_contents_of_file("inc/printint.inc"))
        out_file.write("\n")
        out_file.write("\n")
        out_file.write("\n")

        # user defined subroutines
        out_file.write(subroutine_instructions)

        out_file.write("section .bss\n")
        out_file.write("    digitSpace resb 100\n")
        out_file.write("    digitSpacePos resb 8\n")

        # Numbers are stored as 8-bit longs, so
        # 800 bytes for example gets us 100 numbers
        out_file.write("    memory resb 800\n")
        out_file.write("\n")

        out_file.write("    returnstack resb 800\n\n")

        out_file.write("section .text\n")

        out_file.write("    global _start:\n")
        out_file.write("\n")

        out_file.write("_start:\n")
        out_file.write("    mov r10, -1\n")
        out_file.write(instructions)

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
