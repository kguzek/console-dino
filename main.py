"""Main game process."""

# Standard library imports
import time

# Third-party imports
import keyboard

# Local application imports
from corny_commons import file_manager, console_graphics

NUM_COLUMNS, NUM_ROWS = 5, 5
COLUMN_WIDTH = 3
FRAMERATE = 12  # FPS


DINO_CHAR = "◼"


display = console_graphics.Display(NUM_COLUMNS * COLUMN_WIDTH, NUM_ROWS)


def write(text, x_pos, y_pos) -> None:
    """Interface function for adjusting printed content according to column width."""
    pos = x_pos * 3, y_pos
    whitespace = " " * (COLUMN_WIDTH // 3)
    display.write_string(whitespace + text + whitespace, pos)


def render(jump_phase: int) -> None:
    """Renders the dinosaur and cactuses."""
    display.clear()
    if jump_phase == 3:
        jump_phase = 1
    y_pos = NUM_ROWS - jump_phase - 1
    write(DINO_CHAR, 0, y_pos)


def tick(jump_phase: int, last_tick: float) -> tuple[int, float] or None:
    """Executes one cycle of the game process."""
    # Ensure 10 FPS
    now = time.time()
    if now - last_tick < 1.0 / FRAMERATE:
        return None
    if jump_phase == 3:
        jump_phase = 0
    elif jump_phase > 0:
        jump_phase += 1
    elif keyboard.is_pressed("w"):
        jump_phase = 1
    render(jump_phase)
    return jump_phase, now


def main() -> None:
    """Game entry point."""
    game_data = (0, 0)
    try:
        while True:
            temp = tick(*game_data)
            if temp is not None:
                game_data = temp
    except KeyboardInterrupt:
        display.close(clear=True)
        file_manager.log("Exitted.")


if __name__ == "__main__":
    main()
