import pygame

pygame.init()

class play_state:

    def __init__(self):
        pass

    def start(self):
        print("PlayState iniciado")

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def render(self, surface):
        surface.fill((20, 20, 60))
        font = pygame.font.Font(None, 74)
        text = font.render("PLAYING", True, (255, 255, 255))
        surface.blit(text, (300, 250))