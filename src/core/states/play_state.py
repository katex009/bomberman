import pygame
import random
from pathlib import Path
from entities.player import Player
from entities.map import Map
from systems.bomb_system import BombSystem

pygame.init()

class play_state:

    def __init__(self):
        
        self.map = Map()
        self.player = Player(x=1, y=1)
        self.bomb_system = BombSystem()
        
        pygame.mixer.init()
        pygame.mixer.music.load(str(Path(__file__).resolve().parents[2] / "assets" / "sounds" / "juego.mp3"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def handle_events(self, events):
        action = self.player.handle_events(events)
        
        if action == "place_bomb":
            if self.player.skull_curse_time <= 0:
                fire_range = getattr(self.player, 'fire_range', 1)
                use_remote = self.player.remote_bombs_remaining > 0
                bomb_placed = self.bomb_system.place_bomb(
                    self.player.grid_x,
                    self.player.grid_y,
                    fire_range,
                    is_remote=use_remote
                )
                if bomb_placed and use_remote:
                    self.player.remote_bombs_remaining -= 1
                    self.player.remote_bombs_remaining = max(0, self.player.remote_bombs_remaining)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                has_remote_bombs_active = any(
                    bomb.is_remote and not bomb.exploded
                    for bomb in self.bomb_system.bombs
                )
                can_detonate_remote = (
                    self.player.remote_bombs_remaining > 0
                    or has_remote_bombs_active
                )
                if event.key == pygame.K_e and can_detonate_remote:
                    self.bomb_system.detonate_remote_bomb()
                if event.key == pygame.K_ESCAPE:
                    return "pause"
        return None

    def update(self, dt):

        if self.player.skull_curse_time > 0:
            self.bomb_system.max_bombs = 6
            self.player.skull_curse_time = max(0.0, self.player.skull_curse_time - dt)
            self.player.move_speed = random.randint(80, 500)

        else:
            self.bomb_system.max_bombs = self.bomb_system.base_max_bombs

        if self.player.skull_curse_time > 0 and self.player.is_moving:
            current_tile = (self.player.grid_x, self.player.grid_y)

            if self.player.skull_last_bomb_tile != current_tile:
                if random.random() < 0.5:

                    fire_range = getattr(self.player, 'fire_range', 1)
                    self.bomb_system.place_bomb(
                        self.player.grid_x,
                        self.player.grid_y,
                        fire_range,
                        is_remote=False)
                    
                self.player.skull_last_bomb_tile = current_tile

        if self.player.skull_curse_time <= 0 and self.player.skull_saved_speed is not None:
            self.player.move_speed = self.player.skull_saved_speed
            self.player.skull_saved_speed = None

        #lo demas
        self.player.update(dt)
        self.bomb_system.update(dt)

    def render(self, surface):
        self.map.draw(surface)
        self.bomb_system.draw(surface)
        self.player.draw(surface)
