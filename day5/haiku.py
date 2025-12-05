def parse_input(data):
    """Parse the input into ranges and available IDs"""
    parts = data.strip().split("\n\n")

    # Parse ranges
    ranges = []
    for line in parts[0].strip().split("\n"):
        start, end = map(int, line.split("-"))
        ranges.append((start, end))

    # Parse available IDs
    available_ids = []
    for line in parts[1].strip().split("\n"):
        available_ids.append(int(line))

    return ranges, available_ids


def is_fresh(ingredient_id, ranges):
    """Check if an ingredient ID is in any range"""
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def part1(data):
    """Count how many available IDs are fresh"""
    ranges, available_ids = parse_input(data)
    return sum(1 for id in available_ids if is_fresh(id, ranges))


def merge_ranges(ranges):
    """Merge overlapping ranges"""
    if not ranges:
        return []

    # Sort ranges by start position
    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]

    for current_start, current_end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]

        # If current range overlaps with last merged range
        if current_start <= last_end + 1:
            # Merge them
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            # No overlap, add as new range
            merged.append((current_start, current_end))

    return merged


def part2(data):
    """Count total unique IDs considered fresh by ranges"""
    ranges, _ = parse_input(data)

    # Merge overlapping ranges
    merged = merge_ranges(ranges)

    # Count total IDs in all merged ranges
    total = 0
    for start, end in merged:
        total += end - start + 1

    return total


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

print("Testing with example:")
print(f"Part 1: {part1(test_input)}")
print(f"Expected: 3")
print()
print(f"Part 2: {part2(test_input)}")
print(f"Expected: 14")
print()

# Verify Part 1 logic with individual checks
ranges, available_ids = parse_input(test_input)
print("Part 1 breakdown:")
for id in available_ids:
    fresh = is_fresh(id, ranges)
    print(f"  ID {id}: {'fresh' if fresh else 'spoiled'}")
print()

# Verify Part 2 logic
print("Part 2 breakdown:")
print(f"  Original ranges: {sorted(ranges)}")
merged = merge_ranges(ranges)
print(f"  Merged ranges: {merged}")
print(f"  Range details:")
all_fresh_ids = set()
for start, end in merged:
    ids_in_range = list(range(start, end + 1))
    all_fresh_ids.update(ids_in_range)
    print(f"    {start}-{end}: {len(ids_in_range)} IDs")
print(f"  All fresh IDs: {sorted(all_fresh_ids)}")
