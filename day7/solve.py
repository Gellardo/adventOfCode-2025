example = """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
""".strip()


def part1(s: str):
    lines = s.split("\n")
    beams = set([lines[0].index("S")])
    split = 0
    for i in range(1, len(lines)):
        new_beams = set()
        for beam in beams:
            if lines[i][beam] == ".":
                new_beams.add(beam)
            else:
                split += 1
                new_beams.add(beam - 1)
                new_beams.add(beam + 1)
        beams = new_beams
        # print(beams, len(beams))

    return split


from collections import defaultdict


def part2(s: str):
    lines = s.split("\n")
    beams = {lines[0].index("S"): 1}
    for i in range(1, len(lines)):
        new_beams = defaultdict(int)
        for beam in beams:
            if lines[i][beam] == ".":
                new_beams[beam] += beams[beam]
            else:
                new_beams[beam - 1] += beams[beam]
                new_beams[beam + 1] += beams[beam]
        beams = new_beams
        # print(beams, len(beams))

    return sum([beams[beam] for beam in beams])


assert part1(example) == 21
assert part2(example) == 40


if __name__ == "__main__":
    with open("day7/input.txt") as f:
        input = f.read().strip()
    print("part1: ", part1(input))
    print("part2: ", part2(input))
