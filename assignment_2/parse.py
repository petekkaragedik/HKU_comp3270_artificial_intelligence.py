import os, sys
def read_layout_problem(file_path):
    
    #initializations:
    problem = {} #i chose dictionary data type
    layout = [] #the 2d list for the map
    food_locations = [] #,'ll store locarions of food
    pacman_start_loc = None #i'll store pacman's starting location here
    ghost_start_locs = {} #i'll store ghosts' starting locations here

    #to open and read the file:
    with open(file_path) as f:
        all_lines = f.readlines() #stored all of the lines
    
    #now extracting the first line, for the seed:
    line_of_seed = all_lines[0]
    seed_value_as_string = line_of_seed.strip().split(': ')[1]
    problem['seed'] = int(seed_value_as_string)

    #now the rest of the file:
    for row_no, line in enumerate(all_lines[1:]):
        line = line.strip()
        rows_list = []
        for col_no, character in enumerate(line):
            if character == 'P':
                pacman_start_loc = (row_no, col_no)
            elif character in ('W', 'X', 'Y', 'Z'):
                ghost_start_locs[character] = (row_no, col_no)
            elif character == '.':
                food_locations.append((row_no, col_no))
            rows_list.append(character)
        layout.append(rows_list)
    
    #putting all data we got in problem dict.
    problem['layout'] = layout
    problem['pacman_start_loc'] = pacman_start_loc
    problem['ghost_start_locs'] = ghost_start_locs
    problem['food'] = food_locations
    problem['score'] = 0
    return problem

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        problem = read_layout_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')