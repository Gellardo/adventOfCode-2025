example = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
""".strip()


import math


def part1(s: str, max_connections=1000):
    points = [list(map(int, l.split(","))) for l in s.split("\n")]
    shortest = []
    for i in range(len(points)):
        min_dist = math.inf
        min_i = 0
        for j in range(len(points)):
            if i == j:
                continue
            dist = math.dist(points[i], points[j])
            if dist < min_dist:
                min_dist = dist
                min_i = j
        shortest.append((min_dist, min_i))
    print(shortest)

    circuits = []
    connections = 0
    while connections < max_connections:
        (dist, p2) = min(shortest)
        p1 = shortest.index(min(shortest))
        print(p1, p2, dist, points[p1], points[p2])
        shortest[p1] = (math.inf, -1)
        if any([c for c in circuits if p1 in c and p2 in c]):
            continue
        connections += 1
        p1_c = [i for (i, c) in enumerate(circuits) if p1 in c]
        p2_c = [i for (i, c) in enumerate(circuits) if p2 in c]
        if len(p1_c) > 0 and len(p2_c) > 0:
            circuits[p1_c[0]].union(circuits[p2_c[0]])
        elif len(p1_c) > 0:
            circuits[p1_c[0]].add(p2)
        elif len(p2_c) > 0:
            circuits[p2_c[0]].add(p1)
        else:
            circuits.append(set([p1, p2]))
        print(circuits)

    print(len(circuits), sorted(list(map(lambda c: len(c), circuits)))[-4:])
    return math.prod(sorted(list(map(lambda c: len(c), circuits)))[:4])


def part2(s: str):
    lines = s.split("\n")
    return 0


assert part1(example, max_connections=10) == 40
assert part2(example) == 0


if __name__ == "__main__":
    with open("day8/input.txt") as f:
        input = f.read().strip()
    print("part1: ", part1(input))
    print("part2: ", part2(input))
