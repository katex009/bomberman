import pygame
from utils.asset import load_image, load_sound

pygame.init()

class Bomb:

    def __init__(self, grid_x, grid_y, tile_size=50, is_remote=False):

        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size
        self.map_origin_x = 87
        self.map_origin_y = 168
        self.sprite_size = 28
        
        offset = (self.tile_size - self.sprite_size) // 2
        self.x = self.map_origin_x + self.grid_x * self.tile_size + offset
        self.y = self.map_origin_y + self.grid_y * self.tile_size + offset
        
        self.timer = 3.0  
        self.exploded = False
        self.is_remote = is_remote

        self.bomb_sound = load_sound("sounds/colocar-bomba.mp3", 0.3)
        self.bomb_exp_spund = load_sound("sounds/bomba-explota.mp3", 0.5)
        self.explosion_sound_played = False
        self.bomb_sound.play()
        
        self.frames = [
            load_image("images/bomb/bomba.png", self.sprite_size),
            load_image("images/bomb/bomba2.png", self.sprite_size),
            load_image("images/bomb/bomba3.png", self.sprite_size)
        ]

        self.bomba_perforadora = [
            load_image("images/bomb/bomba_perforadora1.png", self.sprite_size),
            load_image("images/bomb/bomba_perforadora2.png", self.sprite_size),
            load_image("images/bomb/bomba_perforadora3.png", self.sprite_size)
        ]

        self.frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.3
        
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
    
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

        if self.exploded and not self.explosion_sound_played:
            self.bomb_exp_spund.play()
            self.explosion_sound_played = True
    
    def draw(self, surface):
        
        if not self.exploded:
            surface.blit(self.image, self.rect) 
