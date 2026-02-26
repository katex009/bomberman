import pygame
from utils.asset import load_image, load_sound

pygame.init()

class pause_state:
    
    def __init__(self, previous_state):
        self.previous_state = previous_state

        self.boton_sound = load_sound("sounds/sonido-letras.mp3", volume = 0.5)
        self.hover_played = {"resume": False, "main_menu": False}

        self.pause = load_image("images/pause/pause.png")
        self.pause_rect = self.pause.get_rect()

        self.pause_rect.x = 277.5
        self.pause_rect.y = 98.5
        
        self.resume = load_image("images/pause/resume.png")
        self.resume_rect = self.resume.get_rect()

        self.resume_rect.x = 421
        self.resume_rect.y = 321.9

        self.resume2 = load_image("images/pause/resume2.png")
        self.actual_resume = self.resume

        self.main_menu = load_image("images/pause/main-menu.png")
        self.main_menu_rect = self.main_menu.get_rect()

        self.main_menu_rect.x = 382.9
        self.main_menu_rect.y = 454.7

        self.main_menu2 = load_image("images/pause/main-menu2.png")
        self.actual_main_menu = self.main_menu

        self.linea = load_image("images/pause/linea.png")
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
                        return "resume"
                    
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
            if not self.hover_played["resume"]:
                    self.boton_sound.play()
                    self.hover_played["resume"] = True
        else:
            self.actual_resume = self.resume
            self.hover_played["resume"] = False

        if self.main_menu_rect.collidepoint(mouse_pos):
            self.actual_main_menu = self.main_menu2
            if not self.hover_played["main_menu"]:
                    self.boton_sound.play()
                    self.hover_played["main_menu"] = True
        else:
            self.actual_main_menu = self.main_menu
            self.hover_played["main_menu"] = False

    

