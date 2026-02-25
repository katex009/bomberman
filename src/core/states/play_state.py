import pygame
from pathlib import Path

pygame.init()

class play_state:

    def __init__(self):

        GAME_DIR = Path(__file__).resolve().parent 
        SOUNDS_DIR = GAME_DIR.parents[1] / "assets" / "sounds"

        self.play_music = SOUNDS_DIR / "juego.mp3"

        pygame.mixer.init()
        pygame.mixer.music.load(str(self.play_music))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)


    def start(self):
        print("PlayState iniciado")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "pause"
        return None

    def update(self, dt):
        pass

    def render(self, surface):

        surface.fill((40, 70, 30))
        font = pygame.font.Font(None, 74)
        text = font.render("PLAYING", True, (255, 255, 255))
        surface.blit(text, (300, 250))