import sys, parse
import time, os, copy
import random
#got these helper func.s straight from p3.py
def get_valid_moves(layout, position, blocked_positions=set()):
    #list of valid direction, position... 
    #move valid if not a wall and not in blocked_positions(other ghosts)
    row, col = position
    moves = []
    #checking east north south west respectively
    new_pos_e = (row, col + 1)
    if layout[row][col + 1] != '%' and new_pos_e not in blocked_positions:
        moves.append(('E', new_pos_e))
    new_pos_n = (row - 1, col)
    if layout[row - 1][col] != '%' and new_pos_n not in blocked_positions:
        moves.append(('N', new_pos_n))
    new_pos_s = (row + 1, col)
    if layout[row + 1][col] != '%' and new_pos_s not in blocked_positions:
        moves.append(('S', new_pos_s))    
    new_pos_w = (row, col - 1)
    if layout[row][col - 1] != '%' and new_pos_w not in blocked_positions:
        moves.append(('W', new_pos_w))
    return moves

def layout_to_string(layout):
    return "\n".join("".join(row) for row in layout)
#and got this helper function straight from p2.py
def get_manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def better_play_multiple_ghosts(problem): #this one has elements from p2 and p3

    #initializations:
    layout = copy.deepcopy(problem['layout'])
    food_locations = set(problem['food'])
    pacman_pos = problem['pacman_start_loc']
    score = 0
    solution = ''
    winner = 'Ghost' #as default
    #same multiple ghosts logic from p3:
    ghost_positions = copy.deepcopy(problem['ghost_start_locs'])
    ghost_chars_in_order = sorted(ghost_positions.keys())
    num_players = 1 + len(ghost_chars_in_order)
    solution += f"seed: {problem['seed']}\n" #will be -1 for this problem
    solution += "0\n"
    solution += layout_to_string(layout) + "\n"
    #the game loop
    for turn in range(1, 1001): #similar logic from p3
        player_index = (turn - 1) % num_players
        #pacmans turn logic from p2:
        if player_index == 0:
            valid_moves = get_valid_moves(layout, pacman_pos)
            if not valid_moves:
                break
            best_score = -float('inf') #evaluation func from pş2
            best_move = None
            for direction, new_pos in valid_moves:
                #now this is the difference! calc. dist. to NEAREST ghost
                all_ghost_dists = [get_manhattan_distance(new_pos, g_pos) for g_pos in ghost_positions.values()]
                dist_to_ghost = min(all_ghost_dists) if all_ghost_dists else float('inf')
                #now similar logic from p2 continues:
                if dist_to_ghost == 0:
                    move_score = -1000000
                elif dist_to_ghost == 1:
                    move_score = -5000
                else:
                    if not food_locations:
                        min_food_dist = 0
                    else:
                        food_dists = [get_manhattan_distance(new_pos, food) for food in food_locations]
                        min_food_dist = min(food_dists)
                    move_score = (-1.5 * min_food_dist) + (1.0 * dist_to_ghost)
                    if new_pos in food_locations:
                        move_score += 100
                if move_score > best_score:
                    best_score = move_score
                    best_move = (direction, new_pos)
            if best_move is None: #all moves make you die
                best_move = valid_moves[0]
            chosen_direction, new_pos = best_move

            layout[pacman_pos[0]][pacman_pos[1]] = ' ' #clear old pos
            pacman_pos = new_pos
            score += -1
            solution += f"{turn}: P moving {chosen_direction}\n"
            #check if bump into any ghost? from p3:
            if pacman_pos in ghost_positions.values():
                score += -500
                #which ghost?
                for char, pos in ghost_positions.items():
                    if pos == pacman_pos:
                        layout[pacman_pos[0]][pacman_pos[1]] = char
                        break
                solution += layout_to_string(layout) + "\n"
                solution += f"score: {score}\n"
                solution += "WIN: Ghost\n"
                winner = 'Ghost'
                break
            #did pacman eat food?
            if pacman_pos in food_locations:
                score += 10
                food_locations.remove(pacman_pos)
            layout[pacman_pos[0]][pacman_pos[1]] = 'P'
            solution += layout_to_string(layout) + "\n"
            #did pacman win?
            if not food_locations:
                score += 500
                solution += f"score: {score}\n"
                solution += "WIN: Pacman\n"
                winner = 'Pacman'
                break
            solution += f"score: {score}\n"
        #ghosts turn:
        else:
            #which ghost?
            ghost_char = ghost_chars_in_order[player_index - 1]
            ghost_pos = ghost_positions[ghost_char]
            #ghost cannot move on another ghost
            all_ghosts_pos_set = set(ghost_positions.values())
            other_ghost_pos_set = all_ghosts_pos_set - {ghost_pos}
            valid_moves = get_valid_moves(layout, ghost_pos, other_ghost_pos_set) #just like in p3
            if not valid_moves: #ghost stuck, does nothing
                solution += f"{turn}: {ghost_char} moving \n"
                solution += layout_to_string(layout) + "\n"
                solution += f"score: {score}\n"
                continue
            #p4 ghosts move random like p2 and p3
            direction_names = [move[0] for move in valid_moves]
            direction_names.sort()
            chosen_direction = random.choice(direction_names)
            new_pos = None
            for direction, pos in valid_moves:
                if direction == chosen_direction:
                    new_pos = pos
                    break
            if ghost_pos in food_locations:
                layout[ghost_pos[0]][ghost_pos[1]] = '.'
            else:
                layout[ghost_pos[0]][ghost_pos[1]] = ' '
            ghost_positions[ghost_char] = new_pos #update ghost pos.
            ghost_pos = new_pos #use this for collision check
            solution += f"{turn}: {ghost_char} moving {chosen_direction}\n"
            #check if bump into pacman:
            if ghost_pos == pacman_pos:
                score += -500
                layout[ghost_pos[0]][ghost_pos[1]] = ghost_char
                solution += layout_to_string(layout) + "\n"
                solution += f"score: {score}\n"
                solution += "WIN: Ghost\n"
                winner = 'Ghost'
                break
            layout[ghost_pos[0]][ghost_pos[1]] = ghost_char #add ghost to new pos.
            solution += layout_to_string(layout) + "\n"
            solution += f"score: {score}\n"
    return solution.strip(), winner

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 4
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
        solution, winner = better_play_multiple_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)