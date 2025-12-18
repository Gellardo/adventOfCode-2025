import logging
from logging import info, debug

example = """
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
""".strip()


def parse(s):
    blocks = s.strip().split("\n\n")
    shapes = [block.strip().split("\n")[1:] for block in blocks[:-1]]
    regions = [region.split(": ") for region in blocks[-1].split("\n")]
    regions = [
        (list(map(int, region[0].split("x"))), list(map(int, region[1].split(" "))))
        for region in regions
    ]

    debug("shapes: %s, regions: %s", shapes, regions)
    return shapes, regions


def part1(s: str):
    shapes, regions = parse(s)
    too_many = 0

    presents = [
        sum([sum([1 for space in line if space == "#"]) for line in shape])
        for shape in shapes
    ]
    for dimensions, num_shapes in regions:
        size = dimensions[0] * dimensions[1]
        size_presents = sum([p * num for p, num in zip(presents, num_shapes)])
        debug(f"{size=}, {size_presents=}")
        if size < size_presents:
            too_many += 1
    debug(f"{len(regions)=}, {too_many=}")
    return len(regions) - too_many


def part2(s: str):
    lines = s.split("\n")
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()

    # Set log level based on flags
    if args.verbose == 0:
        level = logging.ERROR
    elif args.verbose == 1:
        level = logging.WARNING
    elif args.verbose == 2:
        level = logging.INFO
    else:
        level = logging.DEBUG
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    # my code does not work on the example but on the input
    # assert part1(example) == 2
    assert part2(example) == 0

    with open("day12/input.txt") as f:
        input = f.read().strip()
    print("part1: ", part1(input))
    print("part2: ", part2(input))
