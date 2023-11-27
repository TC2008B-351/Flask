"""
Script to generate a dictionary of positions
"""
from map import Buildings, Semaphores
grid_size = 24

coordinates_dict = {}

for row in range(grid_size):
    for col in range(grid_size):
        current_coordinates = (col, row)
        possible_actions = {}

        # Outer Streets
        if col == 0:
            possible_actions = {'down': 1, 'right': 1}
        elif col == 1:
            possible_actions = {'down': 1, 'left': 1}
        elif row == 0:
            possible_actions = {'right': 1, 'up': 1}
        elif row == 1:
            possible_actions = {'right': 1, 'down': 1}
        elif col == 22:
            possible_actions = {'up': 1, 'right': 1}
        elif col == 23:
            possible_actions = {'up': 1, 'left': 1}
        elif row == 22:
            possible_actions = {'left': 1, 'up': 1}
        elif row == 23:
            possible_actions = {'left': 1, 'down': 1}
        # Cross Streets
        elif row == 8:
            possible_actions = {'right': 1, 'up': 1}
        elif row == 9:
            possible_actions = {'right': 1, 'down': 1}
        elif row == 10:
            possible_actions = {'left': 1, 'up': 1}
        elif row == 11:
            possible_actions = {'left': 1, 'down': 1}
        elif col == 12:
            possible_actions = {'down': 1, 'right': 1}
        elif col == 13:
            possible_actions = {'down': 1, 'left': 1}
        elif col == 14:
            possible_actions = {'up': 1, 'right': 1}
        elif col == 15:
            possible_actions = {'up': 1, 'left': 1}
        else:
            # If no specific constraint, allow movement in all directions
            possible_actions = {'up': 1, 'down': 1, 'left': 1, 'right': 1}

        # Check if the current coordinates are not in the Buildings or Semaphores lists
        if current_coordinates not in [building[0] for building in Buildings] and current_coordinates not in [semaphore[0] for semaphore in Semaphores]:
            coordinates_dict[current_coordinates] = possible_actions

print("{")
for coordinates, actions in coordinates_dict.items():
    print(f"    {coordinates}: {actions},")
print("}")
