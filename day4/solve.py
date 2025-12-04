example = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
""".strip()


def parseGrid(s):
    return [[c for c in line] for line in s.split("\n")]


# the sins i commit, just to not have to edit part1 when switching to ints instead of chars
def get(grid, i, j, default="."):
    def debug():
        if i < 0 or j < 0:
            return default
        try:
            return grid[i][j]
        except:
            return default

    r = debug()
    # print(r, i, j)
    return r


def part1(s: str):
    grid = parseGrid(s)
    accessible = 0
    for i, v in enumerate(grid):
        for j, c in enumerate(v):
            neighbours = 0
            if get(grid, i - 1, j - 1) == "@":
                neighbours += 1
            if get(grid, i - 1, j) == "@":
                neighbours += 1
            if get(grid, i - 1, j + 1) == "@":
                neighbours += 1
            if get(grid, i, j - 1) == "@":
                neighbours += 1
            if get(grid, i, j + 1) == "@":
                neighbours += 1
            if get(grid, i + 1, j - 1) == "@":
                neighbours += 1
            if get(grid, i + 1, j) == "@":
                neighbours += 1
            if get(grid, i + 1, j + 1) == "@":
                neighbours += 1
            if c == "@" and neighbours < 4:
                print(neighbours, end="")
                accessible += 1
            else:
                print(c, end="")
        print()
    return accessible


def part2(s: str):
    g = parseGrid(s)
    g = [[0 if c == "." else 1 for c in line] for line in g]
    total = 0

    def iterate(grid):
        nonlocal total
        for i, v in enumerate(grid):
            for j, c in enumerate(v):
                neighbours = 0
                if get(grid, i - 1, j - 1, default=0) > 0:
                    neighbours += 1
                if get(grid, i - 1, j, default=0) > 0:
                    neighbours += 1
                if get(grid, i - 1, j + 1, default=0) > 0:
                    neighbours += 1
                if get(grid, i, j - 1, default=0) > 0:
                    neighbours += 1
                if get(grid, i, j + 1, default=0) > 0:
                    neighbours += 1
                if get(grid, i + 1, j - 1, default=0) > 0:
                    neighbours += 1
                if get(grid, i + 1, j, default=0) > 0:
                    neighbours += 1
                if get(grid, i + 1, j + 1, default=0) > 0:
                    neighbours += 1
                if c > 0:
                    # print(neighbours, end="")
                    grid[i][j] = neighbours
                    if neighbours < 4:
                        total += 1
                else:
                    pass
                    # print(c, end="")
            # print()
        return [[0 if c < 4 else 1 for c in line] for line in g]

    last_total = -1
    while last_total < total:
        print(last_total, total)
        last_total = total
        g = iterate(g)

    return total


assert part1(example) == 13
assert part2(example) == 43


if __name__ == "__main__":
    with open("day4/input.txt") as f:
        input = f.read().strip()
    print("part1: ", part1(input))
    print("part2: ", part2(input))
