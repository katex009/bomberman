from pathlib import Path
import pygame

BASE_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = BASE_DIR / "assets"

_image_cache = {}
_sound_cache = {}

def load_image(path: str, size: int | None = None) -> pygame.Surface:

    if path not in _image_cache:
        image = pygame.image.load(str(ASSETS_DIR / path)).convert_alpha()

        if size:
            image = pygame.transform.scale(image, (size, size))
            
        _image_cache[path] = image
    return _image_cache[path]

def load_sound(path: str, volume: float = 1.0) -> pygame.mixer.Sound:

    if path not in _sound_cache:
        sound = pygame.mixer.Sound(str(ASSETS_DIR / path))
        sound.set_volume(volume)

        _sound_cache[path] = sound
    return _sound_cache[path]

def load_music(path: str, volume: float = 0.5, loop: int = 0):
    pygame.mixer.init()
    pygame.mixer.music.load(str(ASSETS_DIR / path))
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loop)

# Funciones auxiliares para rutas comunes
def load_player_image(name: str, size: int = 45) -> pygame.Surface:
    return load_image(f"images/player/{name}", size)

def load_menu_image(name: str) -> pygame.Surface:
    return load_image(f"images/menu/{name}")

def load_game_sound(name: str, volume: float = 1.0) -> pygame.mixer.Sound:
    return load_sound(f"sounds/{name}", volume)