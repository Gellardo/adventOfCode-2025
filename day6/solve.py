example = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """


def part1(s: str):
    grid = [
        [e for e in line.split(" ") if e != ""]
        for line in s.split("\n")
        if line.strip() != ""
    ]
    # print(grid)
    check = 0
    for j in range(len(grid[-1])):
        op = grid[-1][j]
        if op == "+":
            agg_f = lambda x, y: x + y
            agg = 0
        elif op == "*":
            agg_f = lambda x, y: x * y
            agg = 1
        else:
            raise NotImplementedError("unsupported opp")
        for i in range(len(grid) - 1):
            agg = agg_f(agg, int(grid[i][j]))
        check += agg
    return check


def part2(s: str):
    grid = [[c for c in line] for line in s.split("\n") if line.strip() != ""]
    assert len(grid[0]) == len(grid[-1])
    check = 0
    current_numbers = []
    for j in range(len(grid[-1]) - 1, -1, -1):
        n = [grid[i][j] for i in range(len(grid) - 1)]
        n = "".join(n).strip()
        if n != "":
            current_numbers.append(int(n))
        op = grid[-1][j]
        if op == "+":
            # print(current_numbers, op, end=" ")
            agg = sum(current_numbers)
            # print(agg)
            check += agg
            current_numbers = []
        elif op == "*":
            # print(current_numbers, op, end=" ")
            agg_f = lambda x, y: x * y
            agg = 1
            for i in range(len(current_numbers)):
                agg = agg_f(agg, int(current_numbers[i]))
            # print(agg)
            check += agg
            current_numbers = []
    return check


assert part1(example) == 4277556
assert part2(example) == 3263827


if __name__ == "__main__":
    with open("day6/input.txt") as f:
        input = f.read()
    print("part1: ", part1(input))
    print("part2: ", part2(input))
