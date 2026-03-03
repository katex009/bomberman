if self.volume_rect.collidepoint(mouse_pos):
                self.actual_volume = self.volume2
                if not self.hover_played["volume"]:
                        self.boton_sound.play()
                        self.hover_played["volume"] = True
            else:
                self.actual_volume = self.volume
                self.hover_played["volume"] = False