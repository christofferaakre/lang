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
OP_PRINT = iota()
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

OP_COUNT = iota()
