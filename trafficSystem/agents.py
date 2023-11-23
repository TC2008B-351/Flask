from mesa import Agent

class CarAgent(Agent):
    def __init__(self, unique_id, model, pos, path):
        super().__init__(unique_id, model)
        self.pos = pos
        self.path = path

    def move(self):
        if not self.path:
            return
        target_coordinates = self.path[0]
        cell_contents = self.model.grid.get_cell_list_contents([target_coordinates])
        # checks for semaphores
        traffic_lights = [obj for obj in cell_contents if isinstance(obj, SemaphoreAgent)]
        #checks for parking lots
        parking_lot = [obj for obj in cell_contents if isinstance(obj, ParkingLotAgent)]
        # checks for other cars
        other_cars = [obj for obj in cell_contents if isinstance(obj, CarAgent) and obj != self]

        if not traffic_lights or traffic_lights[0].state == "green":
            # Move only if there are no traffic lights or the traffic light is green
            if not parking_lot or not parking_lot[0].is_occupied:
                # Move only if the parking lot is unoccupied
                if not other_cars:
                    # Move only if the target cell is not occupied by another car
                    self.model.grid.move_agent(self, target_coordinates)
                    self.pos = target_coordinates
                    self.path.pop(0)
                    if parking_lot:
                        parking_lot[0].occupy()

    def step(self):
        self.move()


class ParkingLotAgent(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.is_occupied = False

    def occupy(self):
        self.is_occupied = True

    def vacate(self):
        self.is_occupied = False


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
