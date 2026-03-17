def read_grid_mdp_problem_p1(file_path):
    problem = {} #this will hold the info i get from the file
    with open(file_path, 'r') as f:
        lines = f.readlines()
    #i will add a bool for when i am reading the actual grid in the file
    is_reading_grid = False
    is_reading_policy = False
    #creating lists that will hold lists (for the grid and policy)
    grid_data = []
    policy_data = []
    for line in lines:
        line = line.strip()
        if not line:
            continue #skip empty line
        if line.startswith('seed: '):
            problem['seed'] = int(line.split(':')[1].strip())
        elif line.startswith('noise: '):
            problem['noise'] = float(line.split(':')[1].strip())
        elif line.startswith('livingReward: '):
            problem['livingReward'] = float(line.split(':')[1].strip())
        elif line.startswith('grid:'):
            is_reading_grid = True
            is_reading_policy = False
            continue
        elif line.startswith('policy:'):
            is_reading_grid = False
            is_reading_policy = True
            continue
        elif is_reading_grid:
            row = line.split() #trying to get cells 1 by 1
            grid_data.append(row)
        elif is_reading_policy:
            row = line.split()
            policy_data.append(row)
    problem['grid'] = grid_data
    problem['policy'] = policy_data #added them into dict.
    return problem

def read_grid_mdp_problem_p2(file_path): #did this in a similar manner as the 1st one actually:
    problem = {}
    with open(file_path, 'r') as f:
        lines = f.readlines()
    grid_data = []
    policy_data = []
    is_reading_grid = False
    is_reading_policy = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('discount:'):
            problem['discount'] = float(line.split(':')[1])
        elif line.startswith('noise:'):
            problem['noise'] = float(line.split(':')[1]) 
        elif line.startswith('livingReward:'):
            problem['livingReward'] = float(line.split(':')[1]) 
        elif line.startswith('iterations:'):
            problem['iterations'] = int(line.split(':')[1]) 
        elif line.startswith('grid:'):
            is_reading_grid = True
            is_reading_policy = False
            continue
        elif line.startswith('policy:'):
            is_reading_grid = False
            is_reading_policy = True
            continue
        if is_reading_grid: #reading the lines of the grid here:
            rowdata = []
            for item in line.split():
                try:
                    rowdata.append(float(item))
                except ValueError:
                    rowdata.append(item)
            grid_data.append(rowdata)
        elif is_reading_policy: #reading the lines of the policy here:
            policy_data.append(line.split())
    problem['grid'] = grid_data
    problem['policy'] = policy_data
    return problem

def read_grid_mdp_problem_p3(file_path): #again, implemented it in a similar manner as the others
    problem = {}
    with open(file_path, "r") as f: 
        lines = f.readlines()
    grid_data = []
    is_reading_grid = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('discount:'):
            problem['discount'] = float(line.split(':')[1])
        elif line.startswith('noise:'):
            problem['noise'] = float(line.split(':')[1])
        elif line.startswith('livingReward:'):
            problem['livingReward'] = float(line.split(':')[1])
        elif line.startswith('iterations:'):
            problem['iterations'] = int(line.split(':')[1])
        elif line.startswith('grid:'):
            is_reading_grid = True
            continue
        if is_reading_grid:
            rowdata = []
            for item in line.split():
                try:
                    rowdata.append(float(item))
                except ValueError:
                    rowdata.append(item)
            grid_data.append(rowdata)
    problem['grid'] = grid_data
    return problem