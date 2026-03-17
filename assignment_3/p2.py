import sys, grader, parse

def policy_evaluation(problem):
    #initializations:
    discount = problem['discount']
    noise = problem['noise']
    livingReward = problem['livingReward']
    iterations_count = problem['iterations']
    grid = problem['grid']
    policy = problem['policy']
    no_rows = len(grid)
    no_cols = len(grid[0]) #this is just one of the cols...
    current_vals = [[0.0 for _ in range(no_cols)] for _ in range(no_rows)]
    return_value = ''
    moves = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0,-1)}
    perpendiculars = {'N': ['W', 'E'], 'S': ['E', 'W'], 'E': ['N', 'S'], 'W': ['S', 'N']}
    def get_value_of_state(r, c, direction, values): #get valu of state, walls, bounds
        dr, dc = moves[direction]
        numrow, numcol = r + dr, c + dc
        if numrow < 0 or numrow >= no_rows or numcol < 0 or numcol >= no_cols or grid[numrow][numcol] == '#':
           return values[r][c]
        return values[numrow][numcol]
    def print_format_output(k, values):
        solution = f"V^pi_k={k}\n"
        for r in range(no_rows):
            for c in range(no_cols):
                if grid[r][c] == '#':
                    solution += "| ##### |"
                else:
                    solution += "|{:7.2f}|".format(values[r][c])
            solution += "\n"
        return solution
    return_value += print_format_output(0, current_vals) #printing k = 0
    for k in range(1, iterations_count):
        new_values = [[0.0 for _ in range(no_cols)] for _ in range(no_rows)]
        for row in range(no_rows):
            for col in range(no_cols):
                pos = grid[row][col]
                if pos == '#': #if it is a wall stay where u are
                    continue
                if isinstance(pos, (float, int)): #numbers stay (bcs. theyre exit state)
                    new_values[row][col] = float(pos)
                    continue
                move = policy[row][col]
                if move == 'exit':
                    new_values[row][col] = livingReward
                    continue
                wanted = get_value_of_state(row, col, move, current_vals)
                pdirections = perpendiculars[move]
                noise1 = get_value_of_state(row, col, pdirections[0], current_vals)
                noise2 = get_value_of_state(row, col, pdirections[1], current_vals)
                weighted_sum = ( (1 - 2 * noise) * wanted + (noise * noise1) + (noise * noise2)) #the equation
                new_values[row][col] = livingReward + discount * weighted_sum
        current_vals = new_values
        return_value += print_format_output(k, current_vals)
    return return_value[:-1] #removed the last line it is just a "\n"!!! --> later adjustment when failed

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = -7
    problem_id = 2
    grader.grade(problem_id, test_case_id, policy_evaluation, parse.read_grid_mdp_problem_p2)