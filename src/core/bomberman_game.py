from arcade_machine_sdk import GameBase
import pygame
from entities.player import Player
from core.states.menu_state import menu_state
from core.states.play_state import play_state
from core.states.pause_state import pause_state

pygame.init()

class BombermanGame(GameBase):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.bg_color = (30, 30, 30)
        self.state = None
        self.previous_state = None

    def start(self, surface):
        super().start(surface)
        self.state = menu_state()
        self.player = Player()
    
    def handle_events(self, events):
        next_state = self.state.handle_events(events)
        if next_state == "play":
            self.state = play_state()
        elif next_state == "pause":
            self.previous_state = self.state
            self.state = pause_state(self.previous_state)
        elif next_state == "resume":
            self.state = self.previous_state
        elif next_state == "menu":
            self.state = menu_state()


    def update(self, dt):
        self.state.update(dt)

    def render(self):
        self.state.render(self.surface)
        





