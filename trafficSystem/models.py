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
from .aStar import create_maximal_graph, astarComplete, manhattan_distance

# Import the logging configuration
setup_logging()

class TrafficModel(Model):
    """
    A model that simulates traffic flow. From cars agents trying to reach
    their destination.
    """

    def __init__(self, width, height, n_cars):
        self.G = create_maximal_graph(OptionMap)
        self.num_cars = n_cars
        self.num_finished_cars = 0
        self.completedCars = 0
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.ids = 1

        """ Create agents """
        # Car agents
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
                if isinstance(agent, CarAgent) and agent.reached_final_position():
                    self.grid.remove_agent(agent)
                    self.schedule.remove(agent)
                    self.num_finished_cars += 1


            """

            # Check parking lots and create new cars
            if creating_positions:
                for pos in creating_positions:
                    starting_pos = random.choice(Parkings)
                    target_pos = pos
                    while target_pos == starting_pos:
                        starting_pos = random.choice(Parkings)
                    print(f"Generating car at {starting_pos} to {target_pos}")
                    path = astar(self.G, starting_pos, target_pos, manhattan_distance)
                    c = CarAgent(self.ids, self, starting_pos, path)
                    self.ids += 1
                    self.schedule.add(c)
                    self.grid.place_agent(c, starting_pos)
                print(f"New cars generated: {len(creating_positions)}")

             """
        except Exception as e:
            # Handle the exception here, you can log it or print an error message
            print(f"An error occurred: {e}")


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
