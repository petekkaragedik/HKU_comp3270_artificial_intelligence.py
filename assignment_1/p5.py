import sys, parse, grader
import heapq

def astar_search(problem):
    start = problem["start"]
    goals = set(problem["goals"])
    adj = problem["adj"]
    heuristics = problem["heuristics"]

    #frontier: total - insertion order - backward cost - string path - list path
    frontier = []
    insertion_order = 0
    heapq.heappush(frontier, (heuristics[start], insertion_order, 0, start, [start]))
    insertion_order += 1

    explored = []
    visited = {}

    while frontier:
        total_value, _, backw_cost, path_string, path = heapq.heappop(frontier)
        node = path[-1]

        #skip if we alr. visited with less or equal backw cost
        if node in visited and visited[node] <= backw_cost:
            continue
        visited[node] = backw_cost

        # Found goal
        if node in goals:
            return " ".join(explored) + "\n" + " ".join(path)

        explored.append(node)

        if node in adj:
            for (nbr, edge_cost) in adj[node]:
                new_g = backw_cost + edge_cost
                new_f = new_g + heuristics[nbr]
                heapq.heappush(frontier,
                               (new_f, insertion_order, new_g, path_string + " " + nbr, path + [nbr]))
                insertion_order += 1 #keeping track of the order im inserting because otherwise the ordering didnt work

    return " ".join(explored) + "\n"

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 5
    grader.grade(problem_id, test_case_id, astar_search, parse.read_graph_search_problem)