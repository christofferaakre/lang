from ops import *

def simulate_program(program, args):
    verbose = False

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

        if verbose:
            print(f"execute: {execute}")
            print(f"instruction: {op}")
            print(f"stack: {stack}")
            # print(f"Vars: {vars_dict}")
            print(f"Macros: {macros_dict}")
            print(f"instruction pointer: {instruction_pointer}")
            print()

        assert OP_COUNT == 26, "Must handle all instructions in simulate_program"

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

        elif op[0] == OP_PRINT:
            a = stack.pop()
            print(a, end="")
            instruction_pointer += 1

        elif op[0] == OP_PRINTS:
            assert len(op) == 2, "OP_PRINTS must have string to print"
            string = op[1]
            print(string, end="")
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
