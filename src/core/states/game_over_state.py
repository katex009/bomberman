import pygame
from utils.asset import load_image, load_sound
from pathlib import Path

pygame.init()


class game_over_state:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load(str(Path(__file__).resolve().parents[2] / "assets" / "sounds" / "game-over.mp3"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(1)

        self.boton_sound = load_sound("sounds/sonido-letras.mp3", volume=0.5)
        self.hover_played = {"restart": False, "main_menu": False}

        try:
            self.fondo = load_image("images/game_over/game_over.png")
            self.fondo_rect = self.fondo.get_rect()
        except pygame.error:
            self.fondo = pygame.Surface((1024, 768))
            self.fondo.fill((20, 0, 0))
            self.fondo_rect = self.fondo.get_rect()

        self.restart = load_image("images/game_over/restart.png")
        self.restart2 = load_image("images/game_over/restart2.png")
        self.actual_restart = self.restart
        self.restart_rect = self.restart.get_rect()
        self.restart_rect.x = 379.8
        self.restart_rect.y = 519.6

        self.main_menu = load_image("images/pause/main-menu.png")
        self.main_menu2 = load_image("images/pause/main-menu2.png")
        self.actual_main_menu = self.main_menu
        self.main_menu_rect = self.main_menu.get_rect()
        self.main_menu_rect.x = 379.8
        self.main_menu_rect.y = 592.4

    def update(self, dt):
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
        surface.blit(self.actual_restart, self.restart_rect)
        surface.blit(self.actual_main_menu, self.main_menu_rect)
