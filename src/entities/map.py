import pygame
from utils.asset import load_image

pygame.init()

import pygame
from utils.asset import load_image

pygame.init()

class Map:
    def __init__(self, width=1024, height=768, tile_size=50):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        
        self.grass_tile = load_image("images/mapa/cesped.png", tile_size)
        self.wall_left_tile = load_image("images/mapa/pared-izq1.png", tile_size)
        self.wall_rigth_tile = load_image("images/mapa/pared-der1.png", tile_size)
        self.wall_top_tile = load_image("images/mapa/pared-sup.png", tile_size)
        self.wall_bottom_tile = load_image("images/mapa/pared-inf.png", 60)

        self.wall_left_dirt = load_image("images/mapa/pared-tierra-izq.png", tile_size)
        self.wall_rigth_dirt = load_image("images/mapa/pared-tierra-der.png", tile_size)
        self.wall_dirt = load_image("images/mapa/pared-tierra.png", tile_size)
        
        self.wall_corner1_tile = load_image("images/mapa/esquina-sup-izq.png", tile_size)
        self.wall_corner2_tile = load_image("images/mapa/esquina-sup-der.png", tile_size)
        self.wall_corner3_tile = load_image("images/mapa/pared-inf.png", 60)
        self.wall_corner4_tile = load_image("images/mapa/pared-inf.png", 60)

        self.bar = load_image("images/mapa/barra.png")
        
        self.tiles_x = 18 
        self.tiles_y = 11 
        self.tiles_y_d = 12 
    
    def draw(self, surface):
        
        surface.blit(self.wall_corner1_tile, (12, 128))
        surface.blit(self.wall_corner2_tile, (962, 128))
        
        

        for y in range(self.tiles_y_d):

            surface.blit(self.wall_left_dirt, (-35, 118 + y * self.tile_size))
            surface.blit(self.wall_rigth_dirt, (1010, 118 + y * self.tile_size))

            surface.blit(self.wall_dirt, (-41, 718))
            surface.blit(self.wall_dirt, (1017, 718))
            
        for x  in range(self.tiles_x):
            surface.blit(self.wall_top_tile, (62 + x * self.tile_size, 128))
            surface.blit(self.wall_bottom_tile, (58 + x * self.tile_size , 718))

        for y  in range(self.tiles_y):
            surface.blit(self.wall_left_tile, (12, 168 + y * self.tile_size))
            surface.blit(self.wall_rigth_tile, (962, 168 + y * self.tile_size))

            surface.blit(self.wall_corner4_tile, (9, 718))
            surface.blit(self.wall_corner3_tile, (957, 718))
                    
        for y  in range(self.tiles_y):
            for x  in range(self.tiles_x):
                surface.blit(self.grass_tile, (62 + x * self.tile_size, 168 + y * self.tile_size))

        surface.blit(self.bar, (0, 0))
