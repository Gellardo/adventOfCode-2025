example = """
3-5
10-14
16-20
12-18

1
5
8
11
17
32
""".strip()


def part1(s: str):
    ranges, items = s.split("\n\n")
    ranges = [
        range(int(r.split("-")[0]), int(r.split("-")[1]) + 1)
        for r in ranges.split("\n")
    ]
    items = [int(i) for i in items.split("\n")]
    count = 0
    for item in items:
        if any((item in range for range in ranges)):
            count += 1
    return count


def part2(s: str):
    ranges, _ = s.split("\n\n")
    ranges = [
        range(int(r.split("-")[0]), int(r.split("-")[1]) + 1)
        for r in ranges.split("\n")
    ]
    open = ranges
    combined = []
    last_len = len(ranges) + 1
    while last_len > len(open):
        last_len = len(open)
        combined = []
        for r in open:
            for i, c in enumerate(combined):
                if r.stop < c.start or r.start > c.stop:
                    pass
                else:
                    combined[i] = range(min(r.start, c.start), max(r.stop, c.stop))
                    break
            else:
                combined.append(r)
        open = combined

    return sum([r.stop - r.start for r in combined])


assert part1(example) == 3
assert part2(example) == 14


if __name__ == "__main__":
    with open("day5/input.txt") as f:
        input = f.read().strip()
    print("part1: ", part1(input))
    print("part2: ", part2(input))
