def solve_cafeteria(puzzle_input):
    """
    Solves both parts of the Advent of Code Day 5: Cafeteria puzzle,
    optimized for large ingredient IDs.

    Args:
        puzzle_input (str): A string containing the puzzle input,
                            with fresh ingredient ID ranges and available
                            ingredient IDs separated by a blank line.

    Returns:
        tuple: A tuple containing two integers:
               - The count of fresh available ingredient IDs (Part 1).
               - The total count of unique fresh ingredient IDs from the ranges (Part 2).
    """

    fresh_ranges_str, available_ids_str = puzzle_input.strip().split("\n\n")

    # Parse fresh ingredient ID ranges
    fresh_ranges_data = []
    for r_str in fresh_ranges_str.split("\n"):
        start, end = map(int, r_str.split("-"))
        fresh_ranges_data.append((start, end))

    # Parse available ingredient IDs
    available_ids = set(map(int, available_ids_str.split("\n")))

    # --- Part 1: Count fresh available ingredient IDs ---
    fresh_available_count = 0
    for ingredient_id in available_ids:
        is_fresh = False
        for start, end in fresh_ranges_data:
            if start <= ingredient_id <= end:
                is_fresh = True
                break
        if is_fresh:
            fresh_available_count += 1

    # --- Part 2: Count total unique fresh ingredient IDs from ranges (Optimized) ---

    # 1. Sort the ranges by their start values. This is crucial for merging.
    fresh_ranges_data.sort()

    # 2. Merge overlapping ranges
    merged_ranges = []
    if not fresh_ranges_data:
        total_unique_fresh_count = 0
    else:
        current_start, current_end = fresh_ranges_data[0]
        for next_start, next_end in fresh_ranges_data[1:]:
            # If the next range overlaps or touches the current merged range
            if next_start <= current_end + 1:
                current_end = max(current_end, next_end)
            else:
                # No overlap, so add the current merged range and start a new one
                merged_ranges.append((current_start, current_end))
                current_start, current_end = next_start, next_end
        # Add the last merged range
        merged_ranges.append((current_start, current_end))

        # 3. Calculate the total count from the merged, non-overlapping ranges
        total_unique_fresh_count = 0
        for start, end in merged_ranges:
            total_unique_fresh_count += end - start + 1

    return fresh_available_count, total_unique_fresh_count


def test_solve_cafeteria():
    """
    Tests the solve_cafeteria function with the provided example.
    """
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

    expected_part1 = 3
    expected_part2 = 14

    result_part1, result_part2 = solve_cafeteria(example_input)

    assert result_part1 == expected_part1, (
        f"Part 1 failed. Expected {expected_part1}, got {result_part1}"
    )
    assert result_part2 == expected_part2, (
        f"Part 2 failed. Expected {expected_part2}, got {result_part2}"
    )

    print("Example tests passed!")


# Run the tests
test_solve_cafeteria()

# To use with your actual puzzle input:
try:
    with open("input.txt", "r") as f:
        your_puzzle_input = f.read()
    your_part1_answer, your_part2_answer = solve_cafeteria(your_puzzle_input)
    print(f"Your Part 1 answer: {your_part1_answer}")
    print(f"Your Part 2 answer: {your_part2_answer}")
except FileNotFoundError:
    print("Please create 'day5_input.txt' with your puzzle input.")
