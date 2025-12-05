def parse_input(input_text):
    """Parse the input into ranges and ingredient IDs."""
    parts = input_text.strip().split("\n\n")

    # Parse ranges
    ranges = []
    for line in parts[0].strip().split("\n"):
        start, end = map(int, line.split("-"))
        ranges.append((start, end))

    # Parse ingredient IDs (only for part 1)
    ingredient_ids = []
    if len(parts) > 1:
        ingredient_ids = [int(line) for line in parts[1].strip().split("\n")]

    return ranges, ingredient_ids


def is_fresh(ingredient_id, ranges):
    """Check if an ingredient ID falls within any fresh range."""
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def merge_ranges(ranges):
    """Merge overlapping ranges and return list of non-overlapping ranges."""
    if not ranges:
        return []

    # Sort ranges by start position
    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]

    for start, end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]

        # If current range overlaps or is adjacent to last range, merge them
        if start <= last_end + 1:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))

    return merged


def count_fresh_in_ranges(ranges):
    """Count total number of IDs covered by ranges."""
    merged = merge_ranges(ranges)
    total = 0
    for start, end in merged:
        total += end - start + 1
    return total


def solve_part1(input_text):
    """Solve part 1: Count fresh ingredients from available list."""
    ranges, ingredient_ids = parse_input(input_text)
    fresh_count = sum(1 for id in ingredient_ids if is_fresh(id, ranges))
    return fresh_count


def solve_part2(input_text):
    """Solve part 2: Count all IDs covered by ranges."""
    ranges, _ = parse_input(input_text)
    return count_fresh_in_ranges(ranges)


# Test with the example
test_input = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

# Test Part 1
result1 = solve_part1(test_input)
print(f"Part 1 (example): {result1}")
assert result1 == 3, f"Expected 3, got {result1}"

# Test Part 2
result2 = solve_part2(test_input)
print(f"Part 2 (example): {result2}")
assert result2 == 14, f"Expected 14, got {result2}"

print("\nAll tests passed!")

# If you have your puzzle input, you can solve it like this:
with open("input.txt", "r") as f:
    puzzle_input = f.read()

print(f"Part 1 answer: {solve_part1(puzzle_input)}")
print(f"Part 2 answer: {solve_part2(puzzle_input)}")
