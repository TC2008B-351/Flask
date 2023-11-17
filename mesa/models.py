import random
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agents import CarAgent, ParkingLotAgent, BuildingAgent, SemaphoreAgent
from map import IntersectionPoints, Parkings, Buildings, Semaphores
from aStar import create_graph, astar, manhattan_distance

class TrafficModel(Model):
    """
    A model that simulates traffic flow. From cars agents trying to reach
    their destination.
    """
    def __init__(self, width, height, n_cars):
        self.G = create_graph(IntersectionPoints)
        self.num_cars = n_cars
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        ids = 0

        """ Create agents """
        # Parking Lot agents
        for coord in Parkings:
            pl = ParkingLotAgent(ids, self, coord)
            ids += 1
            self.schedule.add(pl)
            self.grid.place_agent(pl, coord)
        # Building agents
        for data in Buildings:
            coord, color = data
            b = BuildingAgent(ids, self, coord, color)
            ids += 1
            self.schedule.add(b)
            self.grid.place_agent(b, coord)
        # Semaphore agents
        for data in Semaphores:
            coord, state = data
            s = SemaphoreAgent(ids, self, coord, state)
            ids += 1
            self.schedule.add(s)
            self.grid.place_agent(s, coord)
        # Car agents
        for _ in range(n_cars):
            starting_pos = random.choice(list(IntersectionPoints.keys()))
            target_pos = random.choice(Parkings)
            path = astar(self.G, starting_pos, target_pos, manhattan_distance)
            path_HC = [(2,1), (2,2)]
            c = CarAgent(ids, self, starting_pos, path)
            ids += 1
            self.schedule.add(c)
            self.grid.place_agent(c, starting_pos)


    def step(self):
        self.schedule.step()