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
    points = [list(map(int, line.split(","))) for line in s.split("\n")]
    starting_points = [[94997, 50126], [94997, 48641]]
    best = [0, 0]
    best_p = [[], []]
    for i in range(len(points)):
        above = points[i][1] - starting_points[1][1]
        if 0 > above > -14300:
            size = (abs(points[i][0] - starting_points[1][0]) + 1) * (
                abs(points[i][1] - starting_points[1][1]) + 1
            )
            if size > best[1]:
                best[1] = size
                best_p[1] = [points[i], starting_points[1]]
    for i in range(len(points)):
        below = points[i][1] - starting_points[0][1]
        if 0 < below < 17000:
            size = (abs(points[i][0] - starting_points[0][0]) + 1) * (
                abs(points[i][1] - starting_points[0][1]) + 1
            )
            if size > best[0]:
                best[0] = size
                best_p[0] = [points[i], starting_points[0]]

    print(best)
    print(best_p)
    return max(best)


if __name__ == "__main__":
    assert part1(example) == 50
    # assert part2(example) == 24

    with open("day9/input.txt") as f:
        input = f.read().strip()
    print("part1: ", part1(input))
    print("part2: ", part2(input))
