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
    * Try to simulate: `./main.py examples/fib/fib.lang simulate` and <br>
    * Try to compile: `./main.py examples/dib/fib.lang compile examples/fib/fib.asm`
    * Try to run the compiled file: `./examples/fib/fib`
5. Add the `main.py` to your system path somehow, e.g. save a bash script called `lang` in your `~/bin`:
    ```bash
    ~/coding/lang/main.py "$@"
    ```
    Then, you can do `lang [program] [simulate | compile <out-file>]`

## Usage
Write a program with `.lang` extension, for example `program.lang`. Then you can either simulate
it in Python with `lang program.lang simulate`.
You can compile it to `x86_64` assembly with `lang program.lang compile program.asm`. The compiled
assembly code will be stored in the file specified, in this case `program.asm`. Additionally, an
object file `program.o` will be generated, and the actual executable, simply named `program` with
no extension. To run it, run `./program`.

## Features
`lang` (name not final) is a very simple stack based language, and currently does not have features you might
be used to like variables, etc. Instead, you work with a stack.
A program consists of a series of instructions. Instructions are
separated by spaces, and newlines and excess whitespace are ignored.
You can use `#` to type comments, anything afer a `#` will be ignored.

Currently the only type of data that is supported is signed integers.
Nested if-else blocks and loops are supported.

| Operation  | Syntax  | Description  |
|:-:|---|---|
| `PUSH`  | `int`  | Push a number onto the stack, i.e. `45` pushes the number 45 onto the stack  |
| `POP`  | `pop`  | Pop the top number off the stack|
| `ADD`  | `+`  | Pop the top two numbers off the stack, add them, and push the result back onto the stack  |
| `SUB`  | `-`  | Pop the top two numbers `a` and `b` off the stack, subtract them (`b - a`), then push the result onto the stack   |
| `MUL`  | `*`  | Pop the top two numbers `a` and `b` off the stack, multiply them, then push the result onto the stack   |
| `DIV`  | `/`  | Pop the top two numbers `a` and `b` off the stack and performs integer division `b // a` on them. Then, pushes the ratio and remainder onto the stack, in that order, so the remainder is on top.|
| `DUMP`  | `dump`  | Pop the top number off the stack, and print it to standard output|
| `DUP`  | `dup[n]`  | `dup` will duplicate the top number on the stack and push it on top. `dup2` will duplicate the second number from the top and push it to the top of the stack. You can also do `dup3`, etc.|
| `SWAP`  | `swap`  | Swaps the two topmost numbers on the stack|
| `IF`  | `if`  | Peeks at the top number off the stack. If it is `0`, go to the next `else` or `end`. If it is nonzero, Go to the next instruction|
| `EQ`  | `=`  |Pops the top two numbers off the stack, and checks if they are equal. If they are, push `1` to the stack, otherwise push `0`.|
| `GE`  | `>`  |Pops the top two numbers off the stack, and checks if the second number is greater than the top number. If it is, push `1` to the stack, otherwise push `0`.|
| `GEQ`  | `>=`  |Pops the top two numbers off the stack, and checks if the second number is greater than or equal to the top number. If it is, push `1` to the stack, otherwise push `0`.|
| `LE`  | `<`  |Pops the top two numbers off the stack, and checks if the second number is less than the top number. If it is, push `1` to the stack, otherwise push `0`.|
| `LEQ`  | `<=`  |Pops the top two numbers off the stack, and checks if the second number is less than or equal to the top number. If it is, push `1` to the stack, otherwise push `0`.|
| `ELSE`  | `else`  | If `if` fails, execution will jump to the `else` if one exists|
| `END`  | `end`  | Marks the end of an if-else block or a loop|
| `WHILE`  | `while`  |Peeks at the top number on the stack. If it is nonzero, execute the code until the next `end`. Then peek at the top number again and repeat until the top number is zero, then jump to the `end` |

## Examples
Code examples can be found in the `examples` directory, but here is an
example program that calculates the fibonacci numbers less than or equal to 1000
and prints them to standard output:
```
1 1 while
  dup dump
  swap dup2 +
  dup 1000 >= if 0 end
end
```
