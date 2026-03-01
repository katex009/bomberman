import pygame
from pathlib import Path
from utils.asset import load_image, load_sound

pygame.init()


class final_state:

    def __init__(self):

        pygame.mixer.init()
        pygame.mixer.music.load(str(Path(__file__).resolve().parents[2] / "assets" / "sounds" / "win.mp3"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(0)

        self.boton_sound = load_sound("sounds/sonido-letras.mp3", volume=0.5)
        self.hover_played = {"restart": False, "main_menu": False}

        self.fondo = load_image("images/final/fondo_final.png")
        self.fondo_rect = self.fondo.get_rect()

        self.felicitaciones = load_image("images/final/felicitaciones.png")
        self.felicitaciones_rect = self.felicitaciones.get_rect()
        self.felicitaciones_rect.centerx = self.fondo_rect.centerx
        self.felicitaciones_rect.y = 408
        self.felicitaciones_visible = True
        self.felicitaciones_blink_timer = 0.0
        self.felicitaciones_blink_interval = 0.35

        self.restart = load_image("images/game_over/restart.png")
        self.restart2 = load_image("images/game_over/restart2.png")
        self.actual_restart = self.restart
        self.restart_rect = self.restart.get_rect()
        self.restart_rect.centerx = self.fondo_rect.centerx
        self.restart_rect.y = 500

        self.main_menu = load_image("images/pause/main-menu.png")
        self.main_menu2 = load_image("images/pause/main-menu2.png")
        self.actual_main_menu = self.main_menu
        self.main_menu_rect = self.main_menu.get_rect()
        self.main_menu_rect.centerx = self.fondo_rect.centerx
        self.main_menu_rect.y = 580

        self.buttons_delay = 6.0
        self.buttons_timer = 0.0
        self.buttons_visible = False

    def update(self, dt):
        if not self.buttons_visible:
            self.buttons_timer += dt
            if self.buttons_timer >= self.buttons_delay:
                self.buttons_visible = True

        self.felicitaciones_blink_timer += dt
        if self.felicitaciones_blink_timer >= self.felicitaciones_blink_interval:
            self.felicitaciones_blink_timer = 0.0
            self.felicitaciones_visible = not self.felicitaciones_visible

        if not self.buttons_visible:
            return

        mouse_pos = pygame.mouse.get_pos()

        if self.restart_rect.collidepoint(mouse_pos):
            self.actual_restart = self.restart2
            if not self.hover_played["restart"]:
                self.boton_sound.play()
                self.hover_played["restart"] = True
        else:
            self.actual_restart = self.restart
            self.hover_played["restart"] = False

        if self.main_menu_rect.collidepoint(mouse_pos):
            self.actual_main_menu = self.main_menu2
            if not self.hover_played["main_menu"]:
                self.boton_sound.play()
                self.hover_played["main_menu"] = True
        else:
            self.actual_main_menu = self.main_menu
            self.hover_played["main_menu"] = False

    def handle_events(self, events):
        if not self.buttons_visible:
            return None

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.restart_rect.collidepoint(event.pos):
                    return "restart"
                if self.main_menu_rect.collidepoint(event.pos):
                    return "menu"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"
        return None

    def render(self, surface):
        surface.blit(self.fondo, self.fondo_rect)
        if self.felicitaciones_visible:
            surface.blit(self.felicitaciones, self.felicitaciones_rect)
        if self.buttons_visible:
            surface.blit(self.actual_restart, self.restart_rect)
            surface.blit(self.actual_main_menu, self.main_menu_rect)
