import pygame
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
            fire_range = getattr(self.player, 'fire_range', 1)
            self.bomb_system.place_bomb(self.player.grid_x, self.player.grid_y, fire_range)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "pause"
        return None

    def update(self, dt):
        self.player.update(dt)
        self.bomb_system.update(dt)

    def render(self, surface):
        self.map.draw(surface)
        self.bomb_system.draw(surface)
        self.player.draw(surface)
