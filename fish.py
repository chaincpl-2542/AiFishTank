import pygame
import random

MAX_SPEED = 7

COHERENCE_FACTOR = 0.01
ALIGNMENT_FACTOR = 0.1
SEPARATION_FACTOR = 0.05
SEPARATION_DISTANCE = 20
AGENT_RANGE = 40

class Fish:
    def __init__(self,x,y,screen) -> None:
        self.position = pygame.Vector2(x,y)
        self.velocity = pygame.Vector2(random.uniform(-MAX_SPEED, MAX_SPEED), random.uniform(-MAX_SPEED, MAX_SPEED))
        self.acceleration = pygame.Vector2(0,0)
        self.mess = 1
        self.screen = screen
        
    def update(self):
        self.velocity += self.acceleration
        if(self.velocity.length() >= MAX_SPEED):
            self.velocity = self.velocity.normalize() * MAX_SPEED
        self.position += self.velocity
        self.acceleration = pygame.Vector2(0,0)
 
    def apply_force(self,x,y): 
        force = pygame.Vector2(x,y)
        self.acceleration += force / self.mess
        
    def seek(self,x,y):
        d = pygame.Vector2(x,y) - self.position
        d = d.normalize() * 0.1
        seeking_force = d
        self.apply_force(seeking_force.x,seeking_force.y)
    
    def coherence(self, agents):    
        center_of_mass = pygame.Vector2(0,0)
        agent_in_range_count = 0
        for agent in agents:
            if agent != self:
                dist = self.position.distance_to(agent.position)
                if(dist < AGENT_RANGE):
                    center_of_mass += agent.position
                    agent_in_range_count += 1 
        
        if(agent_in_range_count > 0):
            center_of_mass /= agent_in_range_count    
            d = center_of_mass - self.position
            f = d * COHERENCE_FACTOR
            self.apply_force(f.x,f.y)
    
    def separation(self, agents):
        d = pygame.Vector2(0, 0)
        for agent in agents:
             if agent != self:
                dist = self.position.distance_to(agent.position)
                if(dist < SEPARATION_DISTANCE):
                    d += self.position - agent.position
                
        separation_force = d * SEPARATION_FACTOR

        self.apply_force(separation_force.x,separation_force.y)
    
    def alignment(self, agents):
        v = pygame.Vector2(0,0)
        agent_in_range_count = 0
        for agent in agents:
            if(agent != self):
                dist = self.position.distance_to(agent.position)
                if dist < AGENT_RANGE:
                    v += agent.velocity
                    agent_in_range_count += 1
    
        if agent_in_range_count > 0:
            v /= agent_in_range_count  # Calculate average velocity
            alignment_force = v * ALIGNMENT_FACTOR  # Apply alignment force
            self.apply_force(alignment_force.x, alignment_force.y)
    
    def draw(self):
        pygame.draw.circle(self.screen,"red",self.position,8)
        
    def findFood(self, foodPosition,food):
        dist = self.position.distance_to(foodPosition)
        if(dist < 100):
            velocity_x = foodPosition.x - self.position.x
            velocity_y = foodPosition.y - self.position.y
            self.velocity = pygame.Vector2(velocity_x,velocity_y)
            
            if(dist < 5):
                food.eaten()