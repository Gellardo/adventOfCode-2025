example = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
""".strip()

import math


def part1(s: str):
    points = [list(map(int, line.split(","))) for line in s.split("\n")]
    # print(points)
    max_size = 0
    for i in range(len(points)):
        for j in range(len(points)):
            size = (abs(points[i][0] - points[j][0]) + 1) * (
                abs(points[i][1] - points[j][1]) + 1
            )
            if size > max_size:
                max_size = size

    return max_size


def part2(s: str):
    lines = s.split("\n")
    return 0


assert part1(example) == 50
assert part2(example) == 0


if __name__ == "__main__":
    with open("day9/input.txt") as f:
        input = f.read().strip()
    print("part1: ", part1(input))
    print("part2: ", part2(input))
