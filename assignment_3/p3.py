import sys, grader, parse

def value_iteration(problem):
    #initializations
    discount = problem['discount']
    noise = problem['noise']
    livingReward = problem['livingReward']
    iterations_count = problem['iterations']
    grid = problem['grid']
    no_rows = len(grid)
    no_cols = len(grid[0])
    curr_values = [[0.0 for _ in range(no_cols)] for _ in range(no_rows)]
    return_value = ''
    moves = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
    perpendiculars = {'N': ['W', 'E'], 'S': ['E', 'W'], 'E': ['N', 'S'], 'W': ['S', 'N']}
    possibilities = ['N', 'E', 'S', 'W'] #tie breaking order
    def getting_value(row, col, direction, values):
        direction_r, direction_c = moves[direction]
        numrow, numcol = row + direction_r, col + direction_c
        if numrow < 0 or numrow >= no_rows or numcol < 0 or numcol >= no_cols or grid[numrow][numcol] == '#':
            return values[row][col]
        return values[numrow][numcol]
    def printing_format(k, values): #formatting the output here, helper
        solution = f"V_k={k}\n"
        for r in range(no_rows):
            for c in range(no_cols):
                if grid[r][c] == '#':
                    solution += "| ##### |"
                else:
                    solution += "|{:7.2f}|".format(values[r][c])
            solution += "\n"
        return solution
    def printing_format_policy(k, policy_grid):#formatting policy output here, helper
        solution = f"pi_k={k}\n"
        for r in range(no_rows):
            for c in range(no_cols):
                solution += f"| {policy_grid[r][c]} |"
            solution += "\n"
        return solution
    return_value += printing_format(0, curr_values) #printing k = 0
    #main loop:
    #i am actually following a very similar manner to p2 here
    for k in range(1, iterations_count):
        new_vals = [[0.0 for _ in range(no_cols)] for _ in range(no_rows)]
        policy = [['' for _ in range(no_cols)] for _ in range(no_rows)]
        for row in range(no_rows):
            for col in range(no_cols):
                pos = grid[row][col]
                if pos == '#': #if wall
                    new_vals[row][col] = 0.0
                    policy[row][col] = '#'
                    continue
                if isinstance(pos, (float, int)): #if numeric value - the exit cells are numbers so this is how i identify
                    new_vals[row][col] = float(pos)
                    policy[row][col] = 'x'
                    continue
                best_q_value = -float('inf')
                best_move = ''
                for move in possibilities:
                    wanted = getting_value(row, col, move, curr_values)
                    pdirections = perpendiculars[move] #nosie directions
                    noise1 = getting_value(row, col, pdirections[0], curr_values)
                    noise2 = getting_value(row, col, pdirections[1], curr_values)
                    wanted_val = (1 - 2 * noise) * wanted
                    noise_val = (noise * noise1) + (noise * noise2)
                    weighted_total = wanted_val + noise_val
                    q = livingReward + discount * weighted_total
                    if q > best_q_value: #maximum check, if equal keep, order preserved
                        best_q_value = q
                        best_move = move
                new_vals[row][col] = best_q_value
                policy[row][col] = best_move
        curr_values = new_vals
        return_value += printing_format(k, curr_values)
        return_value += printing_format_policy(k, policy)
    return return_value[:-1] #removed the last line it is just a "\n" - just like in p2

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = -4
    problem_id = 3
    grader.grade(problem_id, test_case_id, value_iteration, parse.read_grid_mdp_problem_p3)