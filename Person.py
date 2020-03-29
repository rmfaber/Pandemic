from mesa import Agent
import random

class Person(Agent):
    """A person in the model
    
    Attributes
    ------------------
    state, str
        The state of the person. Can be healthy, infected, or immune
    
    time_infected, int
        The time-step of the model when the person was infected
    
    Methods
    ------------------
    
    infect
        if agent is infected, they can infect other people around them
    
    heal or die
        if agent is infected, they will heal a certain time after infection
    
    move
        agents move to an empty cell surrounding them 
    """
    def __init__(self, unique_id, model, state):
        super().__init__(unique_id, model)
        self.state = state
        self.r0 = 0
        
        # Get time when people are infected
        if self.state == 'infected':
            self.time_infected = self.model.schedule.time
            self.days_ill = self.random.randint(self.model.min_time_disease, self.model.max_time_disease)
            self.time_healdie = self.time_infected + self.days_ill
        
    def infect(self):
        """Infect neighbors"""
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
                        self.r0 += 1
                        neighbor.state = 'infected'
                        neighbor.time_infected = self.model.schedule.time
                        neighbor.days_ill = neighbor.random.randint(self.model.min_time_disease, self.model.max_time_disease)
                        neighbor.time_healdie = neighbor.time_infected + neighbor.days_ill                
                    
    def heal_or_die(self):
        """heal after a certain amount of time"""
        if self.state == 'infected':
            if self.model.schedule.time == self.time_healdie:
                if self.random.uniform(0,1) <= self.model.death_rate:
                    self.state = 'dead'
                else:
                    self.state = 'immune'
                
    def move(self):
        """move to an empty cell near the person"""
        if self.state == 'dead':
            return
        neighbors = [cell for cell in (self.model.grid.iter_neighborhood(self.pos, moore=True))]
        self.random.shuffle(neighbors)
        for cell in neighbors:
            if self.model.grid.is_cell_empty(cell):
                self.model.grid.move_agent(self, cell)
                break
        
    def step(self):
        self.infect()
        self.heal_or_die()
        self.move()   
        