example = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""


def part1(s: str):
    steps = s.split("\n")

    start = 50
    count = 0
    curr = start
    for s in steps:
        if s == "":
            continue
        n = int(s[1:])
        if s[0] == "L":
            curr -= n
        else:
            curr += n
        curr = curr % 100
        # print(curr)
        if curr == 0:
            count += 1
    return count


def part2(s: str):
    steps = s.split("\n")

    start = 50
    count = 0
    curr = start
    for s in steps:
        if s == "":
            continue
        before = curr
        n = int(s[1:])
        if n > 100:
            count += n // 100
            n = n % 100

        if s[0] == "L":
            curr -= n
        else:
            curr += n

        if curr % 100 == 0:
            count += 1
        # went over 0
        if curr < 0 or curr > 100:
            # if we started not on 0
            if before != 0:
                count += 1
        curr = curr % 100
        # print(s, curr, count)
    return count


assert part1(example) == 3
assert part2(example) == 6
assert part2("L100") == 1
assert part2("L50") == 1
assert part2("L150") == 2
assert part2("R1000") == 10
assert part2("R100") == 1
assert part2("L50\nR100") == 2
assert part2("L51\nR2\nL3\nR2") == 4


if __name__ == "__main__":
    with open("day1/input.txt") as f:
        input = f.read()
    print("part1: ", part1(input))
    print("part2: ", part2(input))
