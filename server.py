from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

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

grid = CanvasGrid(agent_portrayal, 25, 25, 750, 750)

N_chart = ChartModule([{
    "Label": "N_infected",
    "Color":"Red"
},
    {"Label":"N_immune",
     "Color":"Green"        
    },
    {"Label":"N_dead",
    "Color":"Black"}

], data_collector_name = 'datacollector')

r0_chart = ChartModule([{
    "Label": "Average r0",
    "Color":"Black"
}], data_collector_name = 'datacollector')

server = ModularServer(
    Pandemic,
    [grid, N_chart, r0_chart],
    "Pandemic",
    {"height":25,
    "width":25,
    "N":400,
    "N_initial_infected":UserSettableParameter("slider","Initial number of infected",10,1,100,1),
    "infect_prob":UserSettableParameter("slider","Infection probability",0.05,0.01,1,0.01),
     "death_rate":UserSettableParameter("slider","Death rate",0.05,0.01,1,0.01)}
)