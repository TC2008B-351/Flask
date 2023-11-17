import networkx as nx
import heapq
from map import grid_size, grafo_info

""" Get a list of intermediate steps between two points on the grid """
def get_intermediate_steps(origin, goal):
    # Calculate differences in x and y coordinates
    diff_x = goal[0] - origin[0]
    diff_y = goal[1] - origin[1]

    # Determine the number of steps needed for each axis
    num_steps_x = abs(diff_x)
    num_steps_y = abs(diff_y)

    # Calculate the increment values for each step on x and y axes
    increment_x = diff_x // num_steps_x if num_steps_x else 0
    increment_y = diff_y // num_steps_y if num_steps_y else 0

    # Generate the intermediate steps
    intermediate_steps = []
    current_step = origin
    for _ in range(max(num_steps_x, num_steps_y)):
        x = current_step[0] + increment_x
        y = current_step[1] + increment_y
        current_step = (x, y)
        intermediate_steps.append(current_step)

    return intermediate_steps

""" Define Manhattan distance heuristic """
def manhattan_distance(node1, node2):
    return abs(node2[0] - node1[0]) + abs(node2[1] - node1[1])

""" Create the problem directed graph """
def create_graph(grafo_info):
    graph = nx.DiGraph()
    for node, connections in grafo_info.items():
                for neighbor, cost in connections.items():
                    graph.add_edge(node, neighbor, weight=cost)
    return graph
"""
# Add nodes
nodes = [(x, y) for x in range(grid_size) for y in range(grid_size)]
G.add_nodes_from(nodes)

# Add edges with weights
G.add_edges_from(edges)
"""

""" A* algorithm implementation using Manhattan distance as a heuristic """
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

    # Get intermediate steps
    full_path = []
    for i in range(len(path) - 1):
        full_path.extend(get_intermediate_steps(path[i], path[i + 1]))

    return full_path

""" Display path on grid function with 0,0 at bottom left on the terminal """
def display_path_on_grid(path, grid_size):
    grid = [['.' for _ in range(grid_size[1])] for _ in range(grid_size[0])]
    
    for node in path:
        # Adjusting coordinates for display
        adjusted_x = grid_size[0] - 1 - node[1]
        adjusted_y = node[0]
        grid[adjusted_x][adjusted_y] = '*'
    
    for row in grid:
        print(' '.join(row))

""" Test """
def test():
    print("Hello World")
    G = create_graph(grafo_info)
    # Find path using A* with Manhattan distance heuristic
    start_node = (1, 1)
    goal_node = (19, 19)
    path = astar(G, start_node, goal_node, manhattan_distance)

    print('Path from {} to {}:'.format(start_node, goal_node))
    print(path)

    # Display the path on the grid
    display_path_on_grid(path, (grid_size, grid_size))

test()