def solve_cafeteria(puzzle_input):
    """
    Solves both parts of the Advent of Code Day 5: Cafeteria puzzle.

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
    fresh_ranges = []
    for r_str in fresh_ranges_str.split("\n"):
        start, end = map(int, r_str.split("-"))
        fresh_ranges.append((start, end))

    # Parse available ingredient IDs
    available_ids = set(map(int, available_ids_str.split("\n")))

    # --- Part 1: Count fresh available ingredient IDs ---
    fresh_available_count = 0
    for ingredient_id in available_ids:
        is_fresh = False
        for start, end in fresh_ranges:
            if start <= ingredient_id <= end:
                is_fresh = True
                break
        if is_fresh:
            fresh_available_count += 1

    # --- Part 2: Count total unique fresh ingredient IDs from ranges ---
    unique_fresh_ids = set()
    for start, end in fresh_ranges:
        for i in range(start, end + 1):
            unique_fresh_ids.add(i)
    total_unique_fresh_count = len(unique_fresh_ids)

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

# You can replace this with your actual puzzle input to get your answers
# For example:
with open("input.txt", "r") as f:
    your_puzzle_input = f.read()

your_part1_answer, your_part2_answer = solve_cafeteria(your_puzzle_input)
print(f"Your Part 1 answer: {your_part1_answer}")
print(f"Your Part 2 answer: {your_part2_answer}")
