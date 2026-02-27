import pygame
from utils.asset import load_player_image

pygame.init()

class Player:
    def __init__(self, x=0, y=0):
        
        self.grid_x = x
        self.grid_y = y
        self.tile_size = 50
        
        self.x = self.grid_x * self.tile_size
        self.y = self.grid_y * self.tile_size
        
        self.target_x = self.x
        self.target_y = self.y
        self.move_speed = 200 
        
        self.direction = "frente"
        self.frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1
        self.is_moving = False

        self.remote_bombs_remaining = 0
        self.skull_curse_time = 0.0
        self.skull_speed_change_timer = 0.0
        self.skull_auto_bomb_cooldown = 0.0
        self.skull_last_bomb_tile = None
        self.skull_saved_speed = None

        self.animacion = {
            "frente": [
                load_player_image("player-frente.png", 50), 
                load_player_image("player-frente2.png", 50), 
                load_player_image("player-frente3.png", 50)],

            "atras": [
                load_player_image("player-atras.png", 50), 
                load_player_image("player-atras2.png", 50), 
                load_player_image("player-atras3.png", 50)],

            "izq": [
                load_player_image("player-lado-izq.png", 50), 
                load_player_image("player-lado-izq2.png", 50), 
                load_player_image("player-lado-izq3.png", 50)],

            "der": [
                load_player_image("player-lado-der.png", 50), 
                load_player_image("player-lado-der2.png", 50), 
                load_player_image("player-lado-der3.png", 50)]
        }
        
        self.image = self.animacion[self.direction][self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def move(self, dx, dy):
        self.grid_x += dx
        self.grid_y += dy
        self.target_x = self.grid_x * self.tile_size
        self.target_y = self.grid_y * self.tile_size
    
    def handle_events(self, events):
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return "place_bomb"  
        return None

    def update(self, dt):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.direction = "atras"
            self.y -= self.move_speed * dt
            self.is_moving = True
        elif keys[pygame.K_s]:
            self.direction = "frente"
            self.y += self.move_speed * dt
            self.is_moving = True
        elif keys[pygame.K_a]:
            self.direction = "izq"
            self.x -= self.move_speed * dt
            self.is_moving = True
        elif keys[pygame.K_d]:
            self.direction = "der"
            self.x += self.move_speed * dt
            self.is_moving = True
        else:
            self.is_moving = False
            self.frame = 0
        
        self.grid_x = round(self.x / self.tile_size)
        self.grid_y = round(self.y / self.tile_size)
        
        if self.is_moving:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.frame = (self.frame + 1) % 3
                self.animation_timer = 0
        
        self.rect.x = self.x
        self.rect.y = self.y
        self.image = self.animacion[self.direction][self.frame]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
