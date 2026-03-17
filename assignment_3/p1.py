import sys, grader, parse
import random

def play_episode(problem):
    experience = ''
    #initializations:
    seed = problem['seed']
    noise = problem['noise']
    livingReward = problem['livingReward']
    grid = problem['grid']
    policy = problem['policy']
    random.seed(seed, version = 1)
    start_row, start_col = 0, 0
    for r in range(len(grid)): #finding starting pos.
        for c in range(len(grid[r])):
            if grid[r][c] == 'S':
                start_row = r
                start_col = c
                break
    agents_row, agents_col = start_row, start_col
    total_reward = 0.0
    direction_outcomes = {'N': ['N', 'E', 'W'], 'E': ['E', 'S', 'N'], 
                          'S': ['S', 'W', 'E'], 'W': ['W', 'N', 'S']}
    
    #print:
    def print_state(current_grid, agent_r, agent_c, reward):
        result = ''
        for r in range(len(current_grid)):
            row_str = ""
            for c in range(len(current_grid[r])):
                cell = current_grid[r][c]
                display_char = cell
                if r == agent_r and c == agent_c: #if agent here have to put P
                    display_char = 'P'
                row_str += f"{display_char:>5}"
            result += row_str + '\n'
        result += f"Cumulative reward sum: {round(reward, 10)}"
        return result
    experience += "Start state:\n"
    experience += print_state(grid, agents_row, agents_col, total_reward) + '\n'
    
    #game loop:
    while True:
        wanted = policy[agents_row][agents_col] #action that it wants to do
        if wanted == 'exit':
            experience += "-------------------------------------------- \n"
            experience += f"Taking action: exit (intended: exit)\n"
            exit_val = float(grid[agents_row][agents_col])
            total_reward += exit_val
            experience += f"Reward received: {exit_val}\n"
            experience += "New state:\n"
            agents_row, agents_col = -1, -1
            experience += print_state(grid, agents_row, agents_col, total_reward)
            break
        real = random.choices(population = direction_outcomes[wanted], #the actual move calculated
                              weights = [1 - noise * 2, noise, noise])[0]
        #change in coordinates: delta_r, delta_c:
        delta_r, delta_c = 0, 0
        if real == 'N': delta_r = -1
        elif real == 'S': delta_r = 1
        elif real == 'E': delta_c = 1
        elif real == 'W': delta_c = -1
        nextrow = agents_row + delta_r
        nextcol = agents_col + delta_c
        #check if we are hitting a wall or going out of the grid, 
        #we should stay at the same spot we were before:
        if(nextrow < 0 or nextrow >= len(grid) or nextcol < 0 or 
           nextcol >= len(grid[0]) or grid[nextrow][nextcol] == '#'):
            nextrow, nextcol = agents_row, agents_col
        experience += "-------------------------------------------- \n"
        experience += f"Taking action: {real} (intended: {wanted})\n"
        total_reward += livingReward #updating the reward
        experience += f"Reward received: {livingReward}\n"
        experience += "New state:\n"
        agents_row, agents_col = nextrow, nextcol #move
        experience += print_state(grid, agents_row, agents_col, total_reward) + '\n'
    
    return experience

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = 1
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)