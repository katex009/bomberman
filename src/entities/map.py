import pygame
from utils.asset import load_image

pygame.init()

class Map:
    def __init__(self, width=1024, height=768, tile_size=50):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        
        self.grass_tile = load_image("images/mapa/cesped.png", tile_size)
        
        self.tiles_x = width // tile_size + 1
        self.tiles_y = height // tile_size + 1
    
    def draw(self, surface):
        
        for y in range(self.tiles_y):
            for x in range(self.tiles_x):
                surface.blit(self.grass_tile, (x * self.tile_size, y * self.tile_size))
