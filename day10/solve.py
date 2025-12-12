example = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
""".strip()

from dataclasses import dataclass
from typing import LiteralString
import math


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


assert str2bits("##..#.") == 2**0 + 2**1 + 2**4


def indices2bits(indices):
    bits = 0
    for i in indices:
        bits |= 1 << i
    return bits


assert indices2bits([0, 1, 4]) == 2**0 + 2**1 + 2**4


def indices2list(indices):
    return [1 if i in indices else 0 for i in range(max(indices) + 1)]


assert indices2list([0, 1, 4]) == [1, 1, 0, 0, 1]


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


def list2base(l, base):
    number = 0
    for bit in reversed(l):
        number = base * number + bit
    return number


assert list2base([1, 0, 1, 1], base=2) == 2**0 + 2**2 + 2**3
assert list2base([1, 0, 2, 1], base=3) == 3**0 + 2 * 3**2 + 3**3


def base2list(number, base):
    l = []
    while number > 0:
        l.append(number % base)
        number = number // base
    return l


assert base2list(list2base([1, 2, 1, 1, 3], base=4), base=4) == [1, 2, 1, 1, 3]


def joltage2hash(joltage):
    """My max joltage is 271, so base300 works, it's just unreadable"""
    return list2base(joltage, base=300)


def hash2joltage(hash):
    return base2list(hash, base=300)


def estimate_distance(current, goal):
    estimate = 0
    while goal > 0:
        dist = goal % 300 - current % 300
        if dist < 0:
            return -1
        estimate += dist

        current //= 300
        goal //= 300
    return estimate


assert estimate_distance(joltage2hash([1, 2, 3]), joltage2hash([2, 4, 6])) == 1 + 2 + 3
assert estimate_distance(joltage2hash([1, 2, 3]), joltage2hash([0, 2, 3])) == -1


assert hash2joltage(joltage2hash([2, 4, 6, 1])) == [2, 4, 6, 1]


def find_joltage(goal, options):
    # print(f"{goal=} -> {joltage2hash(goal)}")
    goal = joltage2hash(goal)
    # print(options)
    options = [joltage2hash(indices2list(option)) for option in options]
    # print(options)

    estimates = {0: estimate_distance(0, goal)}
    definitive = {goal: 0}

    iterations = 0
    while 0 not in definitive:
        iterations += 1
        _, current = min(((estimates[k], k) for k in estimates if k not in definitive))
        # print(f"  {current=} {estimates=} {len(definitive)=}")
        change = False
        for option in options:
            # print("    checking", option, hash2joltage(option))
            next = current + option
            if next in definitive:
                if definitive[next] < estimates[current]:
                    definitive[current] = definitive[next] + 1
                    del estimates[current]
                    # print(f"found shortest for {current}")
                    break
            elif next not in estimates and next not in definitive:
                if estimate_distance(next, goal) > 0:
                    estimates[next] = estimate_distance(next, goal)
                    change = True

            if next in estimates and estimates[next] + 1 < estimates[current]:
                estimates[current] = estimates[next] + 1
                change = True
            if next in estimates and estimates[next] > estimates[current] + 1:
                estimates[next] = estimates[current] + 1
                change = True
        if current in estimates and not change:
            definitive[current] = estimates[0] + 1
            del estimates[current]
        if iterations % 500 == 0:
            print(
                f"    {estimates[0]=}, {iterations=}, {len(estimates)=}, {len(definitive)=}"
            )
    print(f">>> {definitive[0]=}, {iterations=}, {len(estimates)=}, {len(definitive)=}")
    return definitive[0]


assert find_joltage([0, 1, 2, 0], [[1], [2]]) == 3
assert find_joltage([0, 1, 2, 1], [[1, 2], [2, 3]]) == 2
assert find_joltage([5, 5, 5, 5], [[0, 1, 2], [0, 1], [2, 3]]) == 10


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


assert part1(example) == 7
assert part2(example) == 33


if __name__ == "__main__":
    with open("day10/input.txt") as f:
        input = f.read().strip()
    print("part1: ", part1(input))
    print("part2: ", part2(input))
