import pygame
from utils.asset import load_image, load_sound, load_music

class options_state:

    def __init__(self):

        self.boton_sound = load_sound("sounds/sonido-letras.mp3", volume=0.5)
        self.hover_played = {"exit": False, "volume": False, "controls": False}

        self.background = load_image("images/opciones/options_fondo.png")
        self.rect = self.background.get_rect()

        self.exit_image = load_image("images/menu/exit.png", (103.7, 40))
        self.exit_rect = self.exit_image.get_rect()

        self.exit_rect.x = 39.8
        self.exit_rect.y = 34.3

        self.exit_image2 = load_image("images/menu/exit2.png", (103.7, 40))
        self.actual_exit_image = self.exit_image

        self.controls = load_image("images/opciones/controls.png")
        self.controls_rect = self.controls.get_rect()

        self.controls_rect.x = 360.5
        self.controls_rect.y = 377.3

        self.controls2 = load_image("images/opciones/controls2.png")
        self.acual_controls = self.controls.get_rect()

        self.volume = load_image("images/opciones/volume.png")
        self.volume_rect = self.volume.get_rect()

        self.volume_rect.x = 351.1
        self.volume_rect.y = 239.7

        self.volume2 = load_image("images/opciones/volume2.png")
        self.acual_volume = self.volume.get_rect()

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

            if self.controls_rect.collidepoint(mouse_pos):
                self.actual_controls = self.controls2
                if not self.hover_played["controls"]:
                        self.boton_sound.play()
                        self.hover_played["controls"] = True
            else:
                self.actual_controls = self.controls
                self.hover_played["controls"] = False

            if self.volume_rect.collidepoint(mouse_pos):
                self.actual_volume = self.volume2
                if not self.hover_played["volume"]:
                        self.boton_sound.play()
                        self.hover_played["volume"] = True
            else:
                self.actual_volume = self.volume
                self.hover_played["volume"] = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    if self.exit_rect.collidepoint(event.pos):
                        return "menu"
                    if self.controls_rect.collidepoint(event.pos):
                        return "controls"
                    if self.volume_rect.collidepoint(event.pos):
                        return "volume"
                    
        return None

    def render(self, surface):  
        surface.blit(self.background, self.rect)
        surface.blit(self.actual_exit_image, self.exit_rect)
        surface.blit(self.actual_controls, self.controls_rect)
        surface.blit(self.actual_volume, self.volume_rect)
