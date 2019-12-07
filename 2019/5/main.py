from functools import lru_cache

text = open('input.txt')

input_memory = [int(n) for n in text.read().split(",")]


class Operation:
    def __init__(self, opcode: int, mode1: int, mode2: int, mode3):
        self.opcode = opcode
        self.mode1 = mode1
        self.mode2 = mode2
        self.mode3 = mode3

    def __str__(self):
        return"opcode: " + str(self.opcode)


@lru_cache
def parse_operation(op):
    op_str = str(op).zfill(5)
    return Operation(int(op_str[3:5]), int(op_str[2]), int(op_str[1]), int(op_str[0]))


def get_operands(operation: Operation, memory, pointer):
    op1 = memory[pointer+1]
    if operation.mode1 == 0:
        op1 = memory[op1]
    op2 = memory[pointer+2]
    if operation.mode2 == 0:
        op2 = memory[op2]
    return (op1, op2)


def get_operand(operation: Operation, memory, pointer):
    op1 = memory[pointer+1]
    if operation.mode1 == 0:
        return memory[op1]
    return op1


def computer(memory, input):
    pointer = 0
    while True:
        operation = parse_operation(memory[pointer])
        if operation.opcode == 1:  # add
            operands = get_operands(operation, memory, pointer)
            dest_idx = memory[pointer+3]
            memory[dest_idx] = operands[0] + operands[1]
            pointer += 4
        elif operation.opcode == 2:  # multiply
            operands = get_operands(operation, memory, pointer)
            dest_idx = memory[pointer+3]
            memory[dest_idx] = operands[0] * operands[1]
            pointer += 4
        elif operation.opcode == 3:  # input
            dest_idx = memory[pointer+1]
            memory[dest_idx] = input
            pointer += 2
        elif operation.opcode == 4:  # output
            operand = get_operand(operation, memory, pointer)
            print(operand)
            pointer += 2
        elif operation.opcode == 5:  # jump-if-true
            operands = get_operands(operation, memory, pointer)
            pointer = operands[1] if operands[0] != 0 else pointer+3
        elif operation.opcode == 6:  # jump-if-false
            operands = get_operands(operation, memory, pointer)
            pointer = operands[1] if operands[0] == 0 else pointer+3
        elif operation.opcode == 7:  # less than
            operands = get_operands(operation, memory, pointer)
            dest_idx = memory[pointer+3]
            memory[dest_idx] = 1 if operands[0] < operands[1] else 0
            pointer += 4
        elif operation.opcode == 8:  # equals
            operands = get_operands(operation, memory, pointer)
            dest_idx = memory[pointer+3]
            memory[dest_idx] = 1 if operands[0] == operands[1] else 0
            pointer += 4
        elif operation.opcode == 99:  # halt
            return
        else:
            print("ERROR!" + str(operation.opcode))
            return


def run_program_with_input(initial_memory, input):
    memory = initial_memory[:]
    computer(memory, input)


run_program_with_input(input_memory, 5)
