import random
import pygame
from utils.asset import load_image

pygame.init()


class Enemy:
    def __init__(self, grid_x, grid_y, tile_size=32):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size

        self.x = 62 + self.grid_x * self.tile_size
        self.y = 156 + self.grid_y * self.tile_size

        self.min_x = 62
        self.max_x = 62 + 17 * self.tile_size
        self.min_y = 156
        self.max_y = 156 + 10 * self.tile_size

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
                load_image("images/enemies/enemy1.png", 32),
                load_image("images/enemies/enemy2.png", 32),
                load_image("images/enemies/enemy3.png", 32),
            ],
            "up": [
                load_image("images/enemies/enemy1.png", 32),
                load_image("images/enemies/enemy2.png", 32),
                load_image("images/enemies/enemy3.png", 32),
            ],
            "left": [
                load_image("images/enemies/enemy1.png", 32),
                load_image("images/enemies/enemy2.png", 32),
                load_image("images/enemies/enemy3.png", 32),
            ],
            "right": [
                load_image("images/enemies/enemy1.png", 32),
                load_image("images/enemies/enemy2.png", 32),
                load_image("images/enemies/enemy3.png", 32),
            ],
        }

        self.animacion_dead_enemy = [
            load_image("images/enemies/enemy-dead1.png", 32),
            load_image("images/enemies/enemy-dead2.png", 32),
            load_image("images/enemies/enemy-dead3.png", 32),
            load_image("images/enemies/enemy-dead4.png", 32),
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

    def _set_next_target(self, direction):
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

        next_x = 62 + (self.grid_x + dx) * self.tile_size
        next_y = 156 + (self.grid_y + dy) * self.tile_size

        if next_x < self.min_x or next_x > self.max_x or next_y < self.min_y or next_y > self.max_y:
            return False

        self.target_grid_x = self.grid_x + dx
        self.target_grid_y = self.grid_y + dy
        self.target_x = next_x
        self.target_y = next_y
        self.direction = direction
        self.is_moving = True
        return True

    def _choose_new_direction(self):
        directions = ["up", "down", "left", "right"]
        random.shuffle(directions)
        for direction in directions:
            if self._set_next_target(direction):
                self.run_steps_remaining = random.randint(3, 7)
                return
        self.is_moving = False

    def update(self, dt):
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
            if self.run_steps_remaining > 0 and self._set_next_target(self.direction):
                pass
            else:
                self._choose_new_direction()

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

        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame = (self.frame + 1) % len(self.animacion[self.direction])
            self.image = self.animacion[self.direction][self.frame]

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
