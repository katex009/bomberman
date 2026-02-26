import pygame
from entities.bomb import Bomb
from entities.explosion import Explosion

class BombSystem:
    def __init__(self):
        self.bombs = []
        self.explosions = []
        self.max_bombs = 1  
    def can_place_bomb(self):
        return len(self.bombs) < self.max_bombs
    
    def place_bomb(self, grid_x, grid_y, fire_range=1):

        if self.can_place_bomb():
            bomb = Bomb(grid_x, grid_y)
            bomb.fire_range = fire_range
            self.bombs.append(bomb)
            return True
        return False
    
    def update(self, dt):

        for bomb in self.bombs:
            bomb.update(dt)

            if bomb.exploded and not hasattr(bomb, 'explosion_created'):
                bomb.explosion_created = True
                fire_range = getattr(bomb, 'fire_range', 1)
                self._create_explosions(bomb.grid_x, bomb.grid_y, fire_range)
        
        self.bombs = [bomb for bomb in self.bombs if not bomb.exploded]
        
        for explosion in self.explosions:
            explosion.update(dt)
        
        self.explosions = [exp for exp in self.explosions if not exp.finished]
    
    def _create_explosions(self, grid_x, grid_y, fire_range=1):
        self.explosions.append(Explosion(grid_x, grid_y, direction="center"))
        
        for i in range(1, fire_range + 1):
            if i == fire_range:
                self.explosions.append(Explosion(grid_x, grid_y - i, direction="up"))
            else:
                self.explosions.append(Explosion(grid_x, grid_y - i, direction="middle_vertical"))
            
            if i == fire_range:
                self.explosions.append(Explosion(grid_x, grid_y + i, direction="down"))
            else:
                self.explosions.append(Explosion(grid_x, grid_y + i, direction="middle_vertical"))
            
            if i == fire_range:
                self.explosions.append(Explosion(grid_x - i, grid_y, direction="left"))
            else:
                self.explosions.append(Explosion(grid_x - i, grid_y, direction="middle_horizontal"))
            
            if i == fire_range:
                self.explosions.append(Explosion(grid_x + i, grid_y, direction="right"))
            else:
                self.explosions.append(Explosion(grid_x + i, grid_y, direction="middle_horizontal"))
    
    def draw(self, surface):

        for explosion in self.explosions:
            explosion.draw(surface)
        
        for bomb in self.bombs:
            bomb.draw(surface)
