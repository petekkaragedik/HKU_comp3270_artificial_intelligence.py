import sys, random, grader, parse
import copy

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

def layout_to_string(layout): #to print the layout in expected way
    return "\n".join("".join(row) for row in layout)

def random_play_single_ghost(problem):
    random.seed(problem['seed'], version=1)
    layout = copy.deepcopy(problem['layout']) #get initial state
    food_locations = set(problem['food'])
    #why copy? --> bcs. don't wanna modify originals
    pacman_pos = problem['pacman_start_loc']
    #we have 1 ghost only for problem 1!
    ghost_pos = problem['ghost_start_locs']['W']
    score = 0
    solution = f"seed: {problem['seed']}\n"
    solution += "0\n" #first turn is turn 0: initial state
    solution += layout_to_string(layout) + "\n"
    #the game loop
    #i will limit the # of turns to 1000 so that it doesnt last forever
    for turn in range(1, 1001):
        if turn % 2 == 1:
            #now it's pacmans turn:
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
            pacman_pos = new_pos #move pacman
            score -= 1
            #checking pacmans move in terms of a couple things:
            #1.did ghost catch pacman on pacmans move?
            if pacman_pos == ghost_pos:
                score -= 500
                solution += f"{turn}: P moving {chosen_direction}\n"
                solution += layout_to_string(layout) + "\n"
                solution += f"score: {score}\n"
                solution += "WIN: Ghost\n"
                break
            #2.did pacman eat food?
            if pacman_pos in food_locations:
                score += 10
                food_locations.remove(pacman_pos)
            layout[pacman_pos[0]][pacman_pos[1]] = 'P'
            solution += f"{turn}: P moving {chosen_direction}\n"
            solution += layout_to_string(layout) + "\n"
            #3.does pacman win? did pacman eat all food?
            if not food_locations:
                score += 500
                solution += f"score: {score}\n"
                solution += "WIN: Pacman\n"
                break
            solution += f"score: {score}\n"
        #----------
        else:
            #now it's ghosts turn
            valid_moves = get_valid_moves(layout, ghost_pos)
            if not valid_moves:
                turn += 1
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
                layout[ghost_pos[0]][ghost_pos[1]] = ' ' #clear old pos.
            ghost_pos = new_pos #move ghost
            layout[ghost_pos[0]][ghost_pos[1]] = 'W'
            solution += f"{turn}: W moving {chosen_direction}\n"
            solution += layout_to_string(layout) + "\n"
            #check if the ghost caught pacman?
            if ghost_pos == pacman_pos:
                score -= 500
                solution += f"score: {score}\n"
                solution += "WIN: Ghost\n"
                break
            solution += f"score: {score}\n" #print score if game continues
        
        turn += 1
    return solution.strip()

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, random_play_single_ghost, parse.read_layout_problem)