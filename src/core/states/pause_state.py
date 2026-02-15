import pygame
from pathlib import Path

pygame.init()

class pause_state:
    
    def __init__(self, previous_state):
        self.previous_state = previous_state

        GAME_DIR = Path(__file__).resolve().parent 
        ASSETS_DIR = GAME_DIR.parents[1] / "assets" / "images" / "pause"

        self.pause = pygame.image.load(str(ASSETS_DIR/ "pause.png")).convert_alpha()
        self.pause_rect = self.pause.get_rect()

        self.pause_rect.x = 277.5
        self.pause_rect.y = 98.5
        
        self.resume = pygame.image.load(str(ASSETS_DIR/ "resume.png")).convert_alpha()
        self.resume_rect = self.resume.get_rect()

        self.resume_rect.x = 421
        self.resume_rect.y = 321.9

        self.resume2 = pygame.image.load(str(ASSETS_DIR / "resume2.png")).convert_alpha()
        self.actual_resume = self.resume

        self.main_menu = pygame.image.load(str(ASSETS_DIR/ "main-menu.png")).convert_alpha()
        self.main_menu_rect = self.main_menu.get_rect()

        self.main_menu_rect.x = 382.9
        self.main_menu_rect.y = 454.7

        self.main_menu2 = pygame.image.load(str(ASSETS_DIR / "main-menu2.png")).convert_alpha()
        self.actual_main_menu = self.main_menu

        self.linea = pygame.image.load(str(ASSETS_DIR/ "linea.png")).convert_alpha()
        self.linea_rect = self.linea.get_rect()

    def render(self, surface):
        self.previous_state.render(surface)

        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  
        surface.blit(overlay, (0, 0))

        surface.blit(self.pause, self.pause_rect)
        surface.blit(self.linea, self.linea_rect)
        surface.blit(self.actual_resume, self.resume_rect)
        surface.blit(self.actual_main_menu, self.main_menu_rect)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"
                
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    if self.resume_rect.collidepoint(event.pos):
                        return "play"
                    
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    if self.main_menu_rect.collidepoint(event.pos):
                        return "menu"
        return None

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()

        if self.resume_rect.collidepoint(mouse_pos):
            self.actual_resume = self.resume2
        else:
            self.actual_resume = self.resume

        if self.main_menu_rect.collidepoint(mouse_pos):
            self.actual_main_menu = self.main_menu2
        else:
            self.actual_main_menu = self.main_menu

    

