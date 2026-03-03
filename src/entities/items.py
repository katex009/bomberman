import pygame
from utils.asset import load_image

pygame.init()

class Item:
    def __init__(self, grid_x, grid_y, item_type="speed", tile_size=50):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size
        self.item_type = item_type
        self.map_origin_x = 87
        self.map_origin_y = 168
        
        self.x = self.map_origin_x + self.grid_x * self.tile_size
        self.y = self.map_origin_y + self.grid_y * self.tile_size
        
        self.collected = False
        
        if item_type == "speed":
            self.image = load_image("images/items/velocidad.png", 40)
        elif item_type == "fire":
            self.image = load_image("images/items/flama.png", 40)
        elif item_type == "slow":
            self.image = load_image("images/items/sandalia.png", 40)
        elif item_type == "remote":
            self.image = load_image("images/items/control-remoto.png", 40)
        elif item_type == "calavera":
            self.image = load_image("images/items/calavera.png", 40)
        elif item_type == "perforadora":
            self.image = load_image("images/items/bomba-perforadora.png", 40)
        elif item_type == "mas_bomba":
            self.image = load_image("images/items/mas-bomba.png", 40)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x + 5
        self.rect.y = self.y + 5
    
    def check_collision(self, player, score_system=None):

        if self.grid_x == player.grid_x and self.grid_y == player.grid_y:
            if not self.collected:
                self.collected = True
                self.apply_effect(player)
                if score_system:
                    score_system.add_item_collected()
                return True
        return False
    
    def apply_effect(self, player):

        if self.item_type == "speed":
            if not hasattr(player, 'speed_items_collected'):
                player.speed_items_collected = 0
            
            if player.speed_items_collected < 4:
                player.move_speed += 30
                player.speed_items_collected += 1
        
        elif self.item_type == "fire":
            if not hasattr(player, 'fire_range'):
                player.fire_range = 1
            
            if player.fire_range < 3:
                player.fire_range += 1

        elif self.item_type == "slow":
            if not hasattr(player, 'slow_items_collected'):
                player.slow_items_collected = 0
            
            if player.slow_items_collected < 3:
                player.move_speed -= 60
                player.slow_items_collected += 1

        elif self.item_type == "remote":
            player.remote_bombs_remaining += 3

        elif self.item_type == "calavera":
            if player.skull_saved_speed is None:
                player.skull_saved_speed = player.move_speed
            player.skull_curse_time = max(player.skull_curse_time, 15)
            player.skull_speed_change_timer = 0.0
            player.skull_auto_bomb_cooldown = 0.0
            player.skull_last_bomb_tile = None
        
        elif self.item_type == "perforadora":
            player.has_piercing_bombs = True
            player.piercing_bomb_time = 15.0
        
        elif self.item_type == "mas_bomba":
            player.extra_bombs = min(player.extra_bombs + 1, 7)

        
    
    def update(self, dt):
        pass
    
    def draw(self, surface):
        if not self.collected:
            surface.blit(self.image, self.rect)
