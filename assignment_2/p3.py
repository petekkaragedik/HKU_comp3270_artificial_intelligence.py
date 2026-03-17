import sys, grader, parse, math
import random, copy

#my helper func.s: modified from my p1.py
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

def random_play_multiple_ghosts(problem):

    #initialization(actually similar to p1.py):
    random.seed(problem['seed'], version=1)
    layout = copy.deepcopy(problem['layout'])
    food_locations = set(problem['food'])
    pacman_pos = problem['pacman_start_loc']
    score = 0
    #new ghost p3 logic:
    ghost_positions = copy.deepcopy(problem['ghost_start_locs'])
    #need sorted list of ghosts, this is move order
    ghost_chars_in_order = sorted(ghost_positions.keys())
    #no. of players:
    num_players = 1 + len(ghost_chars_in_order)

    solution = f"seed: {problem['seed']}\n"
    solution += "0\n"
    solution += layout_to_string(layout) + "\n"
    #the game loop:
    for turn in range(1, 1001):
        #0 -> pacmans turn, 1 -> first ghost...
        player_index = (turn - 1) % num_players
        #pacmans turn - logic almost same as p1:
        if player_index == 0:
            valid_moves = get_valid_moves(layout, pacman_pos)
            if not valid_moves:
                break
            direction_names = [move[0] for move in valid_moves]
            direction_names.sort() 
            chosen_direction = random.choice(direction_names)
            new_pos = None
            for direction, pos in valid_moves:
                if direction == chosen_direction:
                    new_pos = pos
                    break
            layout[pacman_pos[0]][pacman_pos[1]] = ' ' #clear old pos.
            pacman_pos = new_pos
            score += -1
            solution += f"{turn}: P moving {chosen_direction}\n"
            #did ghost die? bump into any ghost?
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
                break
            #did pacman eat any food?
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
                break
            solution += f"score: {score}\n"
        #a ghost's turn:
        else:
            #which ghost?
            ghost_char = ghost_chars_in_order[player_index - 1]
            ghost_pos = ghost_positions[ghost_char]
            #ghost cannot move on another ghost
            all_ghosts_pos_set = set(ghost_positions.values())
            other_ghost_pos_set = all_ghosts_pos_set - {ghost_pos}
            valid_moves = get_valid_moves(layout, ghost_pos, other_ghost_pos_set)
            if not valid_moves: #ghost stuck, does nothing
                solution += f"{turn}: {ghost_char} moving \n"
                solution += layout_to_string(layout) + "\n"
                solution += f"score: {score}\n"
                continue
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
            ghost_pos = new_pos #i'll use this to check if bump into each other
            solution += f"{turn}: {ghost_char} moving {chosen_direction}\n"
            #check if bump into each other:
            if ghost_pos == pacman_pos:
                score += -500
                layout[ghost_pos[0]][ghost_pos[1]] = ghost_char
                solution += layout_to_string(layout) + "\n"
                solution += f"score: {score}\n"
                solution += "WIN: Ghost\n"
                break
            layout[ghost_pos[0]][ghost_pos[1]] = ghost_char #add ghost to new pos.
            solution += layout_to_string(layout) + "\n"
            solution += f"score: {score}\n"
    return solution.strip()

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, random_play_multiple_ghosts, parse.read_layout_problem)