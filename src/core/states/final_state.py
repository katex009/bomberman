import pygame
from pathlib import Path
from utils.asset import load_image, load_sound

pygame.init()
pygame.font.init()


class final_state:

    def __init__(self, score_system=None):

        pygame.mixer.init()
        pygame.mixer.music.load(str(Path(__file__).resolve().parents[2] / "assets" / "sounds" / "win.mp3"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(0)

        self.boton_sound = load_sound("sounds/sonido-letras.mp3", volume=0.5)
        self.puntaje_sound = load_sound("sounds/puntaje.mp3", volume=0.5)
        self.hover_played = {"restart": False, "main_menu": False}

        self.score_system = score_system
        font_path = str(Path(__file__).resolve().parents[2] / "assets" / "fonts" / "ARCADECLASSIC.TTF")
        self.score_font = pygame.font.Font(font_path, 50)
        
        self.puntaje_items_actual = 0
        self.puntaje_enemigos_actual = 0
        self.puntaje_total_actual = 0
        
        if score_system:
            self.puntaje_items_target = score_system.puntaje_items
            self.puntaje_enemigos_target = score_system.puntaje_enemigos
            self.puntaje_total_target = score_system.get_total_score()
        else:
            self.puntaje_items_target = 0
            self.puntaje_enemigos_target = 0
            self.puntaje_total_target = 0
        
        self.animation_speed = 100
        self.animation_stage = 0
        self.animation_delay = 1.0
        self.animation_timer = 0.0
        self.sound_played = {"items": False, "enemigos": False, "total": False}

        self.fondo = load_image("images/final/fondo_final.png")
        self.fondo_rect = self.fondo.get_rect()

        self.puntaje_image = load_image("images/final/nombre_puntajes.png", (421, 179))
        self.puntaje_rect = self.puntaje_image.get_rect()

        self.puntaje_rect.x = 147.4
        self.puntaje_rect.y = 335.1

        self.felicitaciones = load_image("images/final/felicitaciones.png")
        self.felicitaciones_rect = self.felicitaciones.get_rect()
        self.felicitaciones_rect.centerx = self.fondo_rect.centerx
        self.felicitaciones_rect.y = 241.5
        self.felicitaciones_visible = True
        self.felicitaciones_blink_timer = 0.0
        self.felicitaciones_blink_interval = 0.35

        self.restart = load_image("images/game_over/restart.png", (227, 44))
        self.restart2 = load_image("images/game_over/restart2.png", (227, 44))
        self.actual_restart = self.restart
        self.restart_rect = self.restart.get_rect()
        self.restart_rect.centerx = self.fondo_rect.centerx
        self.restart_rect.y = 550

        self.main_menu = load_image("images/pause/main-menu.png")
        self.main_menu2 = load_image("images/pause/main-menu2.png")
        self.actual_main_menu = self.main_menu
        self.main_menu_rect = self.main_menu.get_rect()
        self.main_menu_rect.centerx = self.fondo_rect.centerx
        self.main_menu_rect.y = 630

        self.buttons_delay = 8.0
        self.buttons_timer = 0.0
        self.buttons_visible = False

    def update(self, dt):
        self.animation_timer += dt
        
        if self.animation_stage == 0 and self.animation_timer >= self.animation_delay:
            if self.puntaje_items_actual < self.puntaje_items_target:
                if not self.sound_played["items"]:
                    self.puntaje_sound.play()
                    self.sound_played["items"] = True
                increment = min(self.animation_speed, self.puntaje_items_target - self.puntaje_items_actual)
                self.puntaje_items_actual += increment
            else:
                self.animation_stage = 1
                self.animation_timer = 0.0
        
        elif self.animation_stage == 1 and self.animation_timer >= 0.5:
            if self.puntaje_enemigos_actual < self.puntaje_enemigos_target:
                if not self.sound_played["enemigos"]:
                    self.puntaje_sound.play()
                    self.sound_played["enemigos"] = True
                increment = min(self.animation_speed, self.puntaje_enemigos_target - self.puntaje_enemigos_actual)
                self.puntaje_enemigos_actual += increment
            else:
                self.animation_stage = 2
                self.animation_timer = 0.0
        
        elif self.animation_stage == 2 and self.animation_timer >= 0.5:
            if self.puntaje_total_actual < self.puntaje_total_target:
                if not self.sound_played["total"]:
                    self.puntaje_sound.play()
                    self.sound_played["total"] = True
                increment = min(self.animation_speed, self.puntaje_total_target - self.puntaje_total_actual)
                self.puntaje_total_actual += increment
            else:
                self.animation_stage = 3
        
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
        surface.blit(self.puntaje_image, self.puntaje_rect)
        
        items_text = f"{self.puntaje_items_actual:07d}"
        items_surface = self.score_font.render(items_text, True, (255, 255, 255))
        surface.blit(items_surface, (600, 340))
        
        enemigos_text = f"{self.puntaje_enemigos_actual:07d}"
        enemigos_surface = self.score_font.render(enemigos_text, True, (255, 255, 255))
        surface.blit(enemigos_surface, (600, 400))
        
        total_text = f"{self.puntaje_total_actual:07d}"
        total_surface = self.score_font.render(total_text, True, (255, 255, 255))
        surface.blit(total_surface, (600, 460))
        
        if self.felicitaciones_visible:
            surface.blit(self.felicitaciones, self.felicitaciones_rect)
        if self.buttons_visible:
            surface.blit(self.actual_restart, self.restart_rect)
            surface.blit(self.actual_main_menu, self.main_menu_rect)
