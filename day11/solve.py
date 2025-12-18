import logging
from logging import info, debug
from collections import defaultdict

example = """
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
""".strip()

example2 = """
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
""".strip()


def all_paths(graph, start, end, including=[], excluding=[]):
    open = [start]
    paths = defaultdict(int)

    while len(open) > 0:
        current = open.pop()
        debug(f"{current=}, {len(open)=}")
        paths[current] += 1
        if current == end:
            continue

        new = graph[current]
        open.extend(new)

    return paths[end]


def part1(s: str):
    lines = s.split("\n")
    graph = {}
    for line in lines:
        [node, targets] = line.split(":")
        targets = targets.strip().split(" ")
        graph[node] = targets
    debug(graph)
    return all_paths(graph, "you", "out")


def part2(s: str):
    lines = s.split("\n")
    graph = {}
    for line in lines:
        [node, targets] = line.split(":")
        targets = targets.strip().split(" ")
        graph[node] = targets
    debug(graph)
    return all_paths(graph, "svr", "out", including=["fft", "dac"])


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

    assert part1(example) == 5
    assert part2(example2) == 2

    with open("day11/input.txt") as f:
        input = f.read().strip()
    print("part1: ", part1(input))
    print("part2: ", part2(input))
