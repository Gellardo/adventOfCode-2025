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
    print("part1: ", count)


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
        if s[0] == "L":
            curr -= n
        else:
            curr += n
        if before != 0 and curr < 0 or curr > 100:
            count += 1
        curr = curr % 100
        if curr == 0:
            count += 1
        if n > 100:
            count += n // 100
        # print(s, curr, count)
    print("part2: ", count)


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        with open("day1-in.txt") as f:
            input = f.read()
    else:
        input = example
    part1(input)
    part2(input)
