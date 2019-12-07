

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self):
        return abs(self.x) + abs(self.y)


def between(i, i_start, i_end):
    return (i >= i_start and i <= i_end) or (i >= i_end and i <= i_start)


class Segment:
    def __init__(self, x_start, x_end, y_start, y_end, steps):
        self.x_start = x_start
        self.x_end = x_end
        self.y_start = y_start
        self.y_end = y_end
        self.steps = steps

    def horiz(self):
        return self.y_start == self.y_end

    def intersect(self, other):
        if self.horiz() == other.horiz():
            return None
        if self.horiz():
            if between(self.y_start, other.y_start, other.y_end) and between(other.x_start, self.x_start, self.x_end):
                delta_y = abs(self.y_start - other.y_start)
                delta_x = abs(self.x_start - other.x_start)
                total_steps = delta_x + delta_y + self.steps + other.steps
                return (self.y_start, other.x_start, total_steps)
            return None
        else:
            if between(self.x_start, other.x_start, other.x_end) and between(other.y_start, self.y_start, self.y_end):
                delta_y = abs(self.y_start - other.y_start)
                delta_x = abs(self.x_start - other.x_start)
                total_steps = delta_x + delta_y + self.steps + other.steps
                return (self.x_start, other.y_start, total_steps)
            return None

    def __str__(self):
        return "(" + str(self.x_start) + ", " + str(self.y_start) + ") (" + str(self.x_end) + " -> " + str(self.y_end) + ")"


class Wire:
    def __init__(self, segments):
        self.segments = segments

    def __str__(self):
        return ";".join([str(x) for x in self.segments])


lines = [line.rstrip('\n') for line in open('input.txt')]
wire1 = [n for n in lines[0].split(",")]
wire2 = [n for n in lines[1].split(",")]


def segments(wire):
    p = Point(0, 0)
    segments = []
    steps = 0
    for move in wire:
        move_steps = int(move[1:])
        if move.startswith("R"):
            new_x = p.x + move_steps
            segments.append(Segment(p.x, new_x, p.y, p.y, steps))
            p.x = new_x
        elif move.startswith("L"):
            new_x = p.x - move_steps
            segments.append(Segment(p.x, new_x, p.y, p.y, steps))
            p.x = new_x
        elif move.startswith("U"):
            new_y = p.y + move_steps
            segments.append(Segment(p.x, p.x, p.y, new_y, steps))
            p.y = new_y
        elif move.startswith("D"):
            new_y = p.y - move_steps
            segments.append(Segment(p.x, p.x, p.y, new_y, steps))
            p.y = new_y
        steps += move_steps
    return Wire(segments)


w1_segments = segments(wire1)
w2_segments = segments(wire2)


intersects = []
for s1 in w1_segments.segments[1:]:
    for s2 in w2_segments.segments[1:]:
        d = s1.intersect(s2)
        if d != None:
            intersects.append(abs(d[0]) + abs(d[1]))

print(min(intersects))

combined_steps = []
for s1 in w1_segments.segments[1:]:
    for s2 in w2_segments.segments[1:]:
        d = s1.intersect(s2)
        if d != None:
            combined_steps.append(abs(d[2]))

print(min(combined_steps))
