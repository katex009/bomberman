import pygame
from utils.asset import load_image

pygame.init()

class Bomb:

    def __init__(self, grid_x, grid_y, tile_size=50, is_remote=False):

        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size
        
        self.x = self.grid_x * self.tile_size
        self.y = self.grid_y * self.tile_size
        
        self.timer = 3.0  
        self.exploded = False
        self.is_remote = is_remote
        
        self.frames = [
            load_image("images/bomb/bomba.png", 28),
            load_image("images/bomb/bomba2.png", 28),
            load_image("images/bomb/bomba3.png", 28)
        ]

        self.frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.3
        
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update(self, dt):
        self.animation_timer += dt

        if self.animation_timer >= self.animation_speed:
            self.frame = (self.frame + 1) % 3
            self.animation_timer = 0
            self.image = self.frames[self.frame]
        
        if not self.is_remote:
            self.timer -= dt
            if self.timer <= 0:
                self.exploded = True
    
    def draw(self, surface):
        
        if not self.exploded:
            surface.blit(self.image, self.rect) 
