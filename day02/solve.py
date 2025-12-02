example = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""


def enumerate_range(start, stop):
    for i in range(start, stop + 1):
        yield i


def part1(s: str):
    ranges = [
        (int(r.split("-")[0]), int(r.split("-")[1])) for r in s.strip().split(",")
    ]
    sum = 0

    for r in ranges:
        for n in enumerate_range(r[0], r[1]):
            sn = str(n)
            if sn[: len(sn) // 2] == sn[len(sn) // 2 :]:
                # print(sn)
                sum += n
    return sum


def part2(s: str):
    ranges = [
        (int(r.split("-")[0]), int(r.split("-")[1])) for r in s.strip().split(",")
    ]
    sum = 0

    for r in ranges:
        found = set()
        for n in enumerate_range(r[0], r[1]):
            sn = str(n)
            for i in range(1, (len(sn) // 2) + 1):
                if i * (len(sn) // i) == len(sn) and sn == sn[:i] * (len(sn) // i):
                    if n not in found:
                        # print(i, sn)
                        sum += n
                    found.add(n)
    return sum


assert part1(example) == 1227775554
assert part2("95-115") == 99 + 111
assert part2("2220-2225") == 2222
assert part2(example) == 4174379265


if __name__ == "__main__":
    with open("input.txt") as f:
        input = f.read()
    print("part1: ", part1(input))
    print("part2: ", part2(input))
