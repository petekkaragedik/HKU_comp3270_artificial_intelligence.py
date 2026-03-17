import sys, parse
import time, os, copy
import random #for the ghost's moves
#got this helper func from p1.py
def get_valid_moves(layout, position):
    #i implemented this helper function which returns valid moves for next move row and col
    #i assumed a move is valid if it is not a wall
    row, col = position
    moves = []
    #now i will check East West North South one by one
    if layout[row][col + 1] != '%':
        moves.append(('E', (row, col + 1)))
    if layout[row - 1][col] != '%':
        moves.append(('N', (row - 1, col)))
    if layout[row + 1][col] != '%':
        moves.append(('S', (row + 1, col)))
    if layout[row][col - 1] != '%':
        moves.append(('W', (row, col - 1)))
    #this gives us all valid ones, we will randomize in func. below
    return moves
#got this helper func from p1.py
def layout_to_string(layout): #to print the layout in expected way
    return "\n".join("".join(row) for row in layout)

#new helper func: calculates the manhattan distance, the distance btw two points
#this is the way to  calculate the distance requested according to my search on web
def get_manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def better_play_single_ghosts(problem):

    #initializations:
    layout = copy.deepcopy(problem['layout'])
    food_locations = set(problem['food'])
    pacman_pos = problem['pacman_start_loc']
    ghost_pos = problem['ghost_start_locs']['W'] #p2 has a single ghost
    score = 0
    solution = ''
    winner = 'Ghost' #assuming ghost wins if pacman couldnt finish
    solution += f"seed: {problem['seed']}\n" #will be -1 for p2
    solution += "0\n"
    solution += layout_to_string(layout) + "\n"
    #the game loop starts here:
    #i limited the # of turns so that it doesnt run forever
    for turn in range(1,1001):
        #pacmans turn:
        if turn % 2 == 1:
            valid_moves = get_valid_moves(layout, pacman_pos)
            if not valid_moves:
                break
            #my evaluation function logic: the best move is when:
            # 1. is not on a ghost
            # 2. is not next to a ghost
            # 3. is close to food
            # 4. far from ghost
            # 5. eats food now (is a bonus) --> these are from highest to lowest priority
            best_score = -float('inf')
            best_move = None
            for direction, new_pos in valid_moves:
                dist_to_ghost = get_manhattan_distance(new_pos, ghost_pos)
                #now we have a couple of checks:
                #1. does pacman die immadiately?
                if dist_to_ghost == 0:
                    move_score = -1000000  #this move_score is temporary, just for making decision, shows priorities
                #2. is there only 1 step left for death?
                elif dist_to_ghost == 1:
                    move_score = -5000
                #3.if move is safe, evaluate:
                else:
                    if not food_locations:
                        min_food_dist = 0 #no food left, win!
                    else:
                        food_dists = [get_manhattan_distance(new_pos, food) for food in food_locations]
                        min_food_dist = min(food_dists)
                    #my evaluation strategy:
                    #wanna minimize min_food_dist, maximize dist_to_ghost
                    #i will add different weights for food and ghost to prioritize food a little more
                    move_score = (-1.5 * min_food_dist) + (1.0 * dist_to_ghost)
                    #i will consider eating food as a big bonus
                    if new_pos in food_locations:
                        move_score += 100
                #now need to check if this is the best one found so far:
                if move_score > best_score:
                    best_score = move_score
                    best_move = (direction, new_pos)
            #if all moves go to ghost i.e. no good moves at all:
            if best_move is None:
                best_move = valid_moves[0] #just picking the first valid move
            chosen_direction, new_pos = best_move
            #--------------- my evaluation logic ends here
            layout[pacman_pos[0]][pacman_pos[1]] = ' ' #updating layout and position
            pacman_pos = new_pos
            score += -1 
            solution += f"{turn}: P moving {chosen_direction}\n"
            #did you bump into a ghost?
            if pacman_pos == ghost_pos:
                score += -500
                layout[pacman_pos[0]][pacman_pos[1]] = 'W'
                solution += layout_to_string(layout) + "\n"
                solution += f"score: {score}\n"
                solution += "WIN: Ghost\n"
                winner = 'Ghost'
                break
            #did you eat food?
            if pacman_pos in food_locations:
                score += 10
                food_locations.remove(pacman_pos)
            #pacman's new pos.
            layout[pacman_pos[0]][pacman_pos[1]] = 'P'
            solution += layout_to_string(layout) + "\n"
            #win?
            if not food_locations:
                score += 500
                solution += f"score: {score}\n"
                solution += "WIN: Pacman\n"
                winner = 'Pacman'
                break
            solution += f"score: {score}\n"
        #ghosts turn:
        else:
            #this logic is actually same with my p1.py
            valid_moves = get_valid_moves(layout, ghost_pos)
            if not valid_moves:
                continue #the ghost is trapped, skips this turn
            direction_names = [move[0] for move in valid_moves]
            direction_names.sort()
            chosen_direction = random.choice(direction_names)
            new_pos = None
            for direction, pos in valid_moves:
                if direction == chosen_direction:
                    new_pos = pos
                    break
            #clear ghosts old pos. replace with food if he was on one
            if ghost_pos in food_locations:
                layout[ghost_pos[0]][ghost_pos[1]] = '.'
            else:
                layout[ghost_pos[0]][ghost_pos[1]] = ' '
            ghost_pos = new_pos #move the ghost
            solution += f"{turn}: W moving {chosen_direction}\n"
            #did pacman and ghost bump into each other?
            if ghost_pos == pacman_pos:
                score += -500
                layout[ghost_pos[0]][ghost_pos[1]] = 'W'
                solution += layout_to_string(layout) + "\n"
                solution += f"score: {score}\n"
                solution += "WIN: Ghost\n"
                winner = 'Ghost'
                break
            layout[ghost_pos[0]][ghost_pos[1]] = 'W' #draw the ghost in new pos.
            solution += layout_to_string(layout) + "\n"
            solution += f"score: {score}\n" #print the scoe if game continues
    return solution.strip(), winner

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 2
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    num_trials = int(sys.argv[2])
    verbose = bool(int(sys.argv[3]))
    print('test_case_id:',test_case_id)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = better_play_single_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)