from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

from model import Pandemic

def agent_portrayal(agent):
    portrayal = {
        "Shape":'circle',
        "Filled":'true',
        'r':0.5
    }
    
    if agent.state == 'healthy':
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 0
    elif agent.state == 'infected':
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    elif agent.state == "immune":
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
    elif agent.state == "dead":
        portrayal["Color"] = "black"
        portrayal["Layer"] = 0
    
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 50, 500)

chart = ChartModule([{
    "Label": "N_infected",
    "Color":"Black"
},
    {"Label":"N_immune",
     "Color":"Green"        
    }

], data_collector_name = 'datacollector')

server = ModularServer(
    Pandemic,
    [grid, chart],
    "Pandemic",
    {"height":10,
    "width":10,
    "N":75,
    "N_initial_infected":2}
)