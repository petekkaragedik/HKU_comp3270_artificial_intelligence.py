import sys, parse, grader
import heapq

def greedy_search(problem):
    start = problem["start"]
    goals = set(problem["goals"])
    adj = problem["adj"]
    heuristics = problem["heuristics"]

    frontier = []
    heapq.heappush(frontier, (heuristics[start], start, [start])) #heuristic val - string path - list path
    explored = []
    visited = set()
    #this time we just use heuristic value to do nearly the same thing
    while frontier:
        heuristic_value, path_str, path = heapq.heappop(frontier)
        node = path[-1]

        if node in visited:
            continue
        visited.add(node)

        if node in goals:
            return " ".join(explored) + "\n" + " ".join(path)

        explored.append(node)
        if node in adj:
            for (nbr, _) in adj[node]:
                heapq.heappush(frontier, (heuristics[nbr], path_str + " " + nbr, path + [nbr]))

    return " ".join(explored) + "\n"

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 4
    grader.grade(problem_id, test_case_id, greedy_search, parse.read_graph_search_problem)