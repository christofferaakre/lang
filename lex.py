from ops import *

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
            string = ''
            for instruction in instructions:
                #print(instruction_pointer, instruction)
                assert OP_COUNT == 26, "Must handle all instructions in lex_program"
                if '"' in instruction:
                    s = instruction
                    s = instruction.replace('"', '')
                    s = s.replace('\\n', '\n')
                    s = s.replace('\\t', '\t')
                    s = s.replace('\\r', '\r')
                    s = s.replace('\\40', '\40')

                    if instruction.endswith('"'):
                        string += ' ' + s
                        op = (OP_PRINTS, string)
                        program.append(op)
                        string = ''
                    else:
                        string += s



                elif string:
                    s = instruction
                    string += ' ' + s

                elif "#" in instruction:
                    break

                elif 'pop' in instruction:
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

                elif instruction == "print":
                    op = (OP_PRINT, )
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
