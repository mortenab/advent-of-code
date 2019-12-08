from dataclasses import dataclass
import sys


def color(i):
    if i == 1:
        return "#"
    else:
        return " "


@dataclass
class Layer:
    rows: [[int]]

    def count_occs(self, value):
        count = 0
        for r in self.rows:
            for c in r:
                if value == c:
                    count += 1
        return count

    def print_me(self):
        for r in self.rows:
            for c in r:
                sys.stdout.write(str(color(c)))
            print()

    def merge(self, below):
        i = 0
        while i < len(self.rows):
            j = 0
            my_row = self.rows[i]
            below_row = below.rows[i]
            while j < len(my_row):
                if my_row[j] == 2:
                    my_row[j] = below_row[j]
                j += 1
            i += 1


def split(input: str, chunk_size: int):
    i = 0
    chunks = []
    while i < len(input):
        chunk = input[i:i+chunk_size]
        i += chunk_size
        chunks.append(chunk)
    return chunks


def find_layers(input: str, width: int, height: int):
    layers_strs = split(input, width*height)
    layers = []
    for i in layers_strs:
        layer = []
        rows_strs = split(i, width)
        for r in rows_strs:
            row_cells = split(r, 1)
            layer.append([int(n) for n in row_cells])
        layers.append(Layer(layer))
    return layers


text = open('input.txt')
input = text.read().rstrip("\n")
#input = "123456789012"
layers = find_layers(input, 25, 6)
# print(layers)


def check_image():
    fewest_zeros = 100000000
    fewest_zeros_layer = None
    for l in layers:
        zeros = l.count_occs(0)
        if zeros < fewest_zeros:
            fewest_zeros = zeros
            fewest_zeros_layer = l
    fewest_zeros_layer.print_me()
#print(fewest_zeros_layer.count_occs(1) * fewest_zeros_layer.count_occs(2))
# print(fewest_zeros_layer)


# check_image()


def merge_layers():
    i = 1
    layer = layers[0]
    while i < len(layers):
        layer.merge(layers[i])
        i += 1
    layer.print_me()


merge_layers()
