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
    
    def __init__(self, width, height, n_agents):
        self.G = create_graph(IntersectionPoints)
        self.num_agents = n_agents  # unused
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
        starts = list(IntersectionPoints.keys())
        random.shuffle(starts)
        targets = Parkings[:]
        for _ in range(len(targets)):
            starting_pos = starts.pop()
            target_pos = targets.pop()
            path = astar(self.G, starting_pos, target_pos, manhattan_distance)
            c = CarAgent(ids, self, starting_pos, path)
            ids += 1
            self.schedule.add(c)
            self.grid.place_agent(c, starting_pos)

    def step(self):
        self.schedule.step()

    def getPositions(self):
        carPositions = []
        for agent in self.schedule.agents:
            if isinstance(agent, CarAgent):
                id = agent.id
                x_coord, y_coord = agent.pos
                carPositions.append([id, x_coord, y_coord])
        return carPositions
