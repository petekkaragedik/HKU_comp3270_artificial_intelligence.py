import sys, grader, parse
from collections import deque

def bfs_search(problem):
    start = problem["start"]
    goals = set(problem["goals"])
    adj = problem["adj"]
    frontier = deque([(start, [start])])
    explored = []
    visited = set()

    while frontier:
        node, path = frontier.popleft() #only changed to popleft from my dfs implementation
        if node not in visited:
            visited.add(node)

            if node in goals:
                return " ".join(explored) + "\n" + " ".join(path)

            explored.append(node)

            if node in adj:
                for (nbr, _) in adj[node]:
                    if nbr not in visited:
                        frontier.append((nbr, path + [nbr]))

    return " ".join(explored) + "\n"

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 2
    grader.grade(problem_id, test_case_id, bfs_search, parse.read_graph_search_problem)