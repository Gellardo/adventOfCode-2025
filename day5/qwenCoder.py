def part1(ranges, available_ids):
    # Convert ranges to a set of all fresh IDs for fast lookup
    fresh_ids = set()
    for start, end in ranges:
        for i in range(start, end + 1):
            fresh_ids.add(i)

    # Count how many available IDs are in the fresh set
    count = 0
    for id_ in available_ids:
        if id_ in fresh_ids:
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
print("Part 1 Example Result:", part1(ranges, available_ids))  # Expected: 3

# Test Part 2
print("Part 2 Example Result:", part2(ranges))  # Expected: 14

# Process actual input (replace with real file reading if needed)
# For example, assuming input is read from a file named "input.txt":
with open("input.txt", "r") as f:
    input_data = f.read().strip()

lines = input_data.split("\n")
blank_line_index = lines.index("")
ranges_lines = lines[:blank_line_index]
available_lines = lines[blank_line_index + 1 :]

ranges = []
for line in ranges_lines:
    start, end = map(int, line.split("-"))
    ranges.append((start, end))

available_ids = [int(line) for line in available_lines]

print("Part 1:", part1(ranges, available_ids))
print("Part 2:", part2(ranges))
