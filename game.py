import pygame
import random
import math
import pygame_gui
from food import Food
from fish import Fish

WIDTH = 1280
HEIGHT = 720

NUMBER_AGENT = 80


MAXFOOD = 5

#-------------Setup-------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

font = pygame.font.Font(None, 36)

fishs = [Fish(random.uniform(0,WIDTH),random.uniform(0,HEIGHT),screen) for i in range(NUMBER_AGENT)]
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
        
        if(len(foods) > 0):
            for food in foods:
                fish.findFood(food.foodPosition,food)
    
    if(len(foods) < MAXFOOD):
        if pygame.mouse.get_pressed()[0]:
            foods.append(Food(pygame.Vector2(pygame.mouse.get_pos()),screen))
        
    if(len(foods) > 0):
        for food in foods:
            food.draw()
                
    foods = [food for food in foods if not food.isEat]    
            
    for fish in fishs:
        if(fish.position.x > WIDTH):
            fish.position.x = 0
        elif(fish.position.x < 0):
             fish.position.x = WIDTH
        if(fish.position.y > HEIGHT):
            fish.position.y = 0
        elif(fish.position.y < 0):
              fish.position.y = HEIGHT

    
        
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, pygame.Color('white'))
    screen.blit(fps_text, (WIDTH - fps_text.get_width() - 10, 10))
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()