import sys
from pathlib import Path
import pygame
from arcade_machine_sdk import GameMeta

ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR / "src"))
from core.bomberman_game import BombermanGame

if not pygame.get_init():
    pygame.init()

metadata = (
    GameMeta()
    .with_title("Bomberman")
    .with_description("Juego arcade estilo Bomberman")
    .with_release_date("2026")
    .with_group_number(1)
    .add_tag("Arcade")
    .add_author("Katherin Martinez y Rene Franco")
)

game = BombermanGame(metadata)

if __name__ == "__main__":
    game.run_independently()