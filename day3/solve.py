example = """
987654321111111
811111111111119
234234234234278
818181911112111
""".strip()


def part1(s: str):
    banks = [[int(c) for c in bank] for bank in s.split("\n")]

    sum = 0
    for bank in banks:
        max_first = max(bank[:-1])
        max_last = max(bank[bank.index(max_first) + 1 :])
        joltage = max_first * 10 + max_last
        sum += joltage
    return sum


def find_next_digit(digits, remaining):
    # print(digits, remaining)
    assert len(digits) >= remaining
    if remaining == 1:
        return [max(digits)]
    remaining -= 1
    best = max(digits[:-remaining])
    best_i = digits.index(best)
    # print(best, best_i, digits[:-remaining])
    return [best] + find_next_digit(digits[best_i + 1 :], remaining)


def part2(s: str):
    banks = [find_next_digit([int(c) for c in bank], 12) for bank in s.split("\n")]
    max_joltage = sum([int("".join([str(i) for i in bank])) for bank in banks])

    return max_joltage


assert part1(example) == 357
assert part2(example) == 3121910778619


if __name__ == "__main__":
    with open("day3/input.txt") as f:
        input = f.read().strip()
    print("part1: ", part1(input))
    print("part2: ", part2(input))
