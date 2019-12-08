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


class Computer:
    def __init__(self, memory):
        self.memory = memory
        self.pointer = 0
        self.last_output = None

    def read_output(self):
        o = self.last_output
        self.last_output = None
        return o

    def run(self, inputs):
        input_counter = 0
        while True:
            operation = parse_operation(self.memory[self.pointer])
            if operation.opcode == 1:  # add
                operands = get_operands(operation, self.memory, self.pointer)
                dest_idx = self.memory[self.pointer+3]
                self.memory[dest_idx] = operands[0] + operands[1]
                self.pointer += 4
            elif operation.opcode == 2:  # multiply
                operands = get_operands(operation, self.memory, self.pointer)
                dest_idx = self.memory[self.pointer+3]
                self.memory[dest_idx] = operands[0] * operands[1]
                self.pointer += 4
            elif operation.opcode == 3:  # input
                dest_idx = self.memory[self.pointer+1]
                if input_counter == len(inputs):
                    # wait for next input and dont increment pointer
                    return "WaitForInput"
                else:
                    self.memory[dest_idx] = inputs[input_counter]
                    input_counter += 1
                self.pointer += 2
            elif operation.opcode == 4:  # output
                operand = get_operand(operation, self.memory, self.pointer)
                self.last_output = operand
                self.pointer += 2
            elif operation.opcode == 5:  # jump-if-true
                operands = get_operands(operation, self.memory, self.pointer)
                self.pointer = operands[1] if operands[0] != 0 else self.pointer+3
            elif operation.opcode == 6:  # jump-if-false
                operands = get_operands(operation, self.memory, self.pointer)
                self.pointer = operands[1] if operands[0] == 0 else self.pointer+3
            elif operation.opcode == 7:  # less than
                operands = get_operands(operation, self.memory, self.pointer)
                dest_idx = self.memory[self.pointer+3]
                self.memory[dest_idx] = 1 if operands[0] < operands[1] else 0
                self.pointer += 4
            elif operation.opcode == 8:  # equals
                operands = get_operands(operation, self.memory, self.pointer)
                dest_idx = self.memory[self.pointer+3]
                self.memory[dest_idx] = 1 if operands[0] == operands[1] else 0
                self.pointer += 4
            elif operation.opcode == 99:  # halt
                return "Halt"
            else:
                print("ERROR!" + str(operation.opcode))
                return None


def run_amplifiers(program, phases: [int]):
    amplifiers = []
    i = 0
    while i < len(phases):
        memory = program[:]
        amplifiers.append(Computer(memory))
        i += 1

    # set phases for each amp
    i = 0
    while i < len(phases):
        amp = amplifiers[i]
        amp.run([phases[i]])
        i += 1

    # calculate thrust
    thrust = 0
    done = False
    while not done:
        i = 0
        while i < len(phases):
            amp = amplifiers[i]
            inputs = [thrust]
            amp.run(inputs)
            output = amp.read_output()
            if output == None:
                done = True
                break
            thrust = output
            i += 1
    return thrust


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


text = open('input.txt')
amplifier_program = [int(n) for n in text.read().split(",")]
# run_amplifiers(amplifier_program, [9,8,7,6,5])


def find_largest_thrust():
    allcombinations = []
    combinations([5, 6, 7, 8, 9], [], allcombinations)
    largest = 0
    best_combination = []
    for combination in allcombinations:
        thrust = run_amplifiers(amplifier_program, combination)
        if thrust > largest:
            largest = thrust
            best_combination = combination
    print(largest)
    print(best_combination)


find_largest_thrust()
