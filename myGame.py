import pygame
import random
import pygame_gui
from food import Food
from slime import Slime
from giantSlime import GiantSlime

WIDTH = 1280
HEIGHT = 720

MAX_SLIME = 100
MAX_GIANT_SLIME = 8
MAXFOOD = 5

#-------------Setup-------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

font = pygame.font.Font(None, 25)

slimes = [Slime(random.uniform(0,WIDTH),random.uniform(0,HEIGHT),screen) for i in range(MAX_SLIME)]
giantSlimes = [GiantSlime(random.uniform(0,WIDTH),random.uniform(0,HEIGHT),screen) for i in range(MAX_GIANT_SLIME)]
foods = []

gui_manager = pygame_gui.UIManager((WIDTH,HEIGHT))
clock = pygame.time.Clock()
showDebugMode = False
                
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
    
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_q]):
        if(showDebugMode == True):
            showDebugMode = False
        else:
            showDebugMode = True
    
    for slime in slimes:
        slime.coherence(slimes)
        slime.separation(slimes)
        slime.alignment(slimes)
        slime.update()
        slime.draw(showDebugMode)
        slime.slimeOutOfArea()
        slime.update_animation()
        
        for giantSlime in giantSlimes:
            slime.find_closest_GiantSlime(giantSlimes)
            slime.findGiantSlime()
            
        if(len(foods) > 0):
            for food in foods:
                slime.findFood(food.foodPosition,food)
                
                
    for giantSlime in giantSlimes:
        giantSlime.update()
        giantSlime.draw()
        giantSlime.slimeOutOfArea()
        giantSlime.update_animation()
        giantSlime.slime_name = f"Giant Slime {giantSlimes.index(giantSlime) + 1}"
        
        name_text = font.render(giantSlime.slime_name, True, (0, 0, 0))  # Adjust text color as needed
        name_rect = name_text.get_rect(center=(giantSlime.position.x, giantSlime.position.y - 40))  # Adjust offset as needed
        if(showDebugMode == True):
            screen.blit(name_text, name_rect)
    
    if(len(foods) < MAXFOOD):
        if pygame.mouse.get_pressed()[0]:
            foods.append(Food(pygame.Vector2(pygame.mouse.get_pos()),screen))
        
    if(len(foods) > 0):
        for food in foods:
            food.draw()
            food.update_animation()
                
    foods = [food for food in foods if not food.isEat]    
        
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, pygame.Color('white'))
    screen.blit(fps_text, (WIDTH - fps_text.get_width() - 10, 10))
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()