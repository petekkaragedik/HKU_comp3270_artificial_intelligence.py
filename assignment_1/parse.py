import os, sys
def read_graph_search_problem(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    start = lines[0].split(":")[1].strip() #have to split on ":" here
    goals = lines[1].split(":")[1].strip().split() #i can have multiple goals as well
    heuristics = {}
    adj = {}
    i = 2
    #parsing the heuristic values in this loop
    while i < len(lines) and len(lines[i].split()) == 2: #lines that have 2 elemnts bc. node+heuristic
        state, h = lines[i].split()
        heuristics[state] = float(h)
        adj[state] = []   #initializing empty adj list here for all the nodes
        i += 1

    #keeping track of the given order here
    while i < len(lines):
        s, t, c = lines[i].split()
        adj[s].append((t, float(c)))
        i += 1

    return {
        "start": start,
        "goals": goals,
        "heuristics": heuristics,
        "adj": adj
    }

#i assumed that the input is in the expected format as it was discussed on the forum
def read_8queens_search_problem(file_path):
    board = []
    queens = {}

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    for r, line in enumerate(lines):
        row = line.split()
        board.append(row)
        for c, val in enumerate(row):
            if val == "q":
                queens[c] = r

    return {
        "board": board,
        "queens": queens
    }

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        if int(problem_id) <= 5:
            problem = read_graph_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        else:
            problem = read_8queens_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')