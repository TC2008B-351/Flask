import math
from mesa import Agent


def calculate_rotation_angle(past_coords, current_coords, future_coords):
    # Calculate vectors
    vector1 = [current_coords[0] - past_coords[0], current_coords[1] - past_coords[1]]
    vector2 = [future_coords[0] - current_coords[0], future_coords[1] - current_coords[1]]

    # Calculate dot product
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]

    # Calculate magnitudes
    magnitude1 = math.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
    magnitude2 = math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)

    # Calculate angle in radians
    if magnitude1 == 0 or magnitude2 == 0:
        return 0  # Avoid division by zero
    else:
        cos_theta = dot_product / (magnitude1 * magnitude2)
        angle_rad = math.acos(cos_theta)

    # Convert angle to degrees
    angle_deg = math.degrees(angle_rad)
    return angle_deg

class CarAgent(Agent):
    def __init__(self, unique_id, model, pos, path):
        super().__init__(unique_id, model)
        self.pos = pos
        self.path = path
        self.rotationToPos = 0

    def move(self):
        old_coords = self.pos
        if not self.path:
            return
        target_coordinates = self.path[0]
        current_coords = target_coordinates
        cell_contents = self.model.grid.get_cell_list_contents([target_coordinates])
        # checks for semaphores
        traffic_lights = [obj for obj in cell_contents if isinstance(obj, SemaphoreAgent)]
        # checks for other cars
        other_cars = [obj for obj in cell_contents if isinstance(obj, CarAgent) and obj != self]

        if not traffic_lights or traffic_lights[0].state == "green":
            # Move only if there are no traffic lights or the traffic light is green
            if not other_cars:
                # Move only if the target cell is not occupied by another car
                self.model.grid.move_agent(self, target_coordinates)
                self.pos = target_coordinates
                self.path.pop(0)
                future_coords = self.path[0]
                self.rotationToPos = calculate_rotation_angle(old_coords, current_coords, future_coords)


    def step(self):
        self.move()

    def reached_final_position(self):
        return not bool(self.path)


class ParkingLotAgent(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos

class BuildingAgent(Agent):
    def __init__(self, unique_id, model, pos, color):
        super().__init__(unique_id, model)
        self.pos = pos
        self.color = color

    def step(self):
        pass


class SemaphoreAgent(Agent):
    def __init__(self, unique_id, model, pos, state):
        super().__init__(unique_id, model)
        self.pos = pos
        self.state = state # States: "red", "green"
        self.timer = 5  # Initial Time

    def change_state(self):
        if self.state == 'red' and self.timer == 0:
            self.state = 'green'
            self.timer = 3  # Green light duration
        elif self.state == 'green' and self.timer == 0:
            self.state = 'red'
            self.timer = 3  # Red light duration
        else:
            self.timer -= 1

    def step(self):
        self.change_state()


# Example usage:
start_coords = [1, 1]
current_coords = [2, 1]
future_coords = [2, -1]

rotation_angle = calculate_rotation_angle(start_coords, current_coords, future_coords)
print(f"Rotation Angle: {rotation_angle} degrees")