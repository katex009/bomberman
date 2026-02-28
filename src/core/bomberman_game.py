from arcade_machine_sdk import GameBase
import pygame
from core.states.menu_state import menu_state
from core.states.play_state import play_state
from core.states.pause_state import pause_state
from core.states.game_over_state import game_over_state

pygame.init()

class BombermanGame(GameBase):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.bg_color = (30, 30, 30)
        self.state = None
        self.previous_state = None
        self.play_state_instance = None  

    def start(self, surface):
        super().start(surface)
        self.state = menu_state()
    
    def handle_events(self, events):
        
        next_state = self.state.handle_events(events)
        if next_state == "play":
            pygame.mixer.music.stop()
            self.play_state_instance = play_state()
            self.state = self.play_state_instance
        elif next_state == "pause":
            pygame.mixer.music.pause()
            self.previous_state = self.state
            self.state = pause_state(self.previous_state)
        elif next_state == "resume":
            pygame.mixer.music.unpause()
            self.state = self.previous_state
        elif next_state == "menu":
            pygame.mixer.music.stop()
            self.play_state_instance = None
            self.state = menu_state()
        elif next_state in ("game_over", "game over"):
            pygame.mixer.music.stop()
            self.state = game_over_state()
        elif next_state == "restart":
            pygame.mixer.music.stop()
            self.play_state_instance = play_state()
            self.state = self.play_state_instance


    def update(self, dt):
        self.state.update(dt)

    def render(self):
        self.state.render(self.surface)
        





