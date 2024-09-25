import pygame
import random

MAX_SPEED = 3

COHERENCE_FACTOR = 0.01
ALIGNMENT_FACTOR = 0.1
SEPARATION_FACTOR = 0.05
SEPARATION_DISTANCE = 25
AGENT_RANGE = 50

AGENT_FOOD_RANGE = 120
AGENT_EAT_RANGE = 8


MIN_AGENT_RANGE = 50
MAX_AGENT_RANGE = 100

OBSCRACT_FORCE = 0.1
SIZE = 7
COLOR = (6,87,185)

giantSlime = None
cooldown_duration = 2000
cooldown_counter = 0


class Slime:
    def __init__(self,x,y,screen) -> None:
        self.position = pygame.Vector2(x,y)
        self.velocity = pygame.Vector2(random.uniform(-MAX_SPEED, MAX_SPEED), random.uniform(-MAX_SPEED, MAX_SPEED))
        self.acceleration = pygame.Vector2(0,0)
        self.mess = 1
        self.screen = screen
        self.force = 0
        self.closest_GiantSlime = None
        self.tooCloseGiantSlime = False
        
        self.frame_size = 32
        self.fx = 0
        self.fy = 1
        self.time = 0
        self.animation_frame_rate = 3
        
        self.slime_sprite = pygame.image.load("./assets/SlimeAnimation.png")
        self.agent_frame = self.slime_sprite.subsurface(pygame.Rect( self.fx * self.frame_size, self.fy * self.frame_size,
                                                                    self.frame_size,
                                                                    self.frame_size))
                
    def update(self):
        self.velocity += self.acceleration
        if(self.velocity.length() >= MAX_SPEED):
            self.velocity = self.velocity.normalize() * MAX_SPEED
        self.position += self.velocity
        self.acceleration = pygame.Vector2(0,0)
        
        if abs(self.velocity.x) > abs(self.velocity.y):
            if(self.velocity.x > 0):
                self.fy = 3
            elif(self.velocity.x < 0):
                self.fy = 2
        else:
            if(self.velocity.y > 0):
                self.fy = 0
            elif(self.velocity.y < 0):
                self.fy = 1
            
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
                if(self.tooCloseGiantSlime == False):
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
                if(self.tooCloseGiantSlime == False):
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
                if(self.tooCloseGiantSlime == False):
                    if (dist < AGENT_RANGE):
                        v += agent.velocity
                        agent_in_range_count += 1
    
        if agent_in_range_count > 0:
            v /= agent_in_range_count
            alignment_force = v * ALIGNMENT_FACTOR 
            self.apply_force(alignment_force.x, alignment_force.y)
    
    def draw(self,isShowDebug):
        # pygame.draw.circle(self.screen,COLOR,self.position,SIZE)
        self.screen.blit(self.agent_frame, self.position - pygame.Vector2(16, 16)  )
        if(isShowDebug == True):
            pygame.draw.line(self.screen, "red", self.position, self.position + self.velocity * 10 )
            

        
    def findFood(self, foodPosition,food):
        dist = self.position.distance_to(foodPosition)
        if(self.tooCloseGiantSlime == False):
            if(dist < AGENT_FOOD_RANGE ):
                velocity_x = foodPosition.x - self.position.x
                velocity_y = foodPosition.y - self.position.y
                self.velocity = pygame.Vector2(velocity_x,velocity_y)
                
        if(dist < AGENT_EAT_RANGE):
            food.eaten()        
        
                
    def findGiantSlime(self):
        if(self.closest_GiantSlime != None):
            dist = self.position.distance_to(self.closest_GiantSlime.position)

            if(dist < MAX_AGENT_RANGE):
                self.tooCloseGiantSlime = True
                if(dist > MIN_AGENT_RANGE):
                    self.force = OBSCRACT_FORCE - (dist / MAX_AGENT_RANGE) * OBSCRACT_FORCE
                    self.velocity.x += self.force * (self.position.x - self.closest_GiantSlime.position.x) / dist
                    self.velocity.y += self.force * (self.position.y - self.closest_GiantSlime.position.y) / dist
                    
                else:
                    self.force = OBSCRACT_FORCE + 2
            else:
                self.tooCloseGiantSlime = False
            
    def find_closest_GiantSlime(self,giantSlimes):
        closest_distance = float('inf')

        for giantSlime in giantSlimes:
            distance = self.position.distance_to(giantSlime.position)
            if distance < closest_distance:
                self.closest_GiantSlime = giantSlime
                closest_distance = distance
 
    def slimeOutOfArea(self):
        if(self.position.x > self.screen.get_width()):
            self.position.x = 0
        elif(self.position.x < 0):
            self.position.x = self.screen.get_width()
        if(self.position.y > self.screen.get_height()):
            self.position.y = 0
        elif(self.position.y < 0):
            self.position.y = self.screen.get_height()
            
    def update_animation(self):
        if self.time > self.animation_frame_rate:
            self.fx = self.fx + 1
            self.fx = self.fx%4
            
            self.agent_frame = self.slime_sprite.subsurface(pygame.Rect( self.fx * self.frame_size, 
                                                    self.fy * self.frame_size,
                                                    self.frame_size,
                                                    self.frame_size))
            
            self.time = 0
        else:
            self.time = self.time + 1