# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "z3-solver",
# ]
# ///
example = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
""".strip()

from dataclasses import dataclass
from typing import LiteralString
import math
from random import random


@dataclass
class Machine:
    lights: int
    toggles: list[list[int]]
    joltage: list[int]

    def __init__(self, s):
        (lights, rest) = s.split("]")
        (toggles, joltage) = rest.split("{")

        toggles = [
            list(map(int, toggle[1:-1].split(",")))
            for toggle in toggles.strip().split(" ")
        ]

        self.lights = str2bits(lights[1:])
        self.toggles = toggles
        self.joltage = list(map(int, joltage[:-1].split(",")))
        # print(self)


def str2bits(s):
    bits = 0
    for i, c in enumerate(s):
        if c == "#":
            bits |= 1 << i
    return bits


def indices2bits(indices):
    bits = 0
    for i in indices:
        bits |= 1 << i
    return bits


def indices2list(indices):
    return [1 if i in indices else 0 for i in range(max(indices) + 1)]


def find_shortest(goal, options):
    options = [indices2bits(option) for option in options]
    shortest = {0: 0}
    visited = set()
    steps, current = min(((shortest[k], k) for k in shortest if k not in visited))

    while current != goal:
        visited.add(current)
        for option in options:
            if current ^ option not in shortest:
                shortest[current ^ option] = steps + 1
        steps, current = min(((shortest[k], k) for k in shortest if k not in visited))
    return steps


from typing import Dict, Self
import logging
from logging import debug, info, warning, error

from z3 import *


def find_joltage(joltage, toggles) -> int:
    debug(f"optimizing {joltage=} {toggles=}")
    solver = Optimize()
    vars = [Int(j) for j in range(len(toggles))]
    [solver.add(v >= 0) for v in vars]
    for i in range(len(joltage)):
        solver.add(
            sum([vars[j] for j, t in enumerate(toggles) if i in t]) == joltage[i]
        )
    debug(f"full system of equations: {solver}")
    solver.minimize(sum(vars))
    debug(f"{solver.check()=}")
    debug("times to press %s", [solver.model()[var] for var in vars])
    # return sum([solver.model()[var] for var in vars])

    return solver.model().eval(sum(vars)).as_long()


def part1(s: str):
    machines = [Machine(line) for line in s.split("\n")]

    min_toggles = [
        find_shortest(machine.lights, machine.toggles) for machine in machines
    ]
    # print(min_toggles)
    return sum(min_toggles)


def part2(s: str) -> int:
    machines = [Machine(line) for line in s.split("\n")]
    print("max joltage:", max([max(machine.joltage) for machine in machines]))

    min_toggles = [
        find_joltage(machine.joltage, machine.toggles) for machine in machines
    ]
    # print(min_toggles)
    return sum(min_toggles)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()

    # Set log level based on flags
    if args.verbose == 0:
        level = logging.ERROR
    elif args.verbose == 1:
        level = logging.WARNING
    elif args.verbose == 2:
        level = logging.INFO
    else:
        level = logging.DEBUG
    print(f"{level=}")

    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    with open("day10/input.txt") as f:
        input = f.read().strip()
    print("part1: ", part1(input))
    print("part2: ", part2(input))


# Tests
class TestExamples:
    def test_part1(self):
        assert part1(example) == 7

    def test_part2(self):
        assert part2(example) == 33


class TestPart1:
    def test_conversions(self):
        assert str2bits("##..#.") == 2**0 + 2**1 + 2**4
        assert indices2bits([0, 1, 4]) == 2**0 + 2**1 + 2**4
        assert indices2list([0, 1, 4]) == [1, 1, 0, 0, 1]


class TestJoltage:
    def test_single_toggles(self):
        assert find_joltage([0, 1, 2, 0], [[1], [2]]) == 3

    def test_overlapping_toggles(self):
        assert find_joltage([0, 2, 4, 2], [[1, 2], [2, 3]]) == 4

    def test_overlapping_toggles_no_uniques(self):
        assert find_joltage([0, 2, 4, 2], [[1, 2], [2, 3], [0, 1, 3]]) == 4

    def test_dead_end_possible(self):
        assert find_joltage([5, 5, 5, 5], [[0, 1, 2], [0, 1], [2, 3]]) == 10

    def test_multiple_rounds(self):
        assert (
            find_joltage([2, 5, 2, 5, 3], [[0, 1, 2], [0, 1], [2, 3], [1, 3, 4]]) == 7
        )

    def test_elimination_necessary(self):
        """
        x  +z = 2
          y+z = 3
        ----------
        2-x = 3-y
        ----------
        -x+y = 1
        """
        # TODO this can probably be solved by restricting x/y to be positive somehow
        # Still leaves open the problem that the equation system can by overspecified, leaving multiple solutions that i need to minimize
        assert find_joltage([2, 3], [[0], [1], [0, 1]]) == 3
