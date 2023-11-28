from mesa.visualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from trafficSystem.agents import CarAgent, ParkingLotAgent, BuildingAgent, SemaphoreAgent
from trafficSystem.models import TrafficModel
from trafficSystem.map import grid_size

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
                "Color": "orange",
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
        elif agent.state == 'yellow':
            color = {
                    "Shape": "rect",
                    "Color": "yellow",
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
    TrafficModel, [grid], "Traffic Model", {"width": grid_size, "height": grid_size, "n_cars": 110}
)

server.port = 8521

server.launch()
