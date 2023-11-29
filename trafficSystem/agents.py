import math
from mesa import Agent
import random
from .map import Parkings
from .aStar import astarComplete, manhattan_distance

class CarAgent(Agent):
    def __init__(self, unique_id, model, pos, t_pos, path):
        super().__init__(unique_id, model)
        self.pos = pos
        self.target_pos = t_pos
        self.path = path
        self.rotationToPos = 0
        self.jammedCounter = 0
        self.reached_goal = False

    def recalculateNewPath(self):
        new_target_pos = random.choice(Parkings)
        while new_target_pos == self.target_pos:
            new_target_pos = random.choice(Parkings)
        self.target_pos = new_target_pos
        self.path = astarComplete(self.model.G, self.pos, self.target_pos, manhattan_distance)
        self.jammedCounter = 0

    def move(self):
        if not self.path:
            self.reached_goal = True
            return
        
        # If the car has been in a jam for 5 steps, recalculate the path to a new target Parking
        if self.jammedCounter >= 5:
            self.recalculateNewPath()

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
                # If the car is not jammed, then the jammedCounter is reset
                self.jammedCounter = 0
            # If there is a car, then is jammed and the jammedCounter is increased
            else:
                self.jammedCounter += 1

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
        self.state = state # States: "red", "green", "yellow"
        self.timer = 3  # Initial Time

    def change_state(self):
        if self.state == 'red' and self.timer == 0:
            self.state = 'green'
            self.timer = 3  # Green light duration
        elif self.state == 'yellow' and self.timer == 0:
            self.state = 'red'
            self.timer = 2  # Red light duration
        elif self.state == 'green' and self.timer == 0:
            self.state = 'yellow'
            self.timer = 1  # Yellow light duration
        else:
            self.timer -= 1

    def step(self):
        self.change_state()
