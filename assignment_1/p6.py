import sys, parse, grader
#i assumed that the input is in the expected format as it was discussed on the forum
def number_of_attacks(problem):
    queens = problem["queens"]
    rows = 8
    cols = 8
    copy_of_queens = dict(queens)
    lines = []

    for r in range(rows):
        row_values = []
        for c in range(cols):
            #moving queen in curr. column to row r now
            position = dict(copy_of_queens)
            position[c] = r
            count = 0 #start counting
            for c1 in range(cols):
                r1 = position[c1]
                for c2 in range(c1 + 1, cols):
                    r2 = position[c2]
                    if r1 == r2 or abs(r1 - r2) == abs(c1 - c2):
                        count += 1
            #for the formatting issues i encountered about the two digit numbers - this is the fix
            row_values.append(f"{count:2d}")
        lines.append(" ".join(row_values)) #again, to join them with a single space between them

    return "\n".join(lines)


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    grader.grade(problem_id, test_case_id, number_of_attacks, parse.read_8queens_search_problem)