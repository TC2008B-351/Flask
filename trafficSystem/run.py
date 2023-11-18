from mesa.visualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from .agents import CarAgent, ParkingLotAgent, BuildingAgent, SemaphoreAgent
from .models import TrafficModel
from .map import grid_size

def color_agent(agent):
    color = {}
    if isinstance(agent, CarAgent):
        color = {
                "Shape": "rect",
                "Color": "gray",
                "Filled": "true",
                "Layer": 0,
                "w": 1,
                "h": 1
                }
    if isinstance(agent, ParkingLotAgent):
        color = {
                "Shape": "rect",
                "Color": "yellow",
                "Filled": "true",
                "Layer": 0,
                "w": 1,
                "h": 1
                }
    if isinstance(agent, SemaphoreAgent):
        if agent.state == 'red':
            color = {
                    "Shape": "rect",
                    "Color": "red",
                    "Filled": "true",
                    "Layer": 0,
                    "w": 1,
                    "h": 1
                    }
        else:
            color = {
                    "Shape": "rect",
                    "Color": "green",
                    "Filled": "true",
                    "Layer": 0,
                    "w": 1,
                    "h": 1
                    }
    if isinstance(agent, BuildingAgent):
        color = {
                "Shape": "rect",
                "Color": agent.color,
                "Filled": "true",
                "Layer": 0,
                "w": 1,
                "h": 1
                }
    return color


grid = CanvasGrid(color_agent,grid_size, grid_size)

server = ModularServer(
    TrafficModel, [grid], "Traffic Model", {"width": grid_size, "height": grid_size, "n_agents": 1}
)

server.port = 8521

server.launch()
