def part1(ranges, available_ids):
    # Convert ranges to a set of all fresh IDs for fast lookup
    # But we don't generate all IDs - just check if each available ID is in any range
    def is_fresh(id_):
        for start, end in ranges:
            if start <= id_ <= end:
                return True
        return False

    count = 0
    for id_ in available_ids:
        if is_fresh(id_):
            count += 1
    return count


def merge_ranges(ranges):
    # Sort ranges by start value
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    if not sorted_ranges:
        return []

    merged = [sorted_ranges[0]]
    for current_start, current_end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        # If current range overlaps or is adjacent to the last one
        if current_start <= last_end + 1:
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            merged.append((current_start, current_end))

    return merged


def part2(ranges):
    # Merge overlapping ranges
    merged = merge_ranges(ranges)

    # Count total IDs in all merged ranges
    count = 0
    for start, end in merged:
        count += end - start + 1
    return count


# For large ranges, we can optimize the lookup in part1 using binary search or set operations
def part1_optimized(ranges, available_ids):
    # Sort ranges for binary search optimization
    sorted_ranges = sorted(ranges, key=lambda x: x[0])

    def is_fresh(id_):
        # Binary search approach - but for simplicity with small number of ranges
        # we'll use the direct check (still efficient enough)
        for start, end in sorted_ranges:
            if start <= id_ <= end:
                return True
        return False

    count = 0
    for id_ in available_ids:
        if is_fresh(id_):
            count += 1
    return count


# Example input from problem description
example_input = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

# Parse example input
lines = example_input.strip().split("\n")
blank_line_index = lines.index("")
ranges_lines = lines[:blank_line_index]
available_lines = lines[blank_line_index + 1 :]

# Parse ranges
ranges = []
for line in ranges_lines:
    start, end = map(int, line.split("-"))
    ranges.append((start, end))

# Parse available IDs
available_ids = [int(line) for line in available_lines]

# Test Part 1
print("Part 1 Example Result:", part1_optimized(ranges, available_ids))  # Expected: 3

# Test Part 2
print("Part 2 Example Result:", part2(ranges))  # Expected: 14


# For large ranges, let's handle the actual problem properly
def solve_real_problem(input_file):
    with open(input_file, "r") as f:
        content = f.read().strip()

    lines = content.split("\n")
    blank_line_index = lines.index("")
    ranges_lines = lines[:blank_line_index]
    available_lines = lines[blank_line_index + 1 :]

    # Parse ranges
    ranges = []
    for line in ranges_lines:
        start, end = map(int, line.split("-"))
        ranges.append((start, end))

    # Parse available IDs
    available_ids = [int(line) for line in available_lines]

    # Part 1: Count fresh IDs from available list
    part1_result = part1_optimized(ranges, available_ids)

    # Part 2: Count total fresh IDs from ranges
    part2_result = part2(ranges)

    return part1_result, part2_result


# Since we don't have the actual file here, let's make sure our logic works with larger numbers
# by simulating with some large ranges

# Test with a larger example to verify the approach works for big numbers
large_ranges = [(1, 1000000), (2000000, 3000000), (5000000, 6000000)]
large_available = [500000, 1500000, 2500000, 5500000, 7000000]

print("Large ranges test:")
print("Part 1:", part1_optimized(large_ranges, large_available))
print("Part 2:", part2(large_ranges))


# Actually let's make one more optimization for the case where available IDs are too many to iterate
def part1_final(ranges, available_ids):
    # Create a set of all range start and end points for quick binary search
    import bisect

    # Sort ranges by start point
    sorted_ranges = sorted(ranges, key=lambda x: x[0])

    # For better performance with many available IDs, we can use a more efficient approach
    # But for now let's stick with the working solution that handles large ranges correctly

    count = 0
    for id_ in available_ids:
        # Simple linear search - but this is efficient enough for reasonable input sizes
        found = False
        for start, end in sorted_ranges:
            if start <= id_ <= end:
                found = True
                break
        if found:
            count += 1

    return count


# Final test with the example
print("Final test:")
print("Part 1:", part1_final(ranges, available_ids))
print("Part 2:", part2(ranges))

# Let's make sure we can handle the case where ranges span very large numbers efficiently
# This is what matters - we don't create all the IDs in memory, just work with ranges
