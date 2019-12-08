from functools import lru_cache

import sys
sys.setrecursionlimit(10000)


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


def computer(memory, inputs):
    input_counter = 0
    pointer = 0
    output = []
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
            memory[dest_idx] = inputs[input_counter]
            input_counter += 1
            pointer += 2
        elif operation.opcode == 4:  # output
            operand = get_operand(operation, memory, pointer)
            output.append(operand)
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
            return output
        else:
            print("ERROR!" + str(operation.opcode))
            return None


def run_amplifiers(program, phases: [int]):
    thrust = 0
    for phase in phases:
        memory = program[:]
        output = computer(memory, [phase, thrust])
        thrust = output[0]
    return thrust


# Doh! this is all permuutations
def permutations(range_from, range_to, arr, length, output):
    cur = range_from
    while cur <= range_to:
        new_arr = arr[:]
        new_arr.append(cur)
        cur += 1
        if len(new_arr) == length:
            output.append(new_arr)
        else:
            permutations(range_from, range_to, new_arr, length, output)


def combinations(input, acc, output):
    i = 0
    while i < len(input):
        acc_sub = acc[:]
        acc_sub.append(input[i])
        input_sub = input[:]
        del input_sub[i]
        i += 1
        if len(input) == 1:
            output.append(acc_sub)
        else:
            combinations(input_sub, acc_sub, output)


text = open('test1.txt')
amplifier_program = [int(n) for n in text.read().split(",")]
#run_amplifiers(amplifier_program, [4, 3, 2, 1, 0])


def find_largest_thrust():
    allcombinations = []
    combinations([0, 1, 2, 3, 4], [], allcombinations)
    largest = 0
    best = []
    for combination in allcombinations:
        thrust = run_amplifiers(amplifier_program, combination)
        if thrust > largest:
            largest = thrust
            best = combination
    print(largest)
    print(best)


find_largest_thrust()
