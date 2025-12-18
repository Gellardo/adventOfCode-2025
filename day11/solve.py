import logging
from logging import info, debug
from collections import defaultdict
import math

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
    if len(including) == 0:
        return all_paths_internal(graph, start, end, excluding=excluding)
    if len(including) != 2:
        raise NotImplementedError

    int1, int2 = including
    start2int1 = all_paths_dfs(graph, start, int1, excluding=[int2, end])
    int12int2 = all_paths_dfs(graph, int1, int2, excluding=[start, end])
    int22end = all_paths_dfs(graph, int2, end, excluding=[start, int1])
    path1 = [start2int1, int12int2, int22end]
    paths_via_int1_then_int2 = (
        math.prod(path1) if all([paths > 0 for paths in path1]) else 0
    )
    info(f"{paths_via_int1_then_int2} = prod({path1})")
    # example and my input both use this path, but unnecessary
    # return paths_via_int1_then_int2

    start2int2 = all_paths_dfs(graph, start, int2, excluding=[int1, end])
    int22int1 = all_paths_dfs(graph, int2, int1, excluding=[start, end])
    int12end = all_paths_dfs(graph, int1, end, excluding=[start, int2])
    path2 = [start2int2, int22int1, int12end]
    paths_via_int2_then_int1 = (
        math.prod(path2) if all([paths > 0 for paths in path2]) else 0
    )
    info(f"{paths_via_int2_then_int1} = prod({path2})")

    info(f"number paths = min({paths_via_int1_then_int2=} {paths_via_int2_then_int1=})")
    return max(paths_via_int1_then_int2, paths_via_int2_then_int1)


def all_paths_internal(graph, start, end, excluding=[]):
    open = [start]
    paths = defaultdict(int)

    while len(open) > 0:
        current = open.pop()
        debug(f"{current=}, {len(open)=}")
        paths[current] += 1
        if current in excluding or current == end:
            continue
        # in part2 there seems to be a loop somewhere, so best guess for a max
        # Learning: no it is not a loop, just 17 million paths
        if paths[current] > 1000:
            continue

        new = graph[current]
        open.extend(new)

    return paths[end]


def all_paths_dfs(graph, start, end, excluding):
    path = [start]
    options = [0]
    found = 0
    memo = 0
    paths = defaultdict(int)
    paths[end] = 1

    while len(options) > 0:
        current = path[-1]
        option = options[-1]
        outgoing = graph[current] if current in graph else []

        if current == end:
            found += 1
            info("found path: %s, %s, %d", path, options, found)
            path.pop()
            options.pop()
            continue
        elif option >= len(outgoing):
            debug("finished current: %s, path: %s", current, path)
            paths[current] = sum([paths[out] for out in outgoing])
            path.pop()
            options.pop()
            continue
        else:
            options[-1] = option + 1

        if outgoing[option] in excluding:
            continue
        if outgoing[option] in paths:
            memo += 1
            continue
        if outgoing[option] in path:
            info("loop detected: %s, next: %s", path, outgoing[option])
            continue
        path.append(outgoing[option])
        options.append(0)
    info(f"{paths[end]=} using {memo=}")
    return paths[start]


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
