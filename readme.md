# lang
`lang` is a simple stack based programming language
written in Python. It can either be interpreted in Python,
or be compiled to `x86_64` assembly code using `nasm`. Note that
the compiled executables will only run on 64 bit linux distributions
since linux syscalls are used, although the Python simulation mode
should work on all modern operating systems.

## Installation
1. Clone repository
2. Make sure you have `nasm` and `ld` in your path as these
are used for compiling programs
3. Install python dependcies:
    * `pip install pathlib`
4. Try to run one of the example files:
    * Try to simulate: `./main.py examples/fib/fib.lang -s` and <br>
    * Try to compile: `./main.py examples/fib/fib.lang -c examples/fib/fib`
    * Try to run the compiled file: `./examples/fib/fib`
5. Add the `main.py` to your system path somehow, e.g. save a bash script called `lang` in your `~/bin`:
    ```bash
    ~/coding/lang/main.py "$@"
    ```
    Then, you can do `lang -h]` to see the help for the compiler.

## Usage
Write a program with `.lang` extension, for example `program.lang`. Then you can either simulate
it in Python with `lang program.lang -s`.
You can compile it to `x86_64` assembly with `lang program.lang -c program`. The compiled
assembly code will be stored in the file specified, in this case `program.asm`. Additionally, an
object file `program.o` will be generated, and the actual executable, simply named `program` with
no extension. To run it, run `./program`.

## Command line options
This list may not be up to date. To see a list that is
definitely up to date, run `./main.py -h`.

| Option/Flag  | Description |
|:-:|---|
| `-h, --help`  | See help and options for the compiler  |
| `-c, --compile`  | Set the compiler to compilation mode, i.e. compile to x86\_64 assembly |
| `-s, --simulate`  | Set the compiler to simulation mode, i.e. simulate in python |
| `-v, --verbose`  | Run the compiler in verbose mode |
| `-o, --out-file`  | Output file for compiled binary |
| `-r, --run`  | Run the compiled binary file immidiately after compilation has finished |

## Syntax highlighting
If you use vim, you can get syntax highlighting by using the
syntax file `editor/lang.vim`. See the instructions in that file
if you are unsure about what to do with that file.

## Features
A program consists of a series of instructions. Instructions are
separated by spaces, and newlines and excess whitespace are ignored.
You can use `#` to type comments, anything afer a `#` will be ignored.

Currently the only type of data that is supported is signed integers.
Nested if-else blocks and loops are supported.

| Operation  | Syntax  | Description  |
|:-:|---|---|
| `PUSH`  | `int`  | Push a number onto the stack, i.e. `45` pushes the number 45 onto the stack  |
| `PUSH_VAR`  | `$myvar`  | Pushes the value of the `myvar` variable onto the stack|
| `POP`  | `pop[:optional_var_name]`  | `pop` pops the top number off the stack, and does nothing with it. `pop:myvar` pops the top number off the stack saves it in a variable called `myvar`|
| `ADD`  | `+`  | Pop the top two numbers off the stack, add them, and push the result back onto the stack  |
| `SUB`  | `-`  | Pop the top two numbers `a` and `b` off the stack, subtract them (`b - a`), then push the result onto the stack   |
| `MUL`  | `*`  | Pop the top two numbers `a` and `b` off the stack, multiply them, then push the result onto the stack   |
| `DIV`  | `/`  | Pop the top two numbers `a` and `b` off the stack and performs integer division `b // a` on them. Then, pushes the ratio and remainder onto the stack, in that order, so the remainder is on top.|
| `DUMP`  | `dump`  | Pop the top number off the stack, and print it to standard output with a newline character at the end|
| `PRINT`  | `print`  | Pop the top number off the stack, and print it to standard output. Same as `DUMP`l, but without the newline character at the end.|
| `PRINTS`  | `"my_string"`  | Print the given string to standard output, no newline character unless specified with `\n`. Spaces at the beginning of strings must be escaped using `\40`, for example "\40years old" if you want the string `" years old"`.|
| `EXIT`  | `exit`  | Pop the top number off the stack, and exit using that number as the exit code. If the stack is empty, use 0 as the exit code|
| `DUP`  | `dup[n]`  | `dup` will duplicate the top number on the stack and push it on top. `dup2` will duplicate the second number from the top and push it to the top of the stack. You can also do `dup3`, etc.|
| `SWAP`  | `swap`  | Swaps the two topmost numbers on the stack|
| `IF`  | `if`  | Pop the top number off the stack. If it is `0`, go to the next `else` or `end`. If it is nonzero, Go to the next instruction|
| `EQ`  | `=`  |Pops the top two numbers off the stack, and checks if they are equal. If they are, push `1` to the stack, otherwise push `0`.|
| `GE`  | `>`  |Pops the top two numbers off the stack, and checks if the second number is greater than the top number. If it is, push `1` to the stack, otherwise push `0`.|
| `GEQ`  | `>=`  |Pops the top two numbers off the stack, and checks if the second number is greater than or equal to the top number. If it is, push `1` to the stack, otherwise push `0`.|
| `LE`  | `<`  |Pops the top two numbers off the stack, and checks if the second number is less than the top number. If it is, push `1` to the stack, otherwise push `0`.|
| `LEQ`  | `<=`  |Pops the top two numbers off the stack, and checks if the second number is less than or equal to the top number. If it is, push `1` to the stack, otherwise push `0`.|
| `NOT`  | `not`  |Pops the top number off the stack. If it is 0, push 1 onto the stack, else push 0 onto the stack.|
| `ELSE`  | `else`  | If `if` fails, execution will jump to the `else` if one exists|
| `END`  | `end`  | Marks the end of an if-else block or a loop|
| `WHILE`  | `while`  |Peeks at the top number on the stack. If it is nonzero, execute the code until the next `end`. Then peek at the top number again and repeat until the top number is zero, then jump to the `end` |
| `MACRO`  | `macro:macroname`  |Starts a macro definition block. The macro can be called later with `call:macroname`|
| `RET`  | `ret`  |Returns out of the macro. Return values are not a thing in this language, instead you may push a value onto the stack before returning, and then pop it off after you call the macro. Conditional returns may work "by accident" only in simulation mode due to implementation details. They are *not* supported in either mode.|
| `CALL`  | `call:macroname`  |Call the macro with name `macroname`.|

## Examples
Code examples can be found in the `examples` directory, but here is an
example program that calculates the prime numbers less than or equal to 1000
and prints them to standard output:
```
# Print the prime numbers below 1000
macro:mod
    # second topmost number mod top number
    / swap pop
ret

macro:is_prime
    pop:n
    2 pop:counter
    1 while pop
        $n $counter call:mod
        $counter 1 + pop:counter
      end
    $counter 1 -
    $n =
    swap pop
    ret

# main code to calculate prime numbers
2 dup while pop
    dup call:is_prime
    f
        dup dump
    end
    1 +
   dup 1000 <=
end
```
