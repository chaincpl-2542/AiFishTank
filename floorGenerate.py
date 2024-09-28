import pygame

class Floor:
    def __init__(self,screen):
        self.bgPosition = pygame.Vector2(100,100)
        self.screen = screen
        
        self.frame_size = 512
        self.fx = 0
        self.fy = 0
        
        self.bg_sprite = pygame.image.load("./assets/BG_Grass512.png")
        self.agent_frame = self.bg_sprite.subsurface(pygame.Rect( self.fx * self.frame_size, self.fy * self.frame_size,
                                                                    self.frame_size,
                                                                    self.frame_size))
    
    def draw(self,x,y):
        # self.screen.blit(self.agent_frame, self.bgPosition - pygame.Vector2(64, 64)  )
        self.screen.blit(self.agent_frame,(x,y))
        
    