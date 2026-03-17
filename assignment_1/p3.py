import sys, parse, grader
import heapq

def ucs_search(problem):
    start = problem["start"]
    goals = set(problem["goals"])
    adj = problem["adj"]
    frontier = []
    heapq.heappush(frontier, (0, start, [start])) #cost - node - path
    explored = []
    visited = {}

    while frontier:
        cost, path_str, path = heapq.heappop(frontier)
        node = path[-1]  #the last node in the path/current one

        if node in visited and visited[node] <= cost: #skipping if already visited for cheaper
            continue
        visited[node] = cost #best cost for this node

        if node in goals:
            return " ".join(explored) + "\n" + " ".join(path)

        explored.append(node) 
        #add all neighbors to frontier with the new cost and path
        if node in adj:
            for (nbr, edge_cost) in adj[node]:
                new_cost = cost + edge_cost
                heapq.heappush(frontier, (new_cost, path_str + " " + nbr, path + [nbr]))

    return " ".join(explored) + "\n"

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, ucs_search, parse.read_graph_search_problem)