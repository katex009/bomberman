import pygame
from entities.bomb import Bomb
from entities.explosion import Explosion

pygame.init()

class BombSystem:
    
    def __init__(self, map_ref=None):

        self.bombs = []
        self.explosions = []
        self.base_max_bombs = 1
        self.max_bombs = self.base_max_bombs
        self.map_ref = map_ref

    def can_place_bomb(self):
        return len(self.bombs) < self.max_bombs
    
    def place_bomb(self, grid_x, grid_y, fire_range=1, is_remote=False, is_piercing=False):

        if self.can_place_bomb():
            bomb = Bomb(grid_x, grid_y, is_remote=is_remote)
            bomb.fire_range = fire_range
            bomb.is_piercing = is_piercing
            if is_piercing:
                bomb.frames = bomb.bomba_perforadora
                bomb.image = bomb.frames[bomb.frame]
            self.bombs.append(bomb)
            return True
        return False
    
    def detonate_remote_bomb(self):
        for bomb in self.bombs:
            if bomb.is_remote and not bomb.exploded:
                bomb.exploded = True
                return True
        return False
    
    def update(self, dt):

        for bomb in self.bombs:
            bomb.update(dt)

            if bomb.exploded and not hasattr(bomb, 'explosion_created'):
                bomb.explosion_created = True
                fire_range = getattr(bomb, 'fire_range', 1)
                is_piercing = getattr(bomb, 'is_piercing', False)
                self._create_explosions(bomb.grid_x, bomb.grid_y, fire_range, is_piercing=is_piercing)
        
        self.bombs = [bomb for bomb in self.bombs if not bomb.exploded]
        
        for explosion in self.explosions:
            explosion.update(dt)
        
        self.explosions = [exp for exp in self.explosions if not exp.finished]
    
    def _create_explosions(self, grid_x, grid_y, fire_range=1, is_piercing=False):
        self.explosions.append(Explosion(grid_x, grid_y, direction="center"))
        
        for i in range(1, fire_range + 1):
            new_y = grid_y - i
            if new_y < 0:
                break
            if self.map_ref and self.map_ref.is_indestructible(grid_x, new_y):
                break
            if self.map_ref and self.map_ref.is_destructible(grid_x, new_y):
                for block in self.map_ref.destructible_blocks:
                    if block.grid_x == grid_x and block.grid_y == new_y:
                        block.destroy()
                if not is_piercing:
                    break
            if i == fire_range:
                self.explosions.append(Explosion(grid_x, new_y, direction="up"))
            else:
                self.explosions.append(Explosion(grid_x, new_y, direction="middle_vertical"))
            
        for i in range(1, fire_range + 1):
            new_y = grid_y + i
            if new_y > 10:
                break
            if self.map_ref and self.map_ref.is_indestructible(grid_x, new_y):
                break
            if self.map_ref and self.map_ref.is_destructible(grid_x, new_y):
                for block in self.map_ref.destructible_blocks:
                    if block.grid_x == grid_x and block.grid_y == new_y:
                        block.destroy()
                if not is_piercing:
                    break
            if i == fire_range:
                self.explosions.append(Explosion(grid_x, new_y, direction="down"))
            else:
                self.explosions.append(Explosion(grid_x, new_y, direction="middle_vertical"))
            
        for i in range(1, fire_range + 1):
            new_x = grid_x - i
            if new_x < 0:
                break
            if self.map_ref and self.map_ref.is_indestructible(new_x, grid_y):
                break
            if self.map_ref and self.map_ref.is_destructible(new_x, grid_y):
                for block in self.map_ref.destructible_blocks:
                    if block.grid_x == new_x and block.grid_y == grid_y:
                        block.destroy()
                if not is_piercing:
                    break
            if i == fire_range:
                self.explosions.append(Explosion(new_x, grid_y, direction="left"))
            else:
                self.explosions.append(Explosion(new_x, grid_y, direction="middle_horizontal"))
            
        for i in range(1, fire_range + 1):
            new_x = grid_x + i
            if new_x > 16:
                break
            if self.map_ref and self.map_ref.is_indestructible(new_x, grid_y):
                break
            if self.map_ref and self.map_ref.is_destructible(new_x, grid_y):
                for block in self.map_ref.destructible_blocks:
                    if block.grid_x == new_x and block.grid_y == grid_y:
                        block.destroy()
                if not is_piercing:
                    break
            if i == fire_range:
                self.explosions.append(Explosion(new_x, grid_y, direction="right"))
            else:
                self.explosions.append(Explosion(new_x, grid_y, direction="middle_horizontal"))
    
    def draw(self, surface):

        for explosion in self.explosions:
            explosion.draw(surface)
        
        for bomb in self.bombs:
            bomb.draw(surface)
