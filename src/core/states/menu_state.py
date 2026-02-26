import pygame
from utils.asset import load_image, load_sound, load_music

pygame.init()


class menu_state:
    
    def __init__(self):

        self.boton_sound = load_sound("sounds/sonido-letras.mp3", volume=0.5)
        self.hover_played = {"start": False, "exit": False}
        #self.start_sound = load_sound("sounds/boton-start.mp3", volume=0.5)

        self.background = load_image("images/menu/menu.png")
        self.rect = self.background.get_rect()

        self.start_image = load_image("images/menu/start.png")
        self.start_rect = self.start_image.get_rect()

        self.start_rect.x = 436.3
        self.start_rect.y = 476.5

        self.start_image2 = load_image("images/menu/start2.png")
        self.actual_start_image = self.start_image

        self.exit_image = load_image("images/menu/exit.png")
        self.exit_rect = self.exit_image.get_rect()

        self.exit_rect.x = 438.3
        self.exit_rect.y = 564

        self.exit_image2 = load_image("images/menu/exit2.png")
        self.actual_exit_image = self.exit_image

        load_music("sounds/menu.mp3", volume=0.5, loop=0)

    def render(self, surface):
        surface.blit(self.background, self.rect)
        surface.blit(self.actual_start_image, self.start_rect)
        surface.blit(self.actual_exit_image, self.exit_rect)


    def update(self, dt):
        if pygame.get_init():
            mouse_pos = pygame.mouse.get_pos()

            if self.start_rect.collidepoint(mouse_pos):
                self.actual_start_image = self.start_image2
                if not self.hover_played["start"]:
                    self.boton_sound.play()
                    self.hover_played["start"] = True
            else:
                self.actual_start_image = self.start_image
                self.hover_played["start"] = False

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
                    if self.start_rect.collidepoint(event.pos):
                        #self.start_sound.play()
                        return "play"
            
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    if self.exit_rect.collidepoint(event.pos):
                        pygame.quit()
        return None
