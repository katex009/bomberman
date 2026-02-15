import pygame
from pathlib import Path

pygame.init()

class menu_state:
    
    def __init__(self):

        GAME_DIR = Path(__file__).resolve().parent 
        ASSETS_DIR = GAME_DIR.parents[1] / "assets" / "images" / "menu"

        self.background = pygame.image.load(str(ASSETS_DIR/ "menu.png")).convert()
        self.rect = self.background.get_rect()

        self.start_image = pygame.image.load(str(ASSETS_DIR / "start.png")).convert()
        self.start_rect = self.start_image.get_rect()

        self.start_rect.x = 436.3
        self.start_rect.y = 476.5

        self.start_image2 = pygame.image.load(str(ASSETS_DIR / "start2.png")).convert()
        self.actual_start_image = self.start_image

        self.exit_image = pygame.image.load(str(ASSETS_DIR / "exit.png")).convert()
        self.exit_rect = self.exit_image.get_rect()

        self.exit_rect.x = 438.3
        self.exit_rect.y = 564

        self.exit_image2 = pygame.image.load(str(ASSETS_DIR / "exit2.png")).convert()
        self.actual_exit_image = self.exit_image

    def render(self, surface):
        surface.blit(self.background, self.rect)
        surface.blit(self.actual_start_image, self.start_rect)
        surface.blit(self.actual_exit_image, self.exit_rect)


    def update(self, dt):
        if pygame.get_init():
            mouse_pos = pygame.mouse.get_pos()

            if self.start_rect.collidepoint(mouse_pos):
                self.actual_start_image = self.start_image2
            else:
                self.actual_start_image = self.start_image

            if self.exit_rect.collidepoint(mouse_pos):
                self.actual_exit_image = self.exit_image2
            else:
                self.actual_exit_image = self.exit_image

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    if self.start_rect.collidepoint(event.pos):
                        return "play"
            
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    if self.exit_rect.collidepoint(event.pos):
                        pygame.quit()
        return None
