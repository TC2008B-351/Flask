from mesa import Agent
import random
from map import Steps, Parkings

def buildPathFrom():
    pass

class CarAgent(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.target_pos = random.choice(Parkings)
        self.path = self.buildPath(self.pos, self.target_pos)

    @staticmethod
    def buildPath(current_coords, target_coords, steps = Steps):
        pass

    def move(self):
        target_coordinates = self.path.pop(0)
        cell_contents = self.model.grid.get_cell_list_contents([target_coordinates])
        traffic_lights = [obj for obj in cell_contents if isinstance(obj, SemaphoreAgent)]

        if not traffic_lights or traffic_lights[0].state == "green":
            # Move only if there are no traffic lights or the traffic light is green
            self.model.grid.move_agent(self, target_coordinates)
            self.pos = target_coordinates

    def step(self):
        self.move()

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
        self.state = state
        self.timer = 0

    def change_state(self):
        if self.state == 'red':
            new_state = 'green'
        else:
            new_state = 'red'
        self.state = new_state

    def step(self):
        self.timer += 1
        if self.timer == 5:
            self.change_state()
            self.timer = 0
