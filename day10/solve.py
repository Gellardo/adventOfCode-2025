example = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
""".strip()

from dataclasses import dataclass
from typing import LiteralString


@dataclass
class Machine:
    lights: int
    toggles: list[int]
    joltage: list[int]

    def __init__(self, s):
        (lights, rest) = s.split("]")
        (toggles, joltage) = rest.split("{")

        toggles = [
            indices2bits(list(map(int, toggle[1:-1].split(","))))
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


def find_shortest(goal, options):
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


def joltage2hash(joltage):
    """My max joltage is 271, so base300 works, it's just unreadable"""
    return list2base(joltage, base=300)


def hash2joltage(hash):
    return base2list(hash, base=300)


def list2base(l, base):
    number = 0
    for bit in reversed(l):
        number = 300 * number + bit
    return number


def base2list(number, base):
    l = []
    while number > 0:
        l.append(number % base)
        number = number // base
    return l


def acceptable_joltage(current, goal):
    # print("acceptable?", hash2joltage(current), hash2joltage(goal), end=" ")
    while current > 0:
        if current % 300 > goal % 300:
            # print("false")
            return False
        current //= 300
        goal //= 300
    # print("true")
    return True


# print(joltage2hash([2, 4, 6, 1]))
# print(hash2joltage(joltage2hash([2, 4, 6, 1])))
assert hash2joltage(joltage2hash([2, 4, 6, 1])) == [2, 4, 6, 1]


def find_joltage(goal, options):
    print(f"{goal=} -> {joltage2hash(goal)}")
    goal = joltage2hash(goal)
    print(f"{joltage2hash([1,0,0,0,0])=}")
    print(
        f"{indices2bits([0])=} -> {joltage2hash(base2list(indices2bits([0]), base=2))}"
    )
    options = [joltage2hash(base2list(option, base=2)) for option in options]

    shortest = {0: 0}
    visited = set()
    steps, current = min(((shortest[k], k) for k in shortest if k not in visited))

    while current != goal:
        visited.add(current)
        print("  current:", current, shortest)
        for option in options:
            print("    checking", option, hash2joltage(option))
            next = current + option
            if next not in shortest and acceptable_joltage(next, goal):
                print("accepted", hash2joltage(next), hash2joltage(goal))
                shortest[next] = steps + 1

        steps, current = min(((shortest[k], k) for k in shortest if k not in visited))
    print(f">>> {steps=}")
    return steps


find_joltage(
    [1, 0, 0, 1, 0],
    [indices2bits([0]), indices2bits([3])],
)
find_joltage(
    [1, 2, 3, 4, 5],
    [indices2bits([0, 1, 2, 3, 4]), indices2bits([0, 1, 2]), indices2bits([3, 4])],
)
assert find_joltage([0, 1, 2, 0], [indices2bits([1]), indices2bits([2])]) == 3
assert find_joltage([0, 1, 2, 0], [indices2bits([1, 2]), indices2bits([2])]) == 2


def part1(s: str):
    machines = [Machine(line) for line in s.split("\n")]

    min_toggles = [
        find_shortest(machine.lights, machine.toggles) for machine in machines
    ]
    print(min_toggles)
    return sum(min_toggles)


def part2(s: str):
    machines = [Machine(line) for line in s.split("\n")]
    print("max joltage:", max([max(machine.joltage) for machine in machines]))

    min_toggles = [
        find_joltage(machine.joltage, machine.toggles) for machine in machines
    ]
    print(min_toggles)
    return sum(min_toggles)


assert part1(example) == 7
assert part2(example) == 33


if __name__ == "__main__":
    with open("day10/input.txt") as f:
        input = f.read().strip()
    print("part1: ", part1(input))
    print("part2: ", part2(input))
