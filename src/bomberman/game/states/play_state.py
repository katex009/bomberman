import pygame

pygame.init()

class play_state:

    def __init__(self):
        pass

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