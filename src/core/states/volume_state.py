import pygame
from utils.asset import load_image, load_sound, load_music

class volume_state:

    def __init__(self):
        self.boton_sound = load_sound("sounds/sonido-letras.mp3", volume=0.5)
        self.hover_played = {"exit": False, "music_menos": False, "music_mas": False, "sound_menos": False, "sound_mas": False}

        self.background = load_image("images/opciones/volume_fondo.png")
        self.rect = self.background.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.exit_image = load_image("images/menu/exit.png", (103.7, 40))
        self.exit_rect = self.exit_image.get_rect()
        self.exit_rect.x = 39.8
        self.exit_rect.y = 34.3
        self.exit_image2 = load_image("images/menu/exit2.png", (103.7, 40))
        self.actual_exit_image = self.exit_image

        self.triangulo_menos = load_image("images/opciones/triangulo_menos.png")
        self.triangulo_mas = load_image("images/opciones/triangulo_mas.png")
        self.triangulo_menos2 = load_image("images/opciones/triangulo_menos2.png")
        self.triangulo_mas2 = load_image("images/opciones/triangulo_mas2.png")
        
        self.actual_music_menos = self.triangulo_menos
        self.actual_music_mas = self.triangulo_mas
        self.actual_sound_menos = self.triangulo_menos
        self.actual_sound_mas = self.triangulo_mas

        self.music_volume = 5
        self.sound_volume = 5

        self.music_menos_rect = pygame.Rect(229, 246.6, 50, 50)
        self.music_mas_rect = pygame.Rect(715.8, 246.9, 50, 50)
        self.sound_menos_rect = pygame.Rect(229, 441.4, 50, 50)
        self.sound_mas_rect = pygame.Rect(715.8, 441.4, 50, 50)

    def draw_volume_bar(self, surface, x, y, volume):
        for i in range(volume):
            pygame.draw.rect(surface, (255, 255, 255), (x + i * 40, y, 25, 56))

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
            
            if self.music_menos_rect.collidepoint(mouse_pos):
                self.actual_music_menos = self.triangulo_menos2
                if not self.hover_played["music_menos"]:
                    self.boton_sound.play()
                    self.hover_played["music_menos"] = True
            else:
                self.actual_music_menos = self.triangulo_menos
                self.hover_played["music_menos"] = False
            
            if self.music_mas_rect.collidepoint(mouse_pos):
                self.actual_music_mas = self.triangulo_mas2
                if not self.hover_played["music_mas"]:
                    self.boton_sound.play()
                    self.hover_played["music_mas"] = True
            else:
                self.actual_music_mas = self.triangulo_mas
                self.hover_played["music_mas"] = False
            
            if self.sound_menos_rect.collidepoint(mouse_pos):
                self.actual_sound_menos = self.triangulo_menos2
                if not self.hover_played["sound_menos"]:
                    self.boton_sound.play()
                    self.hover_played["sound_menos"] = True
            else:
                self.actual_sound_menos = self.triangulo_menos
                self.hover_played["sound_menos"] = False
            
            if self.sound_mas_rect.collidepoint(mouse_pos):
                self.actual_sound_mas = self.triangulo_mas2
                if not self.hover_played["sound_mas"]:
                    self.boton_sound.play()
                    self.hover_played["sound_mas"] = True
            else:
                self.actual_sound_mas = self.triangulo_mas
                self.hover_played["sound_mas"] = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.exit_rect.collidepoint(event.pos):
                    return "options"
                
                if self.music_menos_rect.collidepoint(event.pos):
                    self.music_volume = max(0, self.music_volume - 1)
                    pygame.mixer.music.set_volume(self.music_volume / 10)
                    self.boton_sound.play()
                
                if self.music_mas_rect.collidepoint(event.pos):
                    self.music_volume = min(10, self.music_volume + 1)
                    pygame.mixer.music.set_volume(self.music_volume / 10)
                    self.boton_sound.play()
                
                if self.sound_menos_rect.collidepoint(event.pos):
                    self.sound_volume = max(0, self.sound_volume - 1)
                    self.boton_sound.set_volume(self.sound_volume / 10)
                    self.boton_sound.play()
                
                if self.sound_mas_rect.collidepoint(event.pos):
                    self.sound_volume = min(10, self.sound_volume + 1)
                    self.boton_sound.set_volume(self.sound_volume / 10)
                    self.boton_sound.play()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "options"
        return None

    def render(self, surface):  
        surface.blit(self.background, self.rect)
        surface.blit(self.actual_exit_image, self.exit_rect)
        
        surface.blit(self.actual_music_menos, self.music_menos_rect)
        self.draw_volume_bar(surface, 296.7, 240.3, self.music_volume)
        surface.blit(self.actual_music_mas, self.music_mas_rect)
        
        surface.blit(self.actual_sound_menos, self.sound_menos_rect)
        self.draw_volume_bar(surface, 296.7, 439.6, self.sound_volume)
        surface.blit(self.actual_sound_mas, self.sound_mas_rect)