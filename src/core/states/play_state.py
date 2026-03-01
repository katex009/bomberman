import pygame
import random
from pathlib import Path
from entities.player import Player
from entities.enemy import Enemy
from entities.map import Map
from systems.bomb_system import BombSystem
from utils.asset import load_image

pygame.init()


class play_state:

    def __init__(self):

        self.map = Map()
        self.player = Player(x=1, y=1)
        self.enemies = self._spawn_enemies(6)
        self.bomb_system = BombSystem()
        self.player_dead = False
        self.player_dead_type = "bomb"
        self.game_over_delay = 5.0
        self.player_dead_timer = 0.0
        self.death_sound_played = False

        self.map_origin_x = 62
        self.map_origin_y = 168
        self.exit_size = 24
        self.exit_padding = (self.map.tile_size - self.exit_size) // 2
        self.exit_image = load_image("images/mapa/salida.png", (self.exit_size, self.exit_size))
        self.exit_rect = None
        self.exit_grid_pos = None
        self.exit_visible = False
        self.level_completed = False

        pygame.mixer.init()
        pygame.mixer.music.load(str(Path(__file__).resolve().parents[2] / "assets" / "sounds" / "juego.mp3"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        self.player_dead_sound = pygame.mixer.Sound(
            str(Path(__file__).resolve().parents[2] / "assets" / "sounds" / "player-muere.mp3")
        )

    def _spawn_enemies(self, count):
        enemies = []
        used_positions = {(self.player.grid_x, self.player.grid_y)}

        while len(enemies) < count:
            grid_x = random.randint(0, 17)
            grid_y = random.randint(0, 10)
            pos = (grid_x, grid_y)

            if pos in used_positions:
                continue

            enemies.append(Enemy(grid_x, grid_y))
            used_positions.add(pos)

        return enemies

    def _spawn_exit(self):
        if self.exit_visible:
            return

        possible_tiles = []
        for grid_y in range(self.map.tiles_y):
            for grid_x in range(self.map.tiles_x):
                if (grid_x, grid_y) == (self.player.grid_x, self.player.grid_y):
                    continue

                possible_tiles.append((grid_x, grid_y))

        if not possible_tiles:
            return

        self.exit_grid_pos = random.choice(possible_tiles)
        grid_x, grid_y = self.exit_grid_pos
        tile_x = self.map_origin_x + grid_x * self.map.tile_size + self.exit_padding
        tile_y = self.map_origin_y + grid_y * self.map.tile_size + self.exit_padding
        self.exit_rect = pygame.Rect(tile_x, tile_y, self.exit_size, self.exit_size)
        self.exit_visible = True

    def handle_events(self, events):
        if self.level_completed:
            return "final"

        if self.player_dead:
            if self.player_dead_timer >= self.game_over_delay:
                return "game_over"
            return None

        if self.exit_visible and self.exit_grid_pos == (self.player.grid_x, self.player.grid_y):
            self.level_completed = True
            return "final"

        action = self.player.handle_events(events)

        if action == "place_bomb":
            if self.player.skull_curse_time <= 0:
                fire_range = getattr(self.player, 'fire_range', 1)
                use_remote = self.player.remote_bombs_remaining > 0
                bomb_placed = self.bomb_system.place_bomb(
                    self.player.grid_x,
                    self.player.grid_y,
                    fire_range,
                    is_remote=use_remote
                )
                if bomb_placed and use_remote:
                    self.player.remote_bombs_remaining -= 1
                    self.player.remote_bombs_remaining = max(0, self.player.remote_bombs_remaining)

        for event in events:
            if event.type == pygame.KEYDOWN:
                has_remote_bombs_active = any(
                    bomb.is_remote and not bomb.exploded
                    for bomb in self.bomb_system.bombs
                )
                can_detonate_remote = (
                    self.player.remote_bombs_remaining > 0
                    or has_remote_bombs_active
                )
                if event.key == pygame.K_e and can_detonate_remote:
                    self.bomb_system.detonate_remote_bomb()
                if event.key == pygame.K_ESCAPE:
                    return "pause"
        return None

    def _kill_player(self, death_type):
        if self.player_dead:
            return
        self.player_dead = True
        self.player_dead_type = death_type
        self.player_dead_timer = 0.0
        pygame.mixer.music.stop()
        if not self.death_sound_played:
            self.player_dead_sound.play()
            self.death_sound_played = True

    def update(self, dt):
        if self.player_dead:
            self.player_dead_timer += dt

        if self.player.skull_curse_time > 0:
            self.bomb_system.max_bombs = 6
            self.player.skull_curse_time = max(0.0, self.player.skull_curse_time - dt)
            self.player.move_speed = random.randint(80, 500)

        else:
            self.bomb_system.max_bombs = self.bomb_system.base_max_bombs

        if self.player.skull_curse_time > 0 and self.player.is_moving:
            current_tile = (self.player.grid_x, self.player.grid_y)

            if self.player.skull_last_bomb_tile != current_tile:
                if random.random() < 0.5:

                    fire_range = getattr(self.player, 'fire_range', 1)
                    self.bomb_system.place_bomb(
                        self.player.grid_x,
                        self.player.grid_y,
                        fire_range,
                        is_remote=False)

                self.player.skull_last_bomb_tile = current_tile

        if self.player.skull_curse_time <= 0 and self.player.skull_saved_speed is not None:
            self.player.move_speed = self.player.skull_saved_speed
            self.player.skull_saved_speed = None

        self.player.update(dt, is_dead=self.player_dead, death_type=self.player_dead_type)
        self.bomb_system.update(dt)

        for enemy in self.enemies:
            if enemy.dead:
                continue
            if any(
                not exp.finished
                and exp.grid_x == enemy.grid_x
                and exp.grid_y == enemy.grid_y
                for exp in self.bomb_system.explosions
            ):
                enemy.kill()

        for enemy in self.enemies:
            enemy.update(dt)

        if not self.exit_visible and not any(not enemy.dead for enemy in self.enemies):
            self._spawn_exit()

        self.enemies = [enemy for enemy in self.enemies if not enemy.dead_finished]

        if not self.player_dead and any(self.player.rect.colliderect(enemy.rect) for enemy in self.enemies if not enemy.dead):
            self._kill_player("normal")

        if any(
            not exp.finished
            and exp.grid_x == self.player.grid_x
            and exp.grid_y == self.player.grid_y
            for exp in self.bomb_system.explosions
        ):
            self._kill_player("bomb")

        if not self.player_dead and self.exit_visible and self.exit_grid_pos == (self.player.grid_x, self.player.grid_y):
            self.level_completed = True

    def render(self, surface):
        self.map.draw(surface)
        if self.exit_visible and self.exit_rect:
            surface.blit(self.exit_image, self.exit_rect)
        self.bomb_system.draw(surface)
        for enemy in self.enemies:
            enemy.draw(surface)
        self.player.draw(surface)
