from mesa import Model, Agent
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random

class Person(Agent):
    def __init__(self, unique_id, model, state):
        super().__init__(unique_id, model)
        self.state = state
        
        # Get time when people are infected
        if self.state == 'infected':
            self.time_infected = self.model.schedule.time
            self.days_ill = self.random.randint(self.model.min_time_disease, self.model.max_time_disease)
            self.time_healed = self.time_infected + self.days_ill
        
    def infect(self):
        if self.state == 'infected':
            neighboring_cells = self.model.grid.get_neighborhood(
                self.pos,
                moore=True,
                include_center=False
            )
            for neighbor in self.model.grid.neighbor_iter(self.pos):
                # Can only infect people who are healthy
                if neighbor.state == 'healthy':
                    if self.random.uniform(0,1) < self.model.infect_prob:
                        neighbor.state = 'infected'
                        neighbor.time_infected = self.model.schedule.time
                        neighbor.days_ill = neighbor.random.randint(self.model.min_time_disease, self.model.max_time_disease)
                        neighbor.time_healed = neighbor.time_infected + neighbor.days_ill
                        
                    
    def heal_or_die(self):
        if self.state == 'infected':
            if self.model.schedule.time == self.time_healed:
                self.state = 'immune'
                
    def move(self):
        neighbors = [cell for cell in (self.model.grid.iter_neighborhood(self.pos, moore=True))]
        random.shuffle(neighbors)
        for cell in neighbors:
            if self.model.grid.is_cell_empty(cell):
                self.model.grid.move_agent(self, cell)
                break
        
    def step(self):
        self.infect()
        self.heal_or_die()
        self.move()
        
def get_N_infected(model):
    Infected = [agent.state for agent in model.schedule.agents if agent.state == 'infected']
    N_infected = len(Infected)
    return N_infected

def get_N_immune(model):
    Immune = [agent.state for agent in model.schedule.agents if agent.state == 'immune']
    N_immune = len(Immune)
    return N_immune     
        
class Pandemic(Model):
    def __init__(self, height=100,width=100,N=500,N_initial_infected=2, infect_prob = 0.05, min_time_disease = 5, max_time_disease = 15):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, False)
        self.N_infected = N_initial_infected
        self.infect_prob = infect_prob
        self.min_time_disease = min_time_disease
        self.max_time_disease = max_time_disease
        
        self.running = True
        
        # Create agents
        N_infected_placed = 0
        for i in range(self.num_agents):
            if N_infected_placed < self.N_infected:
                a = Person(i, self, state = 'infected')
                N_infected_placed += 1
            else:
                a = Person(i, self, state = 'healthy')
            self.schedule.add(a)
            self.grid.position_agent(a)
            
        self.datacollector = DataCollector(
            model_reporters = {"N_infected":get_N_infected,
                              "N_immune":get_N_immune},
            agent_reporters = {"State": "state"}
        )
    
    def check_N_infected(self):
        N_infected = get_N_infected
        if N_infected == 0:
            self.running = False
    
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
            
            
                
                
        
        
        