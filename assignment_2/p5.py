import sys, parse
import time, os, copy
import math
#helper func.s - altered/taken from my previous implementations
def get_manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def get_valid_moves(layout, position, blocked_positions=set()):
    row, col = position
    moves = []
    directions = [('E', (row, col + 1)), ('N', (row - 1, col)), ('S', (row + 1, col)), ('W', (row, col - 1))]
    for direction, new_pos in directions:
        r, c = new_pos
        if layout[r][c] != '%' and new_pos not in blocked_positions:
            moves.append((direction, new_pos))
    return moves

def layout_to_string(layout):
    return "\n".join("".join(row) for row in layout)

class MinimaxState:
    #class to keep and amanage game state 
    def __init__(self, problem, score = 0, pacman_pos = None, ghost_positions = None, food_locations = None, layout = None):
        #varibles for the current node:
        self.layout = layout if layout is not None else copy.deepcopy(problem['layout'])
        self.pacman_pos = pacman_pos if pacman_pos is not None else problem['pacman_start_loc']
        self.ghost_positions = ghost_positions if ghost_positions is not None else copy.deepcopy(problem['ghost_start_locs'])
        self.food_locations = food_locations if food_locations is not None else set(problem['food'])
        self.score = score
        #some things to fix in game:
        self.ghost_chars_in_order = sorted(self.ghost_positions.keys())
        self.num_ghosts = len(self.ghost_chars_in_order)
        self.num_players = 1 + self.num_ghosts
        
    def check_terminal(self):
        #returns score, winner tuple when game over
        if not self.food_locations:
            return self.score + 500, 'Pacman'
        if self.pacman_pos in self.ghost_positions.values():
            return self.score + -500, 'Ghost'
        return None, None #game still continues

def evaluate_state(state):
    #eval. function used at depth k, pacmans safety and food comes first, similar to p4
    score, winner = state.check_terminal()
    if winner is not None:
        return score
    current_score = state.score
    #max. dist. to nearest ghost
    all_ghost_dists = [get_manhattan_distance(state.pacman_pos, g_pos) for g_pos in state.ghost_positions.values()]
    dist_to_ghost = min(all_ghost_dists) if all_ghost_dists else float('inf')
    
    if dist_to_ghost <= 1:
        #this is a very bad state, but it must be a bit better
        #than an actual loss, if not Pacman will prefer dying
        ghost_term = -500 * 0.9
    else:
        ghost_term = 1.0 * dist_to_ghost
        
    if not state.food_locations:
        min_food_dist = 0
    else: 
        food_dists = [get_manhattan_distance(state.pacman_pos, food) for food in state.food_locations]
        min_food_dist = min(food_dists)
    food_term = -1.5 * min_food_dist
    heuristic_value = current_score + food_term + ghost_term
    return heuristic_value

#some helper func.s to change state
def apply_pacman_move(current_state, new_pos, direction):
    new_state = copy.deepcopy(current_state)
    new_state.layout[new_state.pacman_pos[0]][new_state.pacman_pos[1]] = ' ' #clear
    new_state.pacman_pos = new_pos
    new_state.score += -1 #pacman moves
    #food?
    if new_state.pacman_pos in new_state.food_locations:
        new_state.score += 10
        new_state.food_locations.remove(new_state.pacman_pos)
    if new_state.pacman_pos not in new_state.ghost_positions.values():
        new_state.layout[new_state.pacman_pos[0]][new_state.pacman_pos[1]] = 'P'
    return new_state

def apply_ghost_move(current_state, ghost_char, new_pos, direction):
    new_state = copy.deepcopy(current_state)
    ghost_pos = new_state.ghost_positions[ghost_char]
    if ghost_pos in new_state.food_locations:
        new_state.layout[ghost_pos[0]][ghost_pos[1]] = '.' #ghost was on food
    else:
        new_state.layout[ghost_pos[0]][ghost_pos[1]] = ' ' #was on empty square
    new_state.ghost_positions[ghost_char] = new_pos
    if new_pos != new_state.pacman_pos:
        new_state.layout[new_pos[0]][new_pos[1]] = ghost_char
    return new_state

#minimax search:
def minimax_value(state, agent_index, k_remaining):
    #recursive minimax func.
    #0 = Pacman max, 1= Ghosts min, k_remaining # of Pacman moves left
    score, winner = state.check_terminal()
    if winner is not None:
        return score #first check if game over
    #stop before Pacmans move when k_remaining hits 0  k is ply depth
    if k_remaining == 0:
        return evaluate_state(state)
    is_pacman = (agent_index == 0)
    next_agent_index = -1
    if is_pacman:
        current_pos = state.pacman_pos
        next_agent_index = 1
        current_player_char = 'P'
    else:
        ghost_char = state.ghost_chars_in_order[agent_index - 1]
        current_pos = state.ghost_positions[ghost_char]
        current_player_char = ghost_char
        if agent_index == state.num_ghosts: #last ghost move, next pacman
            next_agent_index = 0
        else: #next is other ghost
            next_agent_index = agent_index + 1
            
    #get valid moves:
    blocked_positions = set()
    if not is_pacman: #ghost cannot go to other ghost loc.
        all_ghosts_pos_set = set(state.ghost_positions.values())
        blocked_positions = all_ghosts_pos_set - {current_pos}
    valid_moves = get_valid_moves(state.layout, current_pos, blocked_positions)
    #stuck
    if not valid_moves:
        if is_pacman:
            return -500 #probably pacman dies
        else:
            #ghost stuck, move on (but still count as a ply)
            return minimax_value(state, next_agent_index, k_remaining - 1)       
    #the actual minimax logic:
    best_value = -math.inf if is_pacman else math.inf
    for direction, new_pos in valid_moves:
        if is_pacman: 
            new_state = apply_pacman_move(state, new_pos, direction)
        else: 
            new_state = apply_ghost_move(state, current_player_char, new_pos, direction)
        #the recursive call, find val. of resulting state
        value = minimax_value(new_state, next_agent_index, k_remaining - 1) 
        if is_pacman:
            best_value = max(best_value, value)
        else:
            best_value = min(best_value, value)
    return best_value

