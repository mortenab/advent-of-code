from dataclasses import dataclass
from typing import List


@dataclass
class Planet:
    name: str
    orbits: str
    orbited_by: List[str]
    jumps: int


def parse_orbit(orbit: str):
    ps = orbit.split(")")
    return(ps[0], ps[1])


inputs = [parse_orbit(line.rstrip('\n')) for line in open('input.txt')]


def build_planets():
    planets = {}
    for orbit in inputs:
        orbitee = orbit[0]
        orbiter = orbit[1]
        p_orbitee = planets.get(orbitee)
        if p_orbitee == None:
            # create orbitee if not exists (does not orbit anyone yet)
            planets[orbitee] = Planet(orbitee, None, [], 0)

        p_orbiter = planets.get(orbiter)
        if p_orbiter == None:
            # create if not exists
            planets[orbiter] = Planet(orbiter, orbitee, [], 0)
        else:
            # else create relation
            planets[orbiter].orbits = orbitee

        # add orbitee -> orbiter relation
        planets[orbitee].orbited_by.append(orbiter)

    return planets


def count_orbits(planets: List[Planet], root: str, acc: int):
    current = planets[root]
    orbited_by = 0
    for name in current.orbited_by:
        orbited_by += count_orbits(planets, name, acc+1)
    return acc + orbited_by


def assign_jumps(planets: List[Planet], root: str, acc: int):
    current = planets[root]
    current.jumps = acc
    for name in current.orbited_by:
        assign_jumps(planets, name, acc+1)


def find_common_ancestor(planets: List[Planet], p1: str, p2: str):
    planet1 = planets[p1]
    planet2 = planets[p2]
    jumps = 0
    while True:
        if planet1.jumps > planet2.jumps:
            planet1 = planets[planet1.orbits]
            jumps += 1
        elif planet1.jumps < planet2.jumps:
            planet2 = planets[planet2.orbits]
            jumps += 1
        else:
            if planet1.name == planet2.name:
                return (planet1.name, jumps)
            else:
                planet1 = planets[planet1.orbits]
                planet2 = planets[planet2.orbits]
                jumps += 2


planets = build_planets()
assign_jumps(planets, "COM", 0)


# print(planets)

p_you = planets["YOU"].orbits
p_san = planets["SAN"].orbits

anc = find_common_ancestor(planets, p_you, p_san)
print("ancestor: " + anc[0] + " " + str(anc[1]))


# print(count_orbits(planets, "COM", 0))
