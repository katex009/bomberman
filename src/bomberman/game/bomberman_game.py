from arcade_machine_sdk import GameBase
import pygame
from bomberman.entities.player import Player




class BombermanGame(GameBase):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.bg_color = (30, 30, 30)

    def start(self, surface):
        super().start(surface)
        self.player = Player()
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.stop()

    def update(self, dt):
        self.player.update(dt)

    def render(self):
        self.surface.fill(self.bg_color)
        self.player.draw(self.surface)





