from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agents import CarAgent, SemaphoreAgent
from map import Parkings, Semaphores

class TrafficModel(Model):
    """
    A model that simulates traffic flow. From cars agents trying to reach
    their destination.
    """
    def __init__(self, width, height, n_agents):
        self.num_agents = n_agents
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        ids = 0

        """ Create agents """
        # 1 Parking lot agents
        for coord in Parkings:
            a = CarAgent(ids, self, coord)
            ids += 1
            self.schedule.add(a)
            self.grid.place_agent(a, coord)
        # 2 Building agents
        # 3 Semaphores agents
        for data in Semaphores:
            coord, state = data
            a = SemaphoreAgent(ids, self, coord, state)
            ids += 1
            self.schedule.add(a)
            self.grid.place_agent(a, coord)
        

    def step(self):
        self.schedule.step()