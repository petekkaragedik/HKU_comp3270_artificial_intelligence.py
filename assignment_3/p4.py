#to run this code, paste this in the terminal if you are using mac:
#python3 p4.py

#my analysis:
#The agent starts with no info, all Q values are 0.
#First, since epsilon is high it runs through grid in a random mannner - exploration (from lecture slides)
#As episode goes on, epsilon decays, agent uses learned Q values more - exploitation
#When it finally comes to 5000 - 6000 episode policy approaches optimal
#We previously found this optimal in problem 3.
#The success ratio is high, meaning my implementation is actually robust

import random

discount = 1.0
noise = 0.1
livingReward = -0.01
grid = [[0.0, 0.0, 0.0, 1.0], [0.0, '#', 0.0, -1.0], [0.0, 0.0, 0.0, 0.0]]
no_rows = 3
no_cols = 4
#this is a reference optimal policy grid we found in problem 3 test case 2:
optimal_policy_grid = [['E', 'E', 'E', 'x'], ['N', '#', 'W', 'x'], ['N', 'W', 'W', 'S']]
actions = ['N', 'E', 'S', 'W']
moves = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
#helper func.s:
def next_state(row, col, action):
    if action == 'N':  #possible outcomes listed for all cases
        choices = ['N', 'E', 'W']
    elif action == 'S': 
        choices = ['S', 'E', 'W']
    elif action == 'E':
        choices = ['E', 'N', 'S']
    elif action == 'W': 
        choices = ['W', 'N', 'S']
    probabilities = [1 - 2 * noise, noise, noise] #the possibility distribution
    what_it_did_actually = random.choices(choices, weights = probabilities)[0]
    #calculating the new position after the random move:
    direction_row, direction_col = moves[what_it_did_actually]
    new_row, new_col = row + direction_row, col + direction_col
    #are we going to a wall or boundary?
    if new_row < 0 or new_row >= no_rows or new_col < 0 or new_col >= no_cols:
        return row, col
    if grid[new_row][new_col] == '#':
        return row, col
    return new_row, new_col
def find_best_action(row, col, Qtable): #best action in Q table for a position
    value_best = -float('inf')
    action_best = ''
    for i in actions:
        value = Qtable[(row, col, i)]
        if value > value_best:
            value_best = value
            action_best = i
    return action_best
def Qlearning(): #the q learning algorithm
    Qtable = {}
    for row in range(no_rows):
        for col in range(no_cols):
            for i in actions:
                Qtable[(row, col, i)] = 0.0
    #parameters:
    episodes = 6000
    alpha = 0.5
    epsilon = 0.5
    minimum_alpha = 0.01
    minimum_epsilon = 0.01
    decay_rate = 0.999
    #episode loop:
    for e in range(episodes):
        while(True): #random start point selection
            r = random.randint(0, no_rows - 1)
            c = random.randint(0, no_cols - 1)
            #wall or exit?
            if grid[r][c] == 0.0:
                break
        while(True):
            if random.random() < epsilon:
                action = random.choice(actions)
            else: 
                action = find_best_action(r, c, Qtable)
            nextrow, nextcol = next_state(r, c, action) #apply your action
            reward = livingReward
            terminal_or_not = False
            if grid[nextrow][nextcol] != 0.0: #then it means this is an exit
                reward = grid[nextrow][nextcol]
                terminal_or_not = True
            #update Q value with the formula:
            old_Qvalue = Qtable[(r, c, action)] 
            maximum_Qvalue_later = 0.0
            if not terminal_or_not:
                best_next = -float('inf')
                for i in actions:
                    value = Qtable[(nextrow, nextcol, i)]
                    if value > best_next:
                        best_next = value
                maximum_Qvalue_later = best_next
            #the update:
            new_Qvalue = old_Qvalue + alpha * (reward + (discount * maximum_Qvalue_later) - old_Qvalue)
            Qtable[(r, c, action)] = new_Qvalue
            #change:
            r, c = nextrow, nextcol
            #if terminal then this episode ends:
            if terminal_or_not:
                break
        if epsilon > minimum_epsilon: #after each episode, it explores less and decays less
            epsilon *= decay_rate
        if alpha > minimum_alpha:
            alpha *= decay_rate
    #checking the result here - comparing with optimal found previously:
    optimal_or_not = True
    learned = [['' for _ in range(no_cols)] for _ in range(no_rows)]
    for r in range(no_rows):
        for c in range(no_cols):
            #wall or exit?
            if grid[r][c] == '#':
                learned[r][c] = '#'
                continue
            if isinstance(grid[r][c], float) and grid[r][c] != 0.0:
                learned[r][c] = 'x'
                continue
            #the best move learned:
            best_action = find_best_action(r, c, Qtable)
            learned[r][c] = best_action
            reference = optimal_policy_grid[r][c] #comparing with the optimal found before
            #for position (2, 3) both W and S work so I am adding that later --> This is a later additon
            if r == 2 and c == 3:
                if best_action not in ['S', 'W']:
                    optimal_or_not = False
            else:
                if best_action != reference:
                    optimal_or_not = False
    return optimal_or_not, learned

#main run logic:
if __name__ == "__main__":
    trials = 10
    successes = 0
    print(f"Running Q learning algorithm for {trials} times.")
    print("-" * 50)
    for i in range(trials):
        success, policy = Qlearning()
        if success:
            print(f"Trial {i + 1} is successful, optimal policy found")
            successes += 1
        else:
            print(f"Trial {i + 1} fails, couldn't find the optimal policy, found another one")
    print("-" * 50)
    print(f"Result is: Out of {trials} trials {successes} of them were successful at finding the optimal policy.")