def get_best_move(state, agent_index, k):
    #find best move for Ghost or Pacman using minimax:
    is_pacman = (agent_index == 0)
    current_pos = state.pacman_pos
    current_player_char = 'P'
    blocked_positions = set()
    if not is_pacman:
        current_player_char = state.ghost_chars_in_order[agent_index - 1]
        current_pos = state.ghost_positions[current_player_char]
        all_ghosts_pos_set = set(state.ghost_positions.values())
        blocked_positions = all_ghosts_pos_set - {current_pos}
        
    valid_moves = get_valid_moves(state.layout, current_pos, blocked_positions)
    if not valid_moves:
        return None, None #stuck
    #for the children:
    next_agent_index = 0
    if is_pacman:
        next_agent_index = 1
    elif agent_index < state.num_ghosts:
        next_agent_index = agent_index + 1 #if its last ghost next_agent_index is alreadly 0 anyways
    #move with the best value?
    best_value = -math.inf if is_pacman else math.inf
    best_moves = []
    
    for direction, new_pos in valid_moves:
        if is_pacman:
            next_state = apply_pacman_move(state, new_pos, direction)
        else:
            next_state = apply_ghost_move(state, current_player_char, new_pos, direction)
        #minimax search starts in next players turn:
        value = minimax_value(next_state, next_agent_index, k - 1)
        if is_pacman:
            if value > best_value:
                best_value = value
                best_moves = [(direction, new_pos)]
            elif value == best_value:
                best_moves.append((direction, new_pos))
        else:
            if value < best_value:
                best_value = value
                best_moves = [(direction, new_pos)]
            elif value == best_value:
                best_moves.append((direction, new_pos))
    #sort by direction name:
    best_moves.sort(key=lambda x: x[0])
    chosen_direction, chosen_pos = best_moves[0]
    return chosen_direction, chosen_pos

def min_max_multiple_ghosts(problem, k):
    #everyone chooses their moves by minimax:
    #initializations:
    state = MinimaxState(problem)
    solution = f"seed: {problem['seed']}\n"
    solution += "0\n"
    solution += layout_to_string(state.layout) + "\n"
    winner = 'Ghost'
    
    #game loop:
    for turn in range(1, 1001):
        player_index = (turn - 1) % state.num_players
        #minimax selct move:
        chosen_direction, new_pos = get_best_move(state, player_index, k)
        if player_index == 0: #pacmans turn:
            if chosen_direction is None:
                break #pacman stuck
            state.layout[state.pacman_pos[0]][state.pacman_pos[1]] = ' '
            state.pacman_pos = new_pos
            state.score += -1
            solution += f"{turn}: P moving {chosen_direction}\n"
            #check if bump into ghost:
            if state.pacman_pos in state.ghost_positions.values():
                state.score += -500
                for char, pos in state.ghost_positions.items():
                    if pos == state.pacman_pos:
                        state.layout[state.pacman_pos[0]][state.pacman_pos[1]] = char
                        break
                solution += layout_to_string(state.layout) + "\n"
                solution += f"score: {state.score}\n"
                solution += "WIN: Ghost\n"
                winner = 'Ghost'
                break
            #check if ate food?
            if state.pacman_pos in state.food_locations:
                state.score += 10
                state.food_locations.remove(state.pacman_pos)
            state.layout[state.pacman_pos[0]][state.pacman_pos[1]] = 'P'
            solution += layout_to_string(state.layout) + "\n"
            #check if pacman wins?
            if not state.food_locations:
                state.score += 500
                solution += f"score: {state.score}\n"
                solution += "WIN: Pacman\n"
                winner = 'Pacman'
                break
            solution += f"score: {state.score}\n"
        else: #ghosts turn:(W, X, Y, Z order)
            ghost_char = state.ghost_chars_in_order[player_index - 1]
            ghost_pos_old = state.ghost_positions[ghost_char]
            if chosen_direction is None: #ghost stuck
                solution += f"{turn}: {ghost_char} moving \n"
                solution += layout_to_string(state.layout) + "\n"
                solution += f"score: {state.score}\n"
                continue
            if ghost_pos_old in state.food_locations: #clear old pos
                state.layout[ghost_pos_old[0]][ghost_pos_old[1]] = '.'
            else:
                state.layout[ghost_pos_old[0]][ghost_pos_old[1]] = ' '
            state.ghost_positions[ghost_char] = new_pos
            solution += f"{turn}: {ghost_char} moving {chosen_direction}\n"
            #did it bump into pacman?
            if new_pos == state.pacman_pos:
                state.score += -500
                state.layout[new_pos[0]][new_pos[1]] = ghost_char
                solution += layout_to_string(state.layout) + "\n"
                solution += f"score: {state.score}\n"
                solution += "WIN: Ghost\n"
                winner = 'Ghost'
                break
            state.layout[new_pos[0]][new_pos[1]] = ghost_char
            solution += layout_to_string(state.layout) + "\n"
            solution += f"score: {state.score}\n"
            
    return solution.strip(), winner

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 5
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    k = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    verbose = bool(int(sys.argv[4]))
    print('test_case_id:',test_case_id)
    print('k:',k)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = min_max_multiple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)