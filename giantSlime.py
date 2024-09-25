import pygame
import random

MAX_SPEED = 2

SIZE = 20
COLOR = (194,25,8)

class GiantSlime:
    def __init__(self,x,y,screen) -> None:
        self.position = pygame.Vector2(x,y)
        self.velocity = pygame.Vector2(random.uniform(-MAX_SPEED, MAX_SPEED), random.uniform(-MAX_SPEED, MAX_SPEED))
        self.acceleration = pygame.Vector2(0,0)
        self.mess = 1
        self.screen = screen
        self.slime_name = ""
        
        self.frame_size = 96
        self.fx = 0
        self.fy = 1
        self.time = 0
        self.animation_frame_rate = 3
        
        self.slime_sprite = pygame.image.load("./assets/GiantSlimeAnimation96.png")
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
    
    def draw(self):
        # pygame.draw.circle(self.screen,COLOR,self.position,SIZE)
        self.screen.blit(self.agent_frame, self.position - pygame.Vector2(48, 48))


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