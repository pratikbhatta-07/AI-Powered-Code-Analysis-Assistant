def analyze_complexity(code: str) -> str:

    code = code.lower()

    for_count = code.count("for")
    while_count = code.count("while")

    total_loops = for_count + while_count

    if total_loops == 0:

        if "recursion" in code:
            return "Time Complexity: O(n) (Possible Recursion)"

        return "Time Complexity: O(1)"

    elif total_loops == 1:

        return "Time Complexity: O(n)"

    elif total_loops == 2:

        return "Time Complexity: O(n²)"

    elif total_loops == 3:

        return "Time Complexity: O(n³)"

    else:

        return "Time Complexity: Complexity could not be determined accurately"