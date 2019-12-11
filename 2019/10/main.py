#   # . # .
#   . % . .
#   # . . #

import math
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def get_vector(self, other):
        delta_x = other.x - self.x
        delta_y = other.y - self.y
        return Vector(delta_x, delta_y)

    def get_asteroid(self, other):
        v = self.get_vector(other)
        return Asteroid(other, v.degrees(), v.length())


@dataclass
class Vector:
    x: float
    y: float

    def __hash__(self):
        return hash(self.x + self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def length(self):
        return math.hypot(self.x, self.y)

    def degrees(self):
        return round(((math.degrees(math.atan2(self.y, self.x)) + 90) % 360), 5)

    def unit_vector(self):
        length = self.length()
        if length > 0:
            return Vector(round(self.x/length, 4), round(self.y/length, 4))
        return (0, 0)


@dataclass
class Asteroid:
    point: Point
    angle: float
    distance: float


@dataclass
class AsteroidsWithAngle:
    angle: float
    asteroids: [Asteroid]

    def ordered_by_length(self):
        self.asteroids.sort(key=lambda a: a.distance)
        return self.asteroids

    def remove_first(self):
        a = self.asteroids[0]
        self.asteroids = self.asteroids[1:]
        return a


def count_visible(p, points):
    filtered = filter(lambda p1: p1 != p, points)
    vectors = [p.get_vector(o) for o in filtered]
    unique = set([o.degrees() for o in vectors])
    return len(unique)


def find_best():
    points = []
    y = 0
    while y < len(lines):
        x = 0
        line = lines[y]
        while x < len(line):
            if line[x] == "#":
                points.append(Point(x, y))
            x += 1
        y += 1

    largest = 0
    best = None
    for p in points:
        v = count_visible(p, points)
        if v > largest:
            largest = v
            best = p

    print(best)
    print(largest)
    return best


def build_points(lines):
    points = []
    y = 0
    while y < len(lines):
        x = 0
        line = lines[y]
        while x < len(line):
            if line[x] == "#":
                points.append(Point(x, y))
            x += 1
        y += 1
    return points


def build_asteroids(p: Point, points):
    asteroids = []
    by_angle = {}
    filtered = list(filter(lambda o: o != p, points))
    for other in filtered:
        asteroid = p.get_asteroid(other)
        # print(asteroid)
        if asteroid.distance != 0:
            asteroids.append(asteroid)

            if by_angle.get(asteroid.angle) == None:
                by_angle[asteroid.angle] = AsteroidsWithAngle(
                    asteroid.angle, [asteroid])
            else:
                by_angle[asteroid.angle].asteroids.append(asteroid)

    return (asteroids, by_angle)


text = open('input.txt')
lines = [l.rstrip("\n") for l in text.readlines()]


best = find_best()

points = build_points(lines)

res = build_asteroids(best, points)
unique_angles = list(set([v.angle for v in res[0]]))
unique_angles.sort()

by_angle = res[1]

removed = 0

while True:
    any_removed = False
    for a in unique_angles:
        asteroids = by_angle[a]
        if len(asteroids.ordered_by_length()) > 0:
            ast = asteroids.remove_first()
            any_removed = True
            removed += 1
            if removed == 200:
                print(str(removed) + ": " + str(ast))
                print(ast.point.x * 100 + ast.point.y)
    if not any_removed:
        break
    any_removed = False
