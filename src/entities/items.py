import pygame
from utils.asset import load_image

pygame.init()

class Item:
    def __init__(self, grid_x, grid_y, item_type="speed", tile_size=50):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size
        self.item_type = item_type
        
        self.x = self.grid_x * self.tile_size
        self.y = self.grid_y * self.tile_size
        
        self.collected = False
        
        if item_type == "speed":
            self.image = load_image("images/items/velocidad.png", 40)
        elif item_type == "fire":
            self.image = load_image("images/items/mas-bomba.png", 40)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x + 5
        self.rect.y = self.y + 5
    
    def check_collision(self, player):

        if self.grid_x == player.grid_x and self.grid_y == player.grid_y:
            if not self.collected:
                self.collected = True
                self.apply_effect(player)
                return True
        return False
    
    def apply_effect(self, player):
        if self.item_type == "speed":
            if not hasattr(player, 'speed_items_collected'):
                player.speed_items_collected = 0
            
            if player.speed_items_collected < 3:
                player.move_speed += 40
                player.speed_items_collected += 1
        
        elif self.item_type == "fire":
            if not hasattr(player, 'fire_range'):
                player.fire_range = 1
            
            if player.fire_range < 3:
                player.fire_range += 1
    
    def update(self, dt):
        pass
    
    def draw(self, surface):
        if not self.collected:
            surface.blit(self.image, self.rect)