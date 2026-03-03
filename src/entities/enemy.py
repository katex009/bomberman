import random
import pygame
from utils.asset import load_image

pygame.init()


class Enemy:
    def __init__(self, grid_x, grid_y, tile_size=50):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size
        self.map_origin_x = 87
        self.map_origin_y = 168
        self.sprite_size = 32
        self.sprite_offset = (self.tile_size - self.sprite_size) // 2

        self.x = self.map_origin_x + self.grid_x * self.tile_size + self.sprite_offset
        self.y = self.map_origin_y + self.grid_y * self.tile_size + self.sprite_offset

        self.min_x = self.map_origin_x + self.sprite_offset
        self.max_x = self.map_origin_x + 16 * self.tile_size + self.sprite_offset
        self.min_y = self.map_origin_y + self.sprite_offset
        self.max_y = self.map_origin_y + 10 * self.tile_size + self.sprite_offset

        self.move_speed = 50
        self.is_moving = False
        self.dead = False
        self.dead_finished = False
        self.dead_animation_duration = 0.8
        self.dead_animation_elapsed = 0.0

        self.target_grid_x = self.grid_x
        self.target_grid_y = self.grid_y
        self.target_x = self.x
        self.target_y = self.y

        self.direction = "down"
        self.run_steps_remaining = random.randint(3, 7)
        self.animation_timer = 0.0
        self.animation_speed = 0.12
        self.frame = 0

        self.animacion = {
            "down": [
                load_image("images/enemies/enemy1.png", self.sprite_size),
                load_image("images/enemies/enemy2.png", self.sprite_size),
                load_image("images/enemies/enemy3.png", self.sprite_size),
            ],
            "up": [
                load_image("images/enemies/enemy1.png", self.sprite_size),
                load_image("images/enemies/enemy2.png", self.sprite_size),
                load_image("images/enemies/enemy3.png", self.sprite_size),
            ],
            "left": [
                load_image("images/enemies/enemy1.png", self.sprite_size),
                load_image("images/enemies/enemy2.png", self.sprite_size),
                load_image("images/enemies/enemy3.png", self.sprite_size),
            ],
            "right": [
                load_image("images/enemies/enemy1.png", self.sprite_size),
                load_image("images/enemies/enemy2.png", self.sprite_size),
                load_image("images/enemies/enemy3.png", self.sprite_size),
            ],
        }

        self.animacion_dead_enemy = [
            load_image("images/enemies/enemy-dead1.png", self.sprite_size),
            load_image("images/enemies/enemy-dead2.png", self.sprite_size),
            load_image("images/enemies/enemy-dead3.png", self.sprite_size),
            load_image("images/enemies/enemy-dead4.png", self.sprite_size),
        ]

        self.image = self.animacion[self.direction][self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def kill(self):
        if self.dead:
            return
        self.dead = True
        self.dead_animation_elapsed = 0.0
        self.frame = 0
        self.image = self.animacion_dead_enemy[self.frame]

    def _set_next_target(self, direction, map_ref=None, bomb_system=None):
        dx = 0
        dy = 0
        if direction == "up":
            dy = -1
        elif direction == "down":
            dy = 1
        elif direction == "left":
            dx = -1
        elif direction == "right":
            dx = 1

        next_grid_x = self.grid_x + dx
        next_grid_y = self.grid_y + dy
        next_x = self.map_origin_x + next_grid_x * self.tile_size + self.sprite_offset
        next_y = self.map_origin_y + next_grid_y * self.tile_size + self.sprite_offset

        if next_x < self.min_x or next_x > self.max_x or next_y < self.min_y or next_y > self.max_y:
            return False
        
        if map_ref and map_ref.is_blocked_with_bombs(next_grid_x, next_grid_y, bomb_system):
            return False

        self.target_grid_x = next_grid_x
        self.target_grid_y = next_grid_y
        self.target_x = next_x
        self.target_y = next_y
        self.direction = direction
        self.is_moving = True
        return True

    def _choose_new_direction(self, map_ref=None, bomb_system=None):
        directions = ["up", "down", "left", "right"]
        random.shuffle(directions)
        for direction in directions:
            if self._set_next_target(direction, map_ref, bomb_system):
                self.run_steps_remaining = random.randint(3, 7)
                return True
        self.is_moving = False
        self.run_steps_remaining = 1
        return False

    def update(self, dt, map_ref=None, bomb_system=None):
        if self.dead:
            self.dead_animation_elapsed = min(
                self.dead_animation_elapsed + dt,
                self.dead_animation_duration
            )
            frame_count = len(self.animacion_dead_enemy)
            progress = self.dead_animation_elapsed / self.dead_animation_duration
            dead_frame = min(int(progress * frame_count), frame_count - 1)
            self.image = self.animacion_dead_enemy[dead_frame]
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)
            if self.dead_animation_elapsed >= self.dead_animation_duration:
                self.dead_finished = True
            return

        if not self.is_moving:
            if self.run_steps_remaining > 0:
                if not self._set_next_target(self.direction, map_ref, bomb_system):
                    self._choose_new_direction(map_ref, bomb_system)
            else:
                if not self._choose_new_direction(map_ref, bomb_system):
                    directions = ["up", "down", "left", "right"]
                    for direction in directions:
                        if self._set_next_target(direction, map_ref, bomb_system):
                            self.run_steps_remaining = 1
                            break

        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = (dx * dx + dy * dy) ** 0.5

        if distance > 0:
            step = self.move_speed * dt
            if step >= distance:
                self.x = self.target_x
                self.y = self.target_y
                self.grid_x = self.target_grid_x
                self.grid_y = self.target_grid_y
                self.is_moving = False
                self.run_steps_remaining = max(0, self.run_steps_remaining - 1)
            else:
                self.x += (dx / distance) * step
                self.y += (dy / distance) * step
                
                current_grid_x = round((self.x - self.map_origin_x - self.sprite_offset) / self.tile_size)
                current_grid_y = round((self.y - self.map_origin_y - self.sprite_offset) / self.tile_size)
                self.grid_x = max(0, min(current_grid_x, 17))
                self.grid_y = max(0, min(current_grid_y, 10))

        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame = (self.frame + 1) % len(self.animacion[self.direction])
            self.image = self.animacion[self.direction][self.frame]

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
