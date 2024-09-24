import pygame
import random

MAX_SPEED = 1

SIZE = 20
COLOR = (194,25,8)

class GiantFish:
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
    
    def draw(self):
        pygame.draw.circle(self.screen,COLOR,self.position,SIZE)

    def fishOutOfArea(self):
        if(self.position.x > self.screen.get_width()):
            self.position.x = 0
        elif(self.position.x < 0):
            self.position.x = self.screen.get_width()
        if(self.position.y > self.screen.get_height()):
            self.position.y = 0
        elif(self.position.y < 0):
            self.position.y = self.screen.get_height()
        