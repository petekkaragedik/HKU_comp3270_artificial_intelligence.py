import sys, grader, parse
from collections import deque

def dfs_search(problem):
    start = problem["start"]
    goals = set(problem["goals"])
    adj = problem["adj"]
    frontier = deque([(start, [start])])  #the tuple is current node and path to current node
    explored = [] #tracking the order nodes are visited
    visited = set() #tracking which nodes visited

    while frontier:
        node, path = frontier.pop()
        if node not in visited:
            visited.add(node)

            if node in goals:
                #if at the goal node already return now
                return " ".join(explored) + "\n" + " ".join(path)

            explored.append(node) #if not a goal!! this way exploration ends before the goal

            #push children in the same order as the given file
            if node in adj:
                for (nbr, _) in adj[node]:
                    if nbr not in visited:
                        frontier.append((nbr, path + [nbr]))

    return " ".join(explored) + "\n"  #couldnt find a path return order


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, dfs_search, parse.read_graph_search_problem)