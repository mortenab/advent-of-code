class Operation:
    def __init__(self, opcode: int, mode1: int, mode2: int, mode3):
        self.opcode = opcode
        self.mode1 = mode1
        self.mode2 = mode2
        self.mode3 = mode3

    def __str__(self):
        return"opcode: " + str(self.opcode)


class Computer:
    def __init__(self, memory, output):
        self.memory = memory
        self.pointer = 0
        self.relative_base_offset = 0
        self.output = output

    def parse_operation(self):
        op = self.memory[self.pointer]
        op_str = str(op).zfill(5)
        return Operation(int(op_str[3:5]), int(op_str[2]), int(op_str[1]), int(op_str[0]))

    def get_operands(self, operation: Operation):
        return (self.get_value(operation.mode1, self.pointer + 1), self.get_value(operation.mode2, self.pointer + 2))

    def get_operand(self, operation: Operation):
        return self.get_value(operation.mode1, self.pointer + 1)

    def get_destination_ptr(self, mode: int, offset: int):
        if mode == 0:  # position
            return self.memory[offset]
        else:  # relative offset
            return self.relative_base_offset+self.memory[offset]

    def get_value(self, mode: int, offset: int):
        val = self.memory[offset]
        if mode == 0:  # position
            return self.memory[val]
        elif mode == 1:  # by value
            return val
        else:  # relative offset
            return self.memory[self.relative_base_offset+val]

    def run(self, inputs):
        input_counter = 0
        while True:
            operation = self.parse_operation()
            if operation.opcode == 1:  # add
                operands = self.get_operands(operation)
                dest_idx = self.get_destination_ptr(
                    operation.mode3, self.pointer+3)
                self.memory[dest_idx] = operands[0] + operands[1]
                self.pointer += 4
            elif operation.opcode == 2:  # multiply
                operands = self.get_operands(operation)
                dest_idx = self.get_destination_ptr(
                    operation.mode3, self.pointer+3)
                self.memory[dest_idx] = operands[0] * operands[1]
                self.pointer += 4
            elif operation.opcode == 3:  # input
                if input_counter == len(inputs):
                    # wait for next input and dont increment pointer
                    return "WaitForInput"
                else:
                    dest_idx = self.get_destination_ptr(
                        operation.mode1, self.pointer+1)
                    self.memory[dest_idx] = inputs[input_counter]
                    input_counter += 1
                self.pointer += 2
            elif operation.opcode == 4:  # output
                operand = self.get_operand(operation)
                self.output(operand)
                self.pointer += 2
            elif operation.opcode == 5:  # jump-if-true
                operands = self.get_operands(operation)
                self.pointer = operands[1] if operands[0] != 0 else self.pointer+3
            elif operation.opcode == 6:  # jump-if-false
                operands = self.get_operands(operation)
                self.pointer = operands[1] if operands[0] == 0 else self.pointer+3
            elif operation.opcode == 7:  # less than
                operands = self.get_operands(operation)
                dest_idx = self.get_destination_ptr(
                    operation.mode3, self.pointer+3)
                self.memory[dest_idx] = 1 if operands[0] < operands[1] else 0
                self.pointer += 4
            elif operation.opcode == 8:  # equals
                operands = self.get_operands(operation)
                dest_idx = self.get_destination_ptr(
                    operation.mode3, self.pointer+3)
                self.memory[dest_idx] = 1 if operands[0] == operands[1] else 0
                self.pointer += 4
            elif operation.opcode == 9:  # set base
                operand = self.get_operand(operation)
                self.relative_base_offset += operand
                self.pointer += 2
            elif operation.opcode == 99:  # halt
                print("computer: Done")
                return "Halt"
            else:
                print("ERROR!" + str(operation.opcode))
                return None


text = open('input.txt')
BOOST = [int(n) for n in text.read().split(",")]


# 32K memory
memory = [0] * (32*1024)

# copy program to memory
i = 0
while i < len(BOOST):
    memory[i] = BOOST[i]
    i += 1

# create computer
c = Computer(memory, lambda o: print("output: " + str(o)))

m = c.run([2])
