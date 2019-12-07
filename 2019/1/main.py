
inputs = [int(line.rstrip('\n')) for line in open('input.txt')]


def fuelWeight(w):
    return int(w/3)-2


def run():
    total = 0
    for w in inputs:
        total += fuelWeight(w)
    print(total)


run()


def moduleWeight(moduleWeight):
    total = 0
    current = moduleWeight
    while True:
        current = fuelWeight(current)
        if current <= 0:
            break
        total += current
    return total


def fuelRec():
    total = 0
    for w in inputs:
        total += moduleWeight(w)
    print(total)


fuelRec()
