import pygame
import random
from utils.asset import load_image
from entities.destructible_block import DestructibleBlock

pygame.init()

class Map:
    def __init__(self, width=1024, height=768, tile_size=50):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.map_origin_x = 87
        self.map_origin_y = 168
        
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
        self.indestructible_tile = load_image("images/mapa/pilar.png", tile_size)
        
        self.tiles_x = 17 
        self.tiles_y = 11 
        self.tiles_y_d = 12
        
        self.indestructible_blocks = []
        self._generate_indestructibles()
        
        self.destructible_blocks = []
        self._generate_destructibles()

    def _generate_indestructibles(self):
        for y in range(1, self.tiles_y, 2):
            for x in range(1, self.tiles_x, 2):
                self.indestructible_blocks.append((x, y))
    
    def _generate_destructibles(self):
        available_positions = []
        for y in range(self.tiles_y):
            for x in range(self.tiles_x):
                if (x, y) not in self.indestructible_blocks:
                    if not ((x == 0 and y == 0) or (x == 0 and y == 1) or (x == 1 and y == 0)):
                        available_positions.append((x, y))
        
        num_blocks = random.randint(89, 90)
        selected_positions = random.sample(available_positions, min(num_blocks, len(available_positions)))
        
        for x, y in selected_positions:
            self.destructible_blocks.append(DestructibleBlock(x, y))
    
    def is_indestructible(self, grid_x, grid_y):
        return (grid_x, grid_y) in self.indestructible_blocks
    
    def is_destructible(self, grid_x, grid_y):
        for block in self.destructible_blocks:
            if block.grid_x == grid_x and block.grid_y == grid_y and not block.destroyed and not block.being_destroyed:
                return True
        return False
    
    def is_blocked(self, grid_x, grid_y):
        return self.is_indestructible(grid_x, grid_y) or self.is_destructible(grid_x, grid_y)
    
    def is_blocked_with_bombs(self, grid_x, grid_y, bomb_system):
        if self.is_blocked(grid_x, grid_y):
            return True
        if bomb_system:
            for bomb in bomb_system.bombs:
                if bomb.grid_x == grid_x and bomb.grid_y == grid_y:
                    return True
        return False
            
    def draw(self, surface):
        
        surface.blit(self.wall_corner1_tile, (37, 128))
        surface.blit(self.wall_corner2_tile, (937, 128))


        for y in range(self.tiles_y_d):

            surface.blit(self.wall_left_dirt, (-10, 118 + y * self.tile_size))
            surface.blit(self.wall_rigth_dirt, (985, 118 + y * self.tile_size))

            surface.blit(self.wall_dirt, (-16, 718))
            surface.blit(self.wall_dirt, (992, 718))
            
        for x  in range(self.tiles_x):
            surface.blit(self.wall_top_tile, (87 + x * self.tile_size, 128))
            surface.blit(self.wall_bottom_tile, (83 + x * self.tile_size , 718))

        for y  in range(self.tiles_y):
            surface.blit(self.wall_left_tile, (37, 168 + y * self.tile_size))
            surface.blit(self.wall_rigth_tile, (937, 168 + y * self.tile_size))

            surface.blit(self.wall_corner4_tile, (34, 718))
            surface.blit(self.wall_corner3_tile, (932, 718))
                    
        for y  in range(self.tiles_y):
            for x  in range(self.tiles_x):
                surface.blit(self.grass_tile, (87 + x * self.tile_size, 168 + y * self.tile_size))
        
        for block in self.destructible_blocks:
            block.draw(surface)
        
        self.destructible_blocks = [block for block in self.destructible_blocks if not block.destroyed]
        
        for grid_x, grid_y in self.indestructible_blocks:
            surface.blit(self.indestructible_tile, (self.map_origin_x + grid_x * self.tile_size, self.map_origin_y + grid_y * self.tile_size))

        surface.blit(self.bar, (0, 0))
