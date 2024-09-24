import pygame
import random
import math
import pygame_gui

WIDTH = 1280
HEIGHT = 720
MAX_SPEED = 7
NUMBER_AGENT = 80

COHERENCE_FACTOR = 0.01
ALIGNMENT_FACTOR = 0.1
SEPARATION_FACTOR = 0.05
SEPARATION_DISTANCE = 20
AGENT_RANGE = 40
MAXFOOD = 5

class Agent:
    def __init__(self,x,y) -> None:
        self.position = pygame.Vector2(x,y)
        self.velocity = pygame.Vector2(random.uniform(-MAX_SPEED, MAX_SPEED), random.uniform(-MAX_SPEED, MAX_SPEED))
        self.acceleration = pygame.Vector2(0,0)
        self.mess = 1
        
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
        pygame.draw.circle(screen,"red",self.position,8)
        
    def findFood(self, foodPosition,food):
        dist = self.position.distance_to(foodPosition)
        if(dist < 100):
            velocity_x = foodPosition.x - self.position.x
            velocity_y = foodPosition.y - self.position.y
            self.velocity = pygame.Vector2(velocity_x,velocity_y)
            
            if(dist < 5):
                food.eaten()
            
class Food:
    def __init__(self,foodPosition):
        self.foodPosition = pygame.Vector2(foodPosition.x,foodPosition.y)
        self.isEat = False
        
    def draw(self):
        pygame.draw.circle(screen,"brown",self.foodPosition,5)
        
    def eaten(self):
        self.isEat = True

#-------------Setup-------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

font = pygame.font.Font(None, 36)

agents = [Agent(random.uniform(0,WIDTH),random.uniform(0,HEIGHT)) for i in range(NUMBER_AGENT)]
foods = []

gui_manager = pygame_gui.UIManager((WIDTH,HEIGHT))
clock = pygame.time.Clock()

                
while running:
    time_delta = clock.tick(60)/1000.0
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            
        gui_manager.process_events(event)
    gui_manager.update(time_delta)
    gui_manager.draw_ui(screen)
            
    screen.fill("gray")
    
    for agent in agents:
        agent.coherence(agents)
        agent.separation(agents)
        agent.alignment(agents)
        agent.update()
        agent.draw()
        
        if(len(foods) > 0):
            for food in foods:
                agent.findFood(food.foodPosition,food)
    
    if(len(foods) < MAXFOOD):
        if pygame.mouse.get_pressed()[0]:
            foods.append(Food(pygame.Vector2(pygame.mouse.get_pos())))
        
    if(len(foods) > 0):
        for food in foods:
            food.draw()
                
    foods = [food for food in foods if not food.isEat]    
            
    for agent in agents:
        if(agent.position.x > WIDTH):
            agent.position.x = 0
        elif(agent.position.x < 0):
             agent.position.x = WIDTH
        if(agent.position.y > HEIGHT):
            agent.position.y = 0
        elif(agent.position.y < 0):
              agent.position.y = HEIGHT

    
        
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, pygame.Color('white'))
    screen.blit(fps_text, (WIDTH - fps_text.get_width() - 10, 10))
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()