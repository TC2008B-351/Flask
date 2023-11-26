import random
from logging import info
from .logging.log_conf import setup_logging
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from .agents import CarAgent, ParkingLotAgent, BuildingAgent, SemaphoreAgent
from .map import IntersectionPoints, Parkings, OutGoingCarPoints, Buildings, Semaphores, grid_size
from .aStar import create_graph, astar, manhattan_distance, display_path_on_grid

# Import the logging configuration
setup_logging()

class TrafficModel(Model):
    """
    A model that simulates traffic flow. From cars agents trying to reach
    their destination.
    """

    def __init__(self, width, height, n_agents):
        self.G = create_graph(IntersectionPoints)
        self.num_agents = n_agents  # unused
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.ids = 1

        """ Create agents """
        # Car agents
        starts = Parkings[:]
        targets = Parkings[:]
        for _ in range(len(Parkings)):
            starting_pos = starts.pop(0)
            target_pos = targets.pop()
            if starting_pos == target_pos:
                starting_pos = starts[0]
            path = astar(self.G, starting_pos, target_pos, manhattan_distance)
            c = CarAgent(self.ids, self, starting_pos, path)
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
        except Exception as e:
            # Handle the exception here, you can log it or print an error message
            print(f"An error occurred: {e}")
        """
        try:

            finished_cars = []
            creating_positions = set()
            conflicting_cars = []

            # Check cars that have reached its destination
            for agent in self.schedule.agents:
                if isinstance(agent, CarAgent) and agent.reached_final_position():
                    finished_cars.append(agent)
                    creating_positions.add(agent.pos)


            #   This handles were a car is going out and a car wants to enter
            for car in finished_cars:
                for agent in self.schedule.agents:
                    if isinstance(agent, CarAgent) and OutGoingCarPoints[car.pos] == agent.pos:
                        finished_cars.append(agent)
                        print(car.pos)
                        print(car)


            # Remove finished cars from the schedule and the grid
            for car in finished_cars:
                self.grid.remove_agent(car)
                self.schedule.remove(car)


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


        except Exception as e:
            # Handle the exception here, you can log it or print an error message
            print(f"An error occurred: {e}")
        """

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
