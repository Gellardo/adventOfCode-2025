example = """
paste here
""".strip()


def part1(s: str):
    lines = s.split("\n")
    return 0


def part2(s: str):
    lines = s.split("\n")
    return 0


assert part1(example) == 0
assert part2(example) == 0


if __name__ == "__main__":
    with open("day|DAY|/input.txt") as f:
        input = f.read().strip()
    print("part1: ", part1(input))
    print("part2: ", part2(input))
