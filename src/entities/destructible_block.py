import pygame
import random
from utils.asset import load_image

pygame.init()

class DestructibleBlock:
    
    ITEM_PROBABILITIES = {
        "speed": 0.06,      
        "fire": 0.1,       
        "slow": 0.05,       
        "remote": 0.03,     
        "calavera": 0.02,   
        "perforadora": 0.03,
        "mas_bomba": 0.1,
        "none": 0.62        
    }
    
    def __init__(self, grid_x, grid_y, tile_size=50):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size
        self.map_origin_x = 87
        self.map_origin_y = 168
        
        self.x = self.map_origin_x + self.grid_x * self.tile_size
        self.y = self.map_origin_y + self.grid_y * self.tile_size
        
        self.destroyed = False
        self.being_destroyed = False
        self.destruction_timer = 0.0
        self.destruction_duration = 0.4
        
        self.block_image = load_image("images/mapa/bloque.png", tile_size)
        self.destruction_frames = [
            load_image("images/mapa/bloque-destruido1.png", tile_size),
            load_image("images/mapa/bloque-destruido2.png", tile_size),
            load_image("images/mapa/bloque-destruido3.png", tile_size),
            load_image("images/mapa/bloque-destruido4.png", tile_size),
            load_image("images/mapa/bloque-destruido5.png", tile_size),
            load_image("images/mapa/bloque-destruido6.png", tile_size),
            load_image("images/mapa/bloque-destruido7.png", tile_size)
        ]
        
        self.current_image = self.block_image
        self.rect = pygame.Rect(self.x, self.y, tile_size, tile_size)
        
        self.item_type = self._determine_item()
        self.item_dropped = False
        self.score_given = False
    
    def _determine_item(self):
        rand = random.random()
        cumulative = 0.0
        for item_type, probability in self.ITEM_PROBABILITIES.items():
            cumulative += probability
            if rand <= cumulative:
                return item_type if item_type != "none" else None
        return None
    
    def destroy(self):
        if not self.destroyed and not self.being_destroyed:
            self.being_destroyed = True
            self.destruction_timer = 0.0
    
    def update(self, dt):
        if self.being_destroyed:
            self.destruction_timer += dt
            progress = self.destruction_timer / self.destruction_duration
            
            if progress >= 1.0:
                self.destroyed = True
                self.being_destroyed = False
            else:
                frame_index = min(int(progress * len(self.destruction_frames)), len(self.destruction_frames) - 1)
                self.current_image = self.destruction_frames[frame_index]
    
    def draw(self, surface):
        if not self.destroyed:
            surface.blit(self.current_image, (self.x, self.y))
