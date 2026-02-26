import sys
from pathlib import Path
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
        
        # Inicializar entidades
        self.map = Map()
        self.player = Player(x=1, y=1)
        self.bomb_system = BombSystem()
        
        # Items de prueba
        self.items = [
            Item(5, 5, item_type="speed"),
            Item(8, 3, item_type="fire"),
            Item(3, 8, item_type="speed"),
            Item(10, 10, item_type="fire")
        ]
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    fire_range = getattr(self.player, 'fire_range', 1)
                    self.bomb_system.place_bomb(self.player.grid_x, self.player.grid_y, fire_range)
    
    def update(self):
        dt = self.clock.get_time() / 1000.0
        self.player.update(dt)
        self.bomb_system.update(dt)
        
        # Actualizar items y verificar colisiones
        for item in self.items:
            item.update(dt)
            item.check_collision(self.player)
    
    def render(self):
        self.map.draw(self.screen)
        self.bomb_system.draw(self.screen)
        
        # Dibujar items
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
