import pygame

shadow_radius = 10
class Food:
    def __init__(self,foodPosition,screen):
        self.foodPosition = pygame.Vector2(foodPosition.x,foodPosition.y)
        self.isEat = False
        self.screen = screen
        
        self.frame_size = 32
        self.fx = 0
        self.fy = 0
        self.time = 0
        self.animation_frame_rate = 3
        
        self.food_sprite = pygame.image.load("./assets/Grass.png")
        self.agent_frame = self.food_sprite.subsurface(pygame.Rect( self.fx * self.frame_size, self.fy * self.frame_size,
                                                                    self.frame_size,
                                                                    self.frame_size))
                
        
    def draw(self):
        
        shadow_surface = pygame.Surface((shadow_radius * 2, shadow_radius), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 100), (0, 0, shadow_radius * 2, shadow_radius))
        shadow_pos = (self.foodPosition.x - 10, self.foodPosition.y + 8)
        self.screen.blit(shadow_surface, shadow_pos)
        
        self.screen.blit(self.agent_frame, self.foodPosition - pygame.Vector2(16, 16)  )
        # pygame.draw.circle(self.screen,"brown",self.foodPosition,5)
        
    def eaten(self):
        self.isEat = True
        
    def update_animation(self):
        if self.time > self.animation_frame_rate:
            self.fx = self.fx + 1
            self.fx = self.fx%4
            
            self.agent_frame = self.food_sprite.subsurface(pygame.Rect( self.fx * self.frame_size, 
                                                    self.fy * self.frame_size,
                                                    self.frame_size,
                                                    self.frame_size))
            
            self.time = 0
        else:
            self.time = self.time + 1