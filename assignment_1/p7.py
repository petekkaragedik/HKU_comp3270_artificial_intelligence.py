import sys, parse, grader

def better_board(problem):
    queens = dict(problem["queens"])
    rows = 8
    cols = 8

    def total_attacks(position):
        count = 0
        for c1 in range(cols):
            r1 = position[c1]
            for c2 in range(c1 + 1, cols):
                r2 = position[c2]
                if r1 == r2 or abs(r1 - r2) == abs(c1 - c2):
                    count += 1
        return count
    #calculated the initial best score first
    best_score = total_attacks(queens)
    best_move = None #initialized as none
#i will just iterate over rows for each coulmn's queens and calculate total # of attacks for each and compare
    for r in range(rows):
        for c in range(cols):
            if queens[c] == r:
                continue  #skipping if we have queen there already
            position = dict(queens)
            position[c] = r
            score = total_attacks(position)
            if score < best_score:
                best_score = score
                best_move = (c, r)

    if best_move:
        col, new_row = best_move
        queens[col] = new_row
    #updated board
    board = []
    for r in range(rows):
        row_vals = []
        for c in range(cols):
            if queens[c] == r:
                row_vals.append("q")
            else:
                row_vals.append(".")
        board.append(" ".join(row_vals))

    return "\n".join(board)


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 7
    grader.grade(problem_id, test_case_id, better_board, parse.read_8queens_search_problem)