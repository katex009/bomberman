import pygame
from utils.asset import load_image

pygame.init()

class Explosion:
    def __init__(self, grid_x, grid_y, direction="center", tile_size=50):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size
        self.direction = direction
        
        self.x = self.grid_x * self.tile_size
        self.y = self.grid_y * self.tile_size
        
        self.timer = 0.5  
        self.finished = False
        
        if direction == "center":
            self.frames = [
                load_image("images/bomb/fire-centro1.png", 50),
                load_image("images/bomb/fire-centro2.png", 50),
                load_image("images/bomb/fire-centro3.png", 50),
                load_image("images/bomb/fire-centro4.png", 50),
            ]
        elif direction == "up":
            self.frames = [
                load_image("images/bomb/fire-punta1.png", 50),
                load_image("images/bomb/fire-punta2.png", 50),
                load_image("images/bomb/fire-punta3.png", 50),
                load_image("images/bomb/fire-punta4.png", 50),
            ]
        elif direction == "down":
            self.frames = [
                load_image("images/bomb/fire-punta-abajo1.png", 50),
                load_image("images/bomb/fire-punta-abajo2.png", 50),
                load_image("images/bomb/fire-punta-abajo3.png", 50),
                load_image("images/bomb/fire-punta-abajo4.png", 50),
            ]
        elif direction == "left":
            self.frames = [
                load_image("images/bomb/fire-punta-izq1.png", 50),
                load_image("images/bomb/fire-punta-izq2.png", 50),
                load_image("images/bomb/fire-punta-izq3.png", 50),
                load_image("images/bomb/fire-punta-izq4.png", 50),
            ]
        elif direction == "right":
            self.frames = [
                load_image("images/bomb/fire-punta-der1.png", 50),
                load_image("images/bomb/fire-punta-der2.png", 50),
                load_image("images/bomb/fire-punta-der3.png", 50),
                load_image("images/bomb/fire-punta-der4.png", 50),
            ]
        elif direction == "middle_vertical":
            self.frames = [
                load_image("images/bomb/fire-medio-ver1.png", 50),
                load_image("images/bomb/fire-medio-ver2.png", 50),
                load_image("images/bomb/fire-medio-ver3.png", 50),
                load_image("images/bomb/fire-medio-ver4.png", 50),
            ]
        elif direction == "middle_horizontal":
            self.frames = [
                load_image("images/bomb/fire-medio-hor1.png", 50),
                load_image("images/bomb/fire-medio-hor2.png", 50),
                load_image("images/bomb/fire-medio-hor3.png", 50),
                load_image("images/bomb/fire-medio-hor4.png", 50),
            ]
        
        self.frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1
        
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update(self, dt):
        self.timer -= dt
        
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.frame = (self.frame + 1) % 4
            self.animation_timer = 0
            self.image = self.frames[self.frame]
        
        if self.timer <= 0:
            self.finished = True
    
    def draw(self, surface):
        if not self.finished:
            surface.blit(self.image, self.rect)
