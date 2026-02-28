import sys
from pathlib import Path
import random
import pygame

# Configurar rutas
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR / "src"))

# Importar lo necesario
from entities.map import Map
from entities.player import Player
from entities.items import Item
from systems.bomb_system import BombSystem

# Inicializar pygame
pygame.init()

# Configuración
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

class TestGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bomberman - Test Items")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.map = Map()
        self.player = Player(x=1, y=1)
        self.bomb_system = BombSystem()
        
        self.items = [
            Item(5, 5, item_type="speed"),
            Item(8, 3, item_type="fire"),
            Item(3, 8, item_type="speed"),
            Item(10, 10, item_type="fire"),
            Item(8, 10, item_type="slow"),
            Item(12, 5, item_type="slow"),
            Item(13, 13, item_type="remote"),
            Item(6, 12, item_type="calavera")
        ]
    
    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                elif event.key == pygame.K_SPACE:
                    if self.player.skull_curse_time <= 0:
                        fire_range = getattr(self.player, 'fire_range', 1)
                        use_remote = self.player.remote_bombs_remaining > 0
                        bomb_placed = self.bomb_system.place_bomb(
                            self.player.grid_x,
                            self.player.grid_y,
                            fire_range,
                            is_remote=use_remote)
                        
                        if bomb_placed and use_remote:
                            self.player.remote_bombs_remaining -= 1
                            self.player.remote_bombs_remaining = max(0, self.player.remote_bombs_remaining)

                elif event.key == pygame.K_e:
                    has_remote_bombs_active = any(
                        bomb.is_remote and not bomb.exploded
                        for bomb in self.bomb_system.bombs)
                    
                    can_detonate_remote = (
                        self.player.remote_bombs_remaining > 0
                        or has_remote_bombs_active)

                    if can_detonate_remote:
                        self.bomb_system.detonate_remote_bomb()
    
    def update(self):
        dt = self.clock.get_time() / 1000.0
        if self.player.skull_curse_time > 0:
            self.bomb_system.max_bombs = 6
        else:
            self.bomb_system.max_bombs = self.bomb_system.base_max_bombs

        if self.player.skull_curse_time > 0:
            self.player.skull_curse_time = max(0.0, self.player.skull_curse_time - dt)
            self.player.skull_speed_change_timer -= dt
            self.player.skull_auto_bomb_cooldown = max(0.0, self.player.skull_auto_bomb_cooldown - dt)

            if self.player.skull_speed_change_timer <= 0:
                self.player.move_speed = random.randint(80, 360)
                self.player.skull_speed_change_timer = random.uniform(0.2, 0.7)

        self.player.update(dt)

        if self.player.skull_curse_time > 0 and self.player.is_moving and self.player.skull_auto_bomb_cooldown <= 0:
            current_tile = (self.player.grid_x, self.player.grid_y)
            if self.player.skull_last_bomb_tile != current_tile:
                fire_range = getattr(self.player, 'fire_range', 1)
                bomb_placed = self.bomb_system.place_bomb(
                    self.player.grid_x,
                    self.player.grid_y,
                    fire_range,
                    is_remote=False
                )
                if bomb_placed:
                    self.player.skull_last_bomb_tile = current_tile
                    self.player.skull_auto_bomb_cooldown = random.uniform(0.15, 0.4)

        if self.player.skull_curse_time <= 0 and self.player.skull_saved_speed is not None:
            self.player.move_speed = self.player.skull_saved_speed
            self.player.skull_saved_speed = None

        self.bomb_system.update(dt)
        
        for item in self.items:
            item.update(dt)
            item.check_collision(self.player)
    
    def render(self):
        self.map.draw(self.screen)
        self.bomb_system.draw(self.screen)
        
        for item in self.items:
            item.draw(self.screen)
        
        self.player.draw(self.screen)
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = TestGame()
    game.run()
