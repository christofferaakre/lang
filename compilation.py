from ops import *
from utils import get_contents_of_file, print_usage
import subprocess

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

            assert OP_COUNT == 26, "Must handle all instructions in compile_program"

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
            elif op[0] == OP_PRINT:
                write(f"    ;; PRINT ;;\n")
                write(f"    pop rax\n")
                write(f"    call _printRAXNoNewLine\n")
                write("\n")

            elif op[0] == OP_PRINTS:
                raise NotImplementedError
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
        out_file.write(get_contents_of_file("inc/dump.inc"))
        out_file.write(get_contents_of_file("inc/print.inc"))
        out_file.write("\n")
        out_file.write("\n")
        out_file.write("\n")

        # user defined subroutines
        out_file.write(subroutine_instructions)

        out_file.write("section .bss\n")
        out_file.write("    digitSpace resb 100\n")
        out_file.write("    digitSpacePos resb 8\n")
        out_file.write("    digitSpace2 resb 100\n")
        out_file.write("    digitSpacePos2 resb 8\n")

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
