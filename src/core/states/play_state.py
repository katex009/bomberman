import pygame
import random
from pathlib import Path
from entities.player import Player
from entities.enemy import Enemy
from entities.map import Map
from entities.items import Item
from systems.bomb_system import BombSystem
from systems.score_system import ScoreSystem
from utils.asset import load_image

pygame.init()
pygame.font.init()


class play_state:

    def __init__(self):

        self.map = Map()
        self.player = Player(x=0, y=0)
        self.enemies = self._spawn_enemies(6)
        self.bomb_system = BombSystem(map_ref=self.map)
        self.items = []
        self.player_dead = False
        self.player_dead_type = "bomb"
        self.game_over_delay = 5.0
        self.player_dead_timer = 0.0
        self.death_sound_played = False

        self.map_origin_x = 87
        self.map_origin_y = 168
        self.exit_size = 24
        self.exit_padding = (self.map.tile_size - self.exit_size) // 2
        self.exit_image = load_image("images/mapa/salida.png", (self.exit_size, self.exit_size))
        self.exit_rect = None
        self.exit_grid_pos = None
        self.exit_visible = False
        self.level_completed = False
        self.victory_animation_timer = 0.0
        self.victory_animation_duration = 3.0

        self.level_time = 180.0
        font_path = str(Path(__file__).resolve().parents[2] / "assets" / "fonts" / "ARCADECLASSIC.TTF")
        self.timer_font = pygame.font.Font(font_path, 40)
        self.score_font = pygame.font.Font(font_path, 40)
        self.score_system = ScoreSystem()

        pygame.mixer.init()
        pygame.mixer.music.load(str(Path(__file__).resolve().parents[2] / "assets" / "sounds" / "juego.mp3"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        self.player_dead_sound = pygame.mixer.Sound(
            str(Path(__file__).resolve().parents[2] / "assets" / "sounds" / "player-muere.mp3")
        )

    def _spawn_enemies(self, count):
        def is_valid_enemy_spawn(grid_x, grid_y, used_positions):
            pos = (grid_x, grid_y)
            if pos in used_positions:
                return False
            return not self.map.is_blocked(grid_x, grid_y)

        enemies = []
        used_positions = {(self.player.grid_x, self.player.grid_y), (0, 0), (1, 0), (0, 1)}

        valid_positions = []
        for grid_y in range(self.map.tiles_y):
            for grid_x in range(self.map.tiles_x):
                if is_valid_enemy_spawn(grid_x, grid_y, used_positions):
                    valid_positions.append((grid_x, grid_y))

        random.shuffle(valid_positions)

        for grid_x, grid_y in valid_positions[:count]:
            enemies.append(Enemy(grid_x, grid_y))

        return enemies

    def _spawn_exit(self):
        if self.exit_visible:
            return

        possible_tiles = []
        for grid_y in range(self.map.tiles_y):
            for grid_x in range(self.map.tiles_x):
                if (grid_x, grid_y) == (self.player.grid_x, self.player.grid_y):
                    continue
                if self.map.is_blocked(grid_x, grid_y):
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
        if self.level_completed and self.victory_animation_timer >= self.victory_animation_duration:
            return "final"

        if self.player_dead:
            if self.player_dead_timer >= self.game_over_delay:
                return "game_over"
            return None

        if self.exit_visible and self.exit_grid_pos == (self.player.grid_x, self.player.grid_y):
            if not self.level_completed:
                self.level_completed = True
            return None

        action = self.player.handle_events(events)

        if action == "place_bomb":
            if self.player.skull_curse_time <= 0:
                fire_range = getattr(self.player, 'fire_range', 1)
                use_remote = self.player.remote_bombs_remaining > 0
                bomb_placed = self.bomb_system.place_bomb(
                    self.player.grid_x,
                    self.player.grid_y,
                    fire_range,
                    is_remote=use_remote,
                    is_piercing=self.player.has_piercing_bombs
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
        if self.level_completed:
            self.victory_animation_timer += dt
            self.player.update(dt, is_victory=True, map_ref=self.map, bomb_system=self.bomb_system)
            return

        self.bomb_system.base_max_bombs = 1 + self.player.extra_bombs
        if self.player.piercing_bomb_time > 0:
            self.player.piercing_bomb_time = max(0.0, self.player.piercing_bomb_time - dt)
            self.player.has_piercing_bombs = self.player.piercing_bomb_time > 0
        
        if self.player_dead:
            self.player_dead_timer += dt
        else:
            self.level_time -= dt
            if self.level_time <= 0:
                self._kill_player("normal")

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
                        is_remote=False,
                        is_piercing=self.player.has_piercing_bombs)

                self.player.skull_last_bomb_tile = current_tile

        if self.player.skull_curse_time <= 0 and self.player.skull_saved_speed is not None:
            self.player.move_speed = self.player.skull_saved_speed
            self.player.skull_saved_speed = None

        self.player.update(dt, is_dead=self.player_dead, death_type=self.player_dead_type, map_ref=self.map, bomb_system=self.bomb_system)
        self.bomb_system.update(dt)
        
        for block in self.map.destructible_blocks:
            block.update(dt)
            if block.destroyed and not block.score_given:
                self.score_system.add_block_destroyed()
                block.score_given = True
            if block.destroyed and not block.item_dropped and block.item_type:
                self.items.append(Item(block.grid_x, block.grid_y, block.item_type))
                block.item_dropped = True
        
        for item in self.items:
            item.check_collision(self.player, self.score_system)

        enemies_killed_this_frame = []
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
                enemies_killed_this_frame.append(enemy)
        
        if enemies_killed_this_frame:
            for enemy in enemies_killed_this_frame:
                self.score_system.add_enemy_kill()
        else:
            self.score_system.reset_multiplicador()

        for enemy in self.enemies:
            enemy.update(dt, map_ref=self.map, bomb_system=self.bomb_system)

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
            if not self.level_completed:
                self.score_system.add_exit_bonus()
                pygame.mixer.music.stop()
            self.level_completed = True

    def render(self, surface):

        self.map.draw(surface)
        if self.exit_visible and self.exit_rect:
            surface.blit(self.exit_image, self.exit_rect)
        
        for item in self.items:
            item.draw(surface)
        
        self.bomb_system.draw(surface)
        for enemy in self.enemies:
            enemy.draw(surface)
        self.player.draw(surface)
        
        minutes = int(max(0, self.level_time) // 60)
        seconds = int(max(0, self.level_time) % 60)
        timer_text = f"{minutes:02d}  {seconds:02d}"
        timer_surface = self.timer_font.render(timer_text, True, (255, 255, 255))
        surface.blit(timer_surface, (188, 45))

        font = pygame.font.Font(None, 36)
        dos_puntos = font.render(":", True, (255, 255, 255))
        surface.blit(dos_puntos, (230, 55))
        
        score_text = f"{self.score_system.get_total_score():07d}"
        score_surface = self.score_font.render(score_text, True, (255, 255, 255))
        surface.blit(score_surface, (778, 45))

        life_text = "0" if self.player_dead else "1"
        life_surface = self.score_font.render(life_text, True, (255, 255, 255))
        surface.blit(life_surface, (455.3, 45.2))
