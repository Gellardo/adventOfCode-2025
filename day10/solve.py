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


@dataclass
class Equation:
    """
    Represents a single equation, f_1 * x_1 + f_2 * x_2 + ... = j.
    """

    factors: Dict[int, int]
    joltage: int

    def solve(self, values):
        to_solve = set(self.factors).difference(values.keys())
        if len(to_solve) > 1:
            raise Exception("Can't solve, because there are at least 2 unknown values")
        sum_left = 0
        for x_i in values:
            factor = self.factors[x_i] if self.has_factor(x_i) else 0
            sum_left += values[x_i] * factor
        remainder = self.joltage - sum_left
        if len(to_solve) == 0 and remainder != 0:
            raise Exception(
                f"values do not produce valid equation {self.joltage=} != {sum_left}"
            )
        elif len(to_solve) == 1:
            return {to_solve.pop(): remainder}
        else:
            return {}

    def has_factor(self, i):
        return i in self.factors

    def factor(self, i):
        return self.factors[i] if i in self.factors else 0

    def check_valid(self, values):
        return len(self.solve(values)) == 0

    def eliminate(self, other: Self, i):
        if not other.has_factor(i):
            raise Exception(
                "can't eliminate factor_i if other Equation does not have a corresponding factor"
            )
        if not self.has_factor(i):
            return
        mult = int(self.factors[i] / other.factors[i])
        factors = set(self.factors).union(set(other.factors))
        for factor in factors:
            self_f = self.factor(factor)
            other_f = other.factor(factor)
            new_f = self_f - mult * other_f

            self.factors[factor] = new_f
        self.joltage = self.joltage - mult * other.joltage

        to_delete = [factor for factor in self.factors if self.factors[factor] == 0]
        for factor in to_delete:
            del self.factors[factor]


def test_Equation_eliminate():
    eq = Equation({0: 1, 2: 1}, 5)
    eq.eliminate(Equation({0: 1}, 3), 0)
    assert eq.joltage == 2
    assert eq.factors[2] == 1

    eq = Equation({0: 1, 2: 1}, 5)
    eq.eliminate(Equation({0: 1, 1: 1}, 3), 0)
    assert eq.factors == {1: -1, 2: 1}
    assert eq.joltage == 2

    """
    - x     + z = 5
      x + y     = 3 (*-1)
    ----------
          y + z = 8
    """
    eq = Equation({0: -1, 2: 1}, 5)
    eq.eliminate(Equation({0: 1, 1: 1}, 3), 0)
    assert eq.factors == {1: 1, 2: 1}
    assert eq.joltage == 8


def test_Equation_solve():
    assert Equation({0: 1, 2: 1}, 5).solve({2: 5}) == {0: 0}
    assert Equation({0: 1, 2: 1}, 5).solve({1: 2, 2: 3}) == {0: 2}

    import pytest

    with pytest.raises(Exception):
        Equation({0: 1, 2: 1}, 5).solve({0: 10, 2: 0})
        Equation({0: 1, 2: 1}, 5).solve({1: 0})


def test_Equation_valid():
    assert Equation({0: 1, 2: 1}, 5).check_valid({0: 2, 1: 10, 2: 3})
    assert Equation({0: 1, 2: 1}, 5).check_valid({0: 10}) == False


def find_joltage(joltage, toggles):
    equations = []
    info(f"starting point: {joltage=}, {toggles=}")
    for i in range(len(joltage)):
        eq = Equation({j: 1 for j, t in enumerate(toggles) if i in t}, joltage[i])
        if eq not in equations:
            equations.append(eq)
    debug(equations)

    values = {}
    solved = []
    while len(equations) > len(solved):
        new_solved = False
        for eq in equations:
            if eq in solved:
                continue
            try:
                new_values = eq.solve(values)
                values.update(new_values)
                if eq.check_valid(values):
                    debug(f"solved {eq=} with {values=}")
                    solved.append(eq)
                    new_solved = True
            except:
                pass
        if new_solved:
            continue

        unsolved_i = [i for i in range(len(joltage)) if i not in values][0]
        debug(f"eliminate {unsolved_i=}")
        related_eqs = [eq for eq in equations if eq.has_factor(unsolved_i)]
        if len(related_eqs) > 1:
            for eq in related_eqs[1:]:
                eq.eliminate(related_eqs[0], unsolved_i)

        # select random unsolved index
        # eliminate it from all others

    debug(f"final values: {values}")
    return sum(values.values())


def part1(s: str):
    machines = [Machine(line) for line in s.split("\n")]

    min_toggles = [
        find_shortest(machine.lights, machine.toggles) for machine in machines
    ]
    # print(min_toggles)
    return sum(min_toggles)


def part2(s: str):
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
