def part1(ranges, available_ids):
    # For each available ID, check if it's in any range
    count = 0
    for id_ in available_ids:
        found = False
        for start, end in ranges:
            if start <= id_ <= end:
                found = True
                break
        if found:
            count += 1
    return count


def merge_ranges(ranges):
    # Sort ranges by start value and merge overlapping ones
    if not ranges:
        return []

    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    merged = [sorted_ranges[0]]

    for current_start, current_end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        if current_start <= last_end + 1:
            # Overlapping or adjacent ranges - merge them
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            merged.append((current_start, current_end))

    return merged


def part2(ranges):
    # Merge overlapping ranges and count total IDs
    merged = merge_ranges(ranges)

    count = 0
    for start, end in merged:
        count += end - start + 1
    return count


# Read from input.txt
with open("input.txt", "r") as f:
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

# Solve both parts
part1_result = part1(ranges, available_ids)
part2_result = part2(ranges)

print(part1_result)
print(part2_result)
