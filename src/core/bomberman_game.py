from arcade_machine_sdk import GameBase
import pygame
from core.states.menu_state import menu_state
from core.states.play_state import play_state
from core.states.pause_state import pause_state
from core.states.game_over_state import game_over_state
from core.states.final_state import final_state
from core.states.controles_state import controls_state
from core.states.options_state import options_state
from core.states.volume_state import volume_state

pygame.init()


class BombermanGame(GameBase):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.bg_color = (30, 30, 30)
        self.state = None
        self.previous_state = None
        self.play_state_instance = None
        self.pause_state_instance = None

    def start(self, surface):
        super().start(surface)
        self.state = menu_state(self)

    def handle_events(self, events):

        next_state = self.state.handle_events(events)
        if next_state == "play":
            pygame.mixer.music.stop()
            self.play_state_instance = play_state()
            self.state = self.play_state_instance
        elif next_state == "options":
            if isinstance(self.state, pause_state):
                self.previous_state = self.state
            self.state = options_state()
        elif next_state == "controls":
            if isinstance(self.state, options_state) and self.pause_state_instance:
                pass
            self.state = controls_state()
        elif next_state == "volume":
            if isinstance(self.state, options_state) and self.pause_state_instance:
                pass
            self.state = volume_state()
        elif next_state == "pause":
            pygame.mixer.music.pause()
            self.previous_state = self.state
            self.pause_state_instance = pause_state(self.previous_state)
            self.state = self.pause_state_instance
        elif next_state == "resume":
            pygame.mixer.music.unpause()
            if self.pause_state_instance:
                self.state = self.pause_state_instance.previous_state
            else:
                self.state = self.previous_state
            self.pause_state_instance = None
        elif next_state == "menu":
            if self.pause_state_instance and (isinstance(self.state, options_state) or isinstance(self.state, controls_state) or isinstance(self.state, volume_state)):
                self.state = self.pause_state_instance
            else:
                pygame.mixer.music.stop()
                self.play_state_instance = None
                self.pause_state_instance = None
                self.state = menu_state(self)
        elif next_state in ("game_over", "game over"):
            pygame.mixer.music.stop()
            self.state = game_over_state()
        elif next_state == "final":
            pygame.mixer.music.stop()
            score_system = self.play_state_instance.score_system if self.play_state_instance else None
            self.state = final_state(score_system)
        elif next_state == "restart":
            pygame.mixer.music.stop()
            self.play_state_instance = play_state()
            self.state = self.play_state_instance

    def update(self, dt):
        self.state.update(dt)

    def render(self):
        self.state.render(self.surface)
