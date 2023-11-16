from mesa import Agent
import random

class CarAgent(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos

    def move(self, new_position):
        # Implement the logic to move the agent to a new position
        self.model.grid.move_agent(self, new_position)
        self.pos = new_position
        
    def step(self):
        pass

class SemaphoreAgent(Agent):
    def __init__(self, unique_id, model, pos, state):
        super().__init__(unique_id, model)
        self.pos = pos
        self.state = state

    def change_state(self):
        if self.state == 'red':
            new_state = 'green'
        else:
            new_state = 'red'
        self.state = new_state

    def step(self):
        pass
        