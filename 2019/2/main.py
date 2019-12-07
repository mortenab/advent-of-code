text = open('input.txt')

input_memory = [int(n) for n in text.read().split(",")]


def computer(memory):
    pointer = 0
    while True:
        if memory[pointer] == 99:
            break
        elif memory[pointer] == 1:
            op1Idx = memory[pointer+1]
            op2Idx = memory[pointer+2]
            destIdx = memory[pointer+3]
            memory[destIdx] = memory[op1Idx] + memory[op2Idx]
            pointer += 4
        elif memory[pointer] == 2:
            op1Idx = memory[pointer+1]
            op2Idx = memory[pointer+2]
            destIdx = memory[pointer+3]
            memory[destIdx] = memory[op1Idx] * memory[op2Idx]
            pointer += 4


def run_program(initial_memory, noun, verb):
    memory = initial_memory[:]
    memory[1] = noun
    memory[2] = verb
    computer(memory)
    return memory[0]


print('1202: ' + str(run_program(input_memory, 12, 2)))


def find_pair(initial_memory):
    for noun in range(0, 100):
        for verb in range(0, 100):
            result = run_program(initial_memory, noun, verb)

            if result == 19690720:
                print('noun: ' + str(noun) + ' verb: ' + str(verb))
                print(100 * noun + verb)


find_pair(input_memory)
