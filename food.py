import pygame


class Food:
    def __init__(self,foodPosition,screen):
        self.foodPosition = pygame.Vector2(foodPosition.x,foodPosition.y)
        self.isEat = False
        self.screen = screen
        
    def draw(self):
        pygame.draw.circle(self.screen,"brown",self.foodPosition,5)
        
    def eaten(self):
        self.isEat = True