import pygame
from pathlib import Path

pygame.init()

class menu_state:
    def __init__(self):

        GAME_DIR = Path(__file__).resolve().parent 
        ASSETS_DIR = GAME_DIR.parents[1] / "assets" / "images" / "menu"
        MENU_IMAGE_PATH = ASSETS_DIR / "menu.png"

        self.background = pygame.image.load(str(MENU_IMAGE_PATH)).convert()
        self.rect = self.background.get_rect()

    def render(self, surface):
        surface.blit(self.background, self.rect)
