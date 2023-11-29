"""
Traffic Model
"""
import random
from logging import info
from .logging.log_conf import setup_logging
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from .agents import CarAgent, ParkingLotAgent, BuildingAgent, SemaphoreAgent
from .map import Parkings, Buildings, Semaphores
from .completeMap import OptionMap
from .aStar import create_maximal_graph, astarComplete, manhattan_distance, display_path_on_grid

# Import the logging configuration
setup_logging()

class TrafficModel(Model):
    """
    A model that simulates traffic flow. From cars agents trying to reach
    their destination.
    """
    def create_car_agents(self):
        options = list(OptionMap.keys())
        for _ in range(self.num_cars):
            starting_pos = random.choice(options)
            target_pos = random.choice(Parkings)
            while starting_pos == target_pos:
                starting_pos = random.choice(options)
            path = astarComplete(self.G, starting_pos, target_pos, manhattan_distance)
            c = CarAgent(self.ids, self, starting_pos, target_pos, path)
            self.ids += 1
            self.schedule.add(c)
            self.grid.place_agent(c, starting_pos)

    def __init__(self, width, height, n_cars):
        self.G = create_maximal_graph(OptionMap)
        self.num_cars = n_cars
        self.completedCars = 0
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.ids = 1

        """ Create agents """
        # Car agents
        self.create_car_agents()
        # Parking Lot agents
        for coord in Parkings:
            pl = ParkingLotAgent(self.ids, self, coord)
            self.ids += 1
            self.schedule.add(pl)
            self.grid.place_agent(pl, coord)
        # Building agents
        for data in Buildings:
            coord, color = data
            b = BuildingAgent(self.ids, self, coord, color)
            self.ids += 1
            self.schedule.add(b)
            self.grid.place_agent(b, coord)
        # Semaphore agents
        for data in Semaphores:
            coord, state = data
            s = SemaphoreAgent(self.ids, self, coord, state)
            self.ids += 1
            self.schedule.add(s)
            self.grid.place_agent(s, coord)

    def step(self):
        try:
            self.schedule.step()
            for agent in self.schedule.agents:
                if isinstance(agent, CarAgent) and agent.reached_goal:
                    self.grid.remove_agent(agent)
                    self.schedule.remove(agent)
                    self.completedCars += 1

            if self.completedCars == self.num_cars:
                self.create_car_agents()
                self.completedCars = 0
        except Exception as e:
            # Handle the exception here, you can log it or print an error message
            print(f"An error occurred: {e}")

    def getInitialCarState(self):
        carPositions = []
        for agent in self.schedule.agents:
            if isinstance(agent, CarAgent):
                id = agent.unique_id
                x_coord, y_coord = agent.pos
                carPositions.append([id, x_coord, y_coord])
        return sorted(carPositions, key= lambda x: x[0])

    def getCarState(self):
        carPositions = []
        for agent in self.schedule.agents:
            if isinstance(agent, CarAgent):
                id = agent.unique_id
                x1_coord, y1_coord = agent.pos
                try:
                    x2_coord, y2_coord = agent.path[0]
                except IndexError:
                    x2_coord, y2_coord = agent.pos
                try:
                    x3_coord, y3_coord = agent.path[1]
                except IndexError:
                    x3_coord, y3_coord = x2_coord, y2_coord
                carPositions.append([id, x1_coord, y1_coord, x2_coord, y2_coord, x3_coord, y3_coord])
        return sorted(carPositions, key= lambda x: x[0])

    def getSemaphoreState(self):
        carLights = []
        for agent in self.schedule.agents:
            if isinstance(agent, SemaphoreAgent):
                id = agent.unique_id
                pos = agent.pos
                state = agent.state
                carLights.append([id, pos, state])
        return sorted(carLights, key= lambda x: x[0])
