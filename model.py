from mesa import Model, Agent
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random

from Person import Person

def get_N_infected(model):
    """Get the number of infected people at a step in the model"""
    Infected = [agent.state for agent in model.schedule.agents if agent.state == 'infected']
    N_infected = len(Infected)
    return N_infected

def get_N_immune(model):
    """Get the number of immune people at a step in the model"""
    Immune = [agent.state for agent in model.schedule.agents if agent.state == 'immune']
    N_immune = len(Immune)
    return N_immune  

def get_N_dead(model):
    """Get the number of immune people at a step in the model"""
    Dead = [agent.state for agent in model.schedule.agents if agent.state == 'dead']
    N_dead = len(Dead)
    return N_dead  

def get_N_state(model, state):
    """Get the number of people with a certain state at a certain step in the model"""
    agents_with_state = [agent.state for agent in model.schedule.agents if agent.state == state]
    N_state = len(agents_with_state)
    return N_state

class Pandemic(Model):
    """Modeling an infection spreading across a population"""
    def __init__(self, height=100,width=100,N=500,N_initial_infected=2, infect_prob = 0.05, min_time_disease = 5, max_time_disease = 15, death_rate = 0.05):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, False)
        self.N_infected = N_initial_infected
        self.infect_prob = infect_prob
        self.min_time_disease = min_time_disease
        self.max_time_disease = max_time_disease
        self.death_rate = death_rate
        
        self.running = True
        
        # Create agents
        N_infected_placed = 0
        for i in range(self.num_agents):
            # place as many infected as indicated
            if N_infected_placed < self.N_infected:
                a = Person(i, self, state = 'infected')
                N_infected_placed += 1
            else:
                a = Person(i, self, state = 'healthy')
            self.schedule.add(a)
            self.grid.position_agent(a)
            
        self.datacollector = DataCollector(
            model_reporters = {"N_infected":get_N_infected,
                              "N_immune":get_N_immune,
                               "N_dead":get_N_dead},
            agent_reporters = {"State": "state"}
        )
    
    def check_N_infected(self):
        N_infected = get_N_infected
        if N_infected == 0:
            self.running = False
    
    def step(self):
        self.datacollector.collect(self)
        self.check_N_infected()
        self.schedule.step()
            
            
                
                
        
        
        