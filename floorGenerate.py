import pygame

class Floor:
    def __init__(self,screen):
        self.bgPosition = pygame.Vector2(100,100)
        self.screen = screen
        
        self.frame_size = 128
        self.fx = 0
        self.fy = 0
        
        self.bg_sprite = pygame.image.load("./assets/BG_Grass.png")
        self.agent_frame = self.bg_sprite.subsurface(pygame.Rect( self.fx * self.frame_size, self.fy * self.frame_size,
                                                                    self.frame_size,
                                                                    self.frame_size))
    
    def draw(self,x,y,tile_Size):
        # self.screen.blit(self.agent_frame, self.bgPosition - pygame.Vector2(64, 64)  )
        self.screen.blit(self.agent_frame,(x * tile_Size, y * tile_Size))
        
    