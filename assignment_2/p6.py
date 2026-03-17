import sys, parse
import time, os, copy
import random

#i am using these for simplicity this time: 
directions = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
ghost_symbols = ['W', 'X', 'Y', 'Z']
#some helper functions needed:
def get_valid_actions(layout, pos, ghosts=None, agent_id=None):
    moves = []
    other_ghost_positions = set()
    if ghosts and agent_id:
        for gid, gpos in ghosts.items():
            if gid != agent_id:
                other_ghost_positions.add(gpos)
    for d, (dr, dc) in directions.items():
        r, c = pos[0] + dr, pos[1] + dc
        #walll?
        if layout[r][c] == '%':
            continue
        #another ghost?
        if agent_id and (r, c) in other_ghost_positions:
            continue
            
        moves.append(d)
    return moves

def move(pos, direction):
    dr, dc = directions[direction]
    return (pos[0] + dr, pos[1] + dc)

def get_manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def is_terminal(pacman, ghosts, foods):
    for g in ghosts.values(): #pacman dies? eaten?
        if g == pacman:
            return 'Ghost'
    if not foods:
        return 'Pacman'
    return None

def evaluate_state(pacman, ghosts, foods, score): #the heuristic evaluation of a state calculated
    if not foods:
        return score + 500
    min_food = min(get_manhattan_distance(pacman, f) for f in foods)
    min_ghost = min(get_manhattan_distance(pacman, g) for g in ghosts.values()) if ghosts else 999
    #want closer food further ghost
    return score - 2 * min_food + 4 * min_ghost

 #expectimax core func.
def expectimax(layout, pacman, ghosts, foods, score, depth, agent_index, k):
    winner = is_terminal(pacman, ghosts, foods)
    if winner == 'Pacman':
        return 500
    elif winner == 'Ghost':
        return -500
    if depth == 0:
        return evaluate_state(pacman, ghosts, foods, score)
    agents = ['P'] + [g for g in ghost_symbols if g in ghosts]
    agent = agents[agent_index]
    next_agent_index = (agent_index + 1) % len(agents)
    next_depth = depth - 1 if next_agent_index == 0 else depth
    if agent == 'P': #pacman
        best_val = float('-inf')
        for a in get_valid_actions(layout, pacman):
            np = move(pacman, a)
            eaten = np in foods
            new_score = score + -1 + (10 if eaten else 0)
            new_foods = foods - {np} if eaten else foods
            val = expectimax(layout, np, ghosts, new_foods, new_score, next_depth, next_agent_index, k)
            if val > best_val:
                best_val = val
        return best_val
    else:  #ghost
        gpos = ghosts[agent]
        acts = get_valid_actions(layout, gpos, ghosts, agent)
        if not acts:
            return expectimax(layout, pacman, ghosts, foods, score, next_depth, next_agent_index, k)
        prob = 1.0 / len(acts)
        exp_val = 0
        for a in acts:
            ng = move(gpos, a)
            ghosts[agent] = ng 
            val = expectimax(layout, pacman, ghosts, foods, score, next_depth, next_agent_index, k)
            exp_val += prob * val
            ghosts[agent] = gpos
        return exp_val

def expecti_max_multiple_ghosts(problem, k):
    layout = problem['layout']
    pacman = problem['pacman_start_loc']
    ghosts = dict(problem['ghost_start_locs'])  #didnt do deepcopy like prev. implementations bcs. took too long: shallow copy
    foods = set(problem['food'])
    score = 0
    solution = ''
    step = 0
    random.seed()  #random ghosts requested

    while True:
        winner = is_terminal(pacman, ghosts, foods)
        if winner:
            solution += f"WIN: {winner}\n"
            return solution, winner
        #pacman decide expectimax:
        best_val, best_act = float('-inf'), None
        legal = get_valid_actions(layout, pacman)
        for a in legal:
            np = move(pacman, a)
            eaten = np in foods
            new_score = score + -1 + (10 if eaten else 0)
            new_foods = foods - {np} if eaten else foods
            val = expectimax(layout, np, dict(ghosts), new_foods, new_score, k-1, 1, k)
            if val > best_val:
                best_val, best_act = val, a
        if not best_act:
            solution += "WIN: Ghost\n"
            return solution, 'Ghost'
        pacman = move(pacman, best_act)
        if pacman in foods:
            foods.remove(pacman)
            score += 10
        score += -1
        step += 1
        solution += f"{step}: P moving {best_act}\n"
        winner = is_terminal(pacman, ghosts, foods)
        if winner:
            solution += f"WIN: {winner}\n"
            return solution, winner
        #ghost move random:
        for g in [g for g in ghost_symbols if g in ghosts]:
            acts = get_valid_actions(layout, ghosts[g], ghosts, g)
            if not acts:
                continue
            choice = random.choice(acts) #random loigc like before
            ghosts[g] = move(ghosts[g], choice)
            step += 1
            solution += f"{step}: {g} moving {choice}\n"
            winner = is_terminal(pacman, ghosts, foods)
            if winner:
                solution += f"WIN: {winner}\n"
                return solution, winner

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 6
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
        solution, winner = expecti_max_multiple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)