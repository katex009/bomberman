import pygame

pygame.init()

class ScoreSystem:
    def __init__(self):
        self.puntaje_enemigos = 0
        self.puntaje_items = 0
        self.puntaje_bloques = 0
        self.puntaje_salida = 0
        self.multiplicador = 1
        self.enemigos_en_explosion = 0
        
    def reset_multiplicador(self):
        self.multiplicador = 1
        self.enemigos_en_explosion = 0
    
    def add_enemy_kill(self):
        puntos = 2000 * self.multiplicador
        self.puntaje_enemigos += puntos
        self.enemigos_en_explosion += 1
        self.multiplicador = 2
    
    def add_item_collected(self):
        self.puntaje_items += 1000

    def add_block_destroyed(self):
        self.puntaje_bloques += 134
    
    def add_exit_bonus(self):
        self.puntaje_salida += 3000
    
    def get_total_score(self):
        return self.puntaje_enemigos + self.puntaje_items + self.puntaje_bloques + self.puntaje_salida
