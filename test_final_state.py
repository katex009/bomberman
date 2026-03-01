import sys
from pathlib import Path

import pygame

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from core.states.final_state import final_state


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Test Final State")
    clock = pygame.time.Clock()

    state = final_state()
    running = True

    while running:
        dt = clock.tick(60) / 1000.0
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        action = state.handle_events(events)
        if action in ("menu", "restart"):
            running = False

        state.update(dt)
        state.render(screen)
        pygame.display.flip()

    pygame.quit()
