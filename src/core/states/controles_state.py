import pygame
from utils.asset import load_image, load_sound, load_music

class controls_state:

    def __init__(self):
        self.boton_sound = load_sound("sounds/sonido-letras.mp3", volume=0.5)
        self.hover_played = {"exit": False}

        self.background = load_image("images/opciones/fondo_controles.png")
        self.rect = self.background.get_rect()

        self.exit_image = load_image("images/menu/exit.png", (103.7, 40))
        self.exit_rect = self.exit_image.get_rect()

        self.exit_rect.x = 39.8
        self.exit_rect.y = 34.3

        self.exit_image2 = load_image("images/menu/exit2.png", (103.7, 40))
        self.actual_exit_image = self.exit_image

    def update(self, dt):
        if pygame.get_init():
            mouse_pos = pygame.mouse.get_pos()

            if self.exit_rect.collidepoint(mouse_pos):
                self.actual_exit_image = self.exit_image2
                if not self.hover_played["exit"]:
                    self.boton_sound.play()
                    self.hover_played["exit"] = True
            else:
                self.actual_exit_image = self.exit_image
                self.hover_played["exit"] = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    if self.exit_rect.collidepoint(event.pos):
                        return "options"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "options"
        return None

    def render(self, surface):  
        surface.blit(self.background, self.rect)
        surface.blit(self.actual_exit_image, self.exit_rect)
