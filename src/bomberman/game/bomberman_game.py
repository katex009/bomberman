from arcade_machine_sdk import GameBase
import pygame
from bomberman.entities.player import Player
from bomberman.game.states.menu_state import menu_state
from bomberman.game.states.play_state import play_state




class BombermanGame(GameBase):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.bg_color = (30, 30, 30)
        self.state = None

    def start(self, surface):
        super().start(surface)
        self.state = menu_state()
        self.player = Player()
    
    def handle_events(self, events):
        next_state = self.state.handle_events(events)
        if next_state == "play":
            self.state = play_state()
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.stop()

    def update(self, dt):
        self.state.update(dt)

    def render(self):
        self.state.render(self.surface)
        





