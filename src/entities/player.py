import pygame
from utils.asset import load_player_image, load_image

pygame.init()

class Player:
    def __init__(self, x=0, y=0):

        self.grid_x =x
        self.grid_y =y
        self.tile_size = 50
        
        self.x = 62 + self.grid_x * self.tile_size
        self.y = 156 + self.grid_y * self.tile_size
        
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
        
        self.animacion_dead_bomb = [
            load_image("images/player_dead/player-dead1.png", 50),
            load_image("images/player_dead/player-dead2.png", 50),
            load_image("images/player_dead/player-dead3.png", 50),
            load_image("images/player_dead/player-dead4.png", 50),
            load_image("images/player_dead/player-dead6.png", 50),
            load_image("images/player_dead/player-dead7.png", 50),
            load_image("images/player_dead/player-dead8.png", 50),
            load_image("images/player_dead/player-dead9.png", 50),
            load_image("images/player_dead/player-dead10.png", 50),
            load_image("images/player_dead/player-dead11.png", 50)
        ]

        self.animacion_dead_normal = [
            load_image("images/player_dead/player-dead-nor.png", 50),
            load_image("images/player_dead/player-dead-nor2.png", (50, 55)),
            load_image("images/player_dead/player-dead-nor5.png", (50, 66)),
            load_image("images/player_dead/player-dead-nor6.png", (50, 66)),
            load_image("images/player_dead/player-dead-nor3.png", 50),
            load_image("images/player_dead/player-dead-nor4.png", 50),
            load_image("images/player_dead/player-dead-nor3.png", 50),
            load_image("images/player_dead/player-dead-nor4.png", 50),
            load_image("images/player_dead/player-dead-nor3.png", 50),
            load_image("images/player_dead/player-dead-nor4.png", 50)
        ]

        self.image_dead = self.animacion_dead_bomb[self.frame]
        self.image = self.animacion[self.direction][self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.player_dead = False
        self.dead_type = "bomb"
        self.dead_animation_duration = 2.0
        self.dead_animation_elapsed = 0.0

    def _get_dead_animation(self):
        if self.dead_type == "normal":
            return self.animacion_dead_normal
        return self.animacion_dead_bomb

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

    def update(self, dt, is_dead=False, death_type="bomb"):
        if is_dead:
            if not self.player_dead:
                self.player_dead = True
                self.dead_type = death_type
                self.frame = 0
                self.dead_animation_elapsed = 0.0
                dead_animation = self._get_dead_animation()
                self.image_dead = dead_animation[self.frame]

            dead_animation = self._get_dead_animation()
            self.dead_animation_elapsed = min(
                self.dead_animation_elapsed + dt,
                self.dead_animation_duration
            )
            dead_frames = len(dead_animation)
            progress = self.dead_animation_elapsed / self.dead_animation_duration
            dead_frame = min(int(progress * dead_frames), dead_frames - 1)
            self.frame = dead_frame
            self.image_dead = dead_animation[self.frame]

            self.rect.x = self.x
            self.rect.y = self.y
            return

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
            
        ###########################LIMITACION DE BORDES
        if self.y<156:
            self.y=156
        if self.y>(156+10*50):
            self.y=(156+10*50)
        if self.x<62:
            self.x=62
        if self.x>(62+17*50):
            self.x=(62+17*50)

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
        if self.player_dead:
            surface.blit(self.image_dead, self.rect)
        else:
            surface.blit(self.image, self.rect)
