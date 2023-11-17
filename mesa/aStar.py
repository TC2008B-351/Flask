import networkx as nx
import heapq
from map import grid_size, edges

# Define Manhattan distance heuristic
def manhattan_distance(node1, node2):
    return abs(node2[0] - node1[0]) + abs(node2[1] - node1[1])

# Create a directed graph
G = nx.DiGraph()

# Add nodes
nodes = [(x, y) for x in range(grid_size) for y in range(grid_size)]
G.add_nodes_from(nodes)

# Add edges with weights
G.add_edges_from(edges)

# A* algorithm implementation using Manhattan distance as a heuristic
def astar(graph, start, goal, heuristic):
    frontier = [(0, start)]
    heapq.heapify(frontier)
    came_from = {}
    cost_so_far = {start: 0}

    while frontier:
        current_cost, current_node = heapq.heappop(frontier)

        if current_node == goal:
            break

        for next_node in graph.neighbors(current_node):
            new_cost = cost_so_far[current_node] + graph[current_node][next_node]['weight']
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(goal, next_node)
                heapq.heappush(frontier, (priority, next_node))
                came_from[next_node] = current_node

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path

# Display path on grid function on 0,0 at bottom left
def display_path_on_grid(path, grid_size):
    grid = [['.' for _ in range(grid_size[1])] for _ in range(grid_size[0])]
    
    for node in path:
        # Adjusting coordinates for display
        adjusted_x = grid_size[0] - 1 - node[1]
        adjusted_y = node[0]
        grid[adjusted_x][adjusted_y] = '*'
    
    for row in grid:
        print(' '.join(row))

# Find path using A* with Manhattan distance heuristic
start_node = (0, 0)
goal_node = (3, 1)
path = astar(G, start_node, goal_node, manhattan_distance)

print('Path from {} to {}:'.format(start_node, goal_node))
print(path)

# Display the path on the grid
display_path_on_grid(path, (grid_size, grid_size))
