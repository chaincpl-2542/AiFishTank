import pygame
import random
import pygame_gui
from food import Food
from fish import Fish
from giantFish import GiantFish

WIDTH = 1280
HEIGHT = 720

MAX_FISH = 100
MAX_GIANT_FISH = 20
MAXFOOD = 5

#-------------Setup-------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

font = pygame.font.Font(None, 36)

fishs = [Fish(random.uniform(0,WIDTH),random.uniform(0,HEIGHT),screen) for i in range(MAX_FISH)]
giantFishs = [GiantFish(random.uniform(0,WIDTH),random.uniform(0,HEIGHT),screen) for i in range(MAX_GIANT_FISH)]
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
    
    for fish in fishs:
        fish.coherence(fishs)
        fish.separation(fishs)
        fish.alignment(fishs)
        fish.update()
        fish.draw()
        fish.fishOutOfArea()
        for giantFish in giantFishs:
            fish.findGiantFish(giantFish.position)
        
        if(len(foods) > 0):
            for food in foods:
                fish.findFood(food.foodPosition,food)
                
    for giantFish in giantFishs:
        giantFish.update()
        giantFish.draw()
        giantFish.fishOutOfArea()
    
    if(len(foods) < MAXFOOD):
        if pygame.mouse.get_pressed()[0]:
            foods.append(Food(pygame.Vector2(pygame.mouse.get_pos()),screen))
        
    if(len(foods) > 0):
        for food in foods:
            food.draw()
                
    foods = [food for food in foods if not food.isEat]    
        
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, pygame.Color('white'))
    screen.blit(fps_text, (WIDTH - fps_text.get_width() - 10, 10))
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()