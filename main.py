"""Main game process."""

# Standard library imports
import time
import random

# Third-party imports
import keyboard

# Local application imports
from corny_commons import file_manager, console_graphics

NUM_COLUMNS, NUM_ROWS = 5, 5
COLUMN_WIDTH = 3
# Number of game cycles to be executed in one second
FRAMERATE = 6
# Min and max bounds for time between generation, milliseconds
CACTUS_GENERATION_BOUNDS = (1000, 3000)

DINO_CHAR = "◼"
CACTUS_CHAR = "8"

display = console_graphics.Display(NUM_COLUMNS * COLUMN_WIDTH, NUM_ROWS)


class GameData:  # pylint: disable=too-few-public-methods
    """Container for the current game process information."""

    game_over = False
    last_tick: float = 0
    jump_stage: float = 0
    last_cactus_generated: float = 0
    cactus_generation_time: float = 0
    cactus_positions: list[int] = []
    keys: dict[str, tuple[str or int]] = {"jump": ("w", "space"), "duck": ("s",)}
    was_pressed: set[str] = set()


def write_char(text, x_pos, y_pos) -> None:
    """Interface function for adjusting printed content according to column width."""
    pos = x_pos * 3, y_pos
    whitespace = " " * (COLUMN_WIDTH // 3)
    display.write_string(whitespace + text + whitespace, pos)


def render() -> None:
    """Rerenders the game window."""
    display.clear()
    jump_stage = GameData.jump_stage
    if jump_stage == 3:
        jump_stage = 1
    y_pos = NUM_ROWS - int(jump_stage) - 1
    write_char(DINO_CHAR, 0, y_pos)
    if jump_stage != -1:
        write_char(DINO_CHAR, 0, y_pos - 1)
    cactus_y = NUM_ROWS - 1
    for cactus_x in GameData.cactus_positions:
        write_char(CACTUS_CHAR, cactus_x, cactus_y)


def get_input() -> None:
    """Checks for user input for each defined action key."""
    for action, keys_tuple in GameData.keys.items():
        if any(keyboard.is_pressed(key) for key in keys_tuple):
            GameData.was_pressed.add(action)


def tick() -> None:
    """Executes one cycle of the game process."""
    # Handle dinosaur control
    if GameData.jump_stage == 3:
        GameData.jump_stage = 0
    elif GameData.jump_stage > 0:
        GameData.jump_stage += 1
    elif "jump" in GameData.was_pressed:
        GameData.jump_stage = 1
    elif "duck" in GameData.was_pressed:
        GameData.jump_stage = -1
    else:
        GameData.jump_stage = 0
    GameData.was_pressed.clear()
    # Handle cactus progression
    for i in range(len(GameData.cactus_positions) - 1, -1, -1):
        cactus_pos = GameData.cactus_positions[i]
        if cactus_pos == 0:
            if GameData.jump_stage <= 0:
                GameData.game_over = True
            GameData.cactus_positions.pop(i)
        else:
            GameData.cactus_positions[i] = cactus_pos - 1
    # Handle cactus generation
    if (
        GameData.last_tick - GameData.last_cactus_generated
        > GameData.cactus_generation_time / 1000
    ):
        GameData.cactus_generation_time = random.randint(*CACTUS_GENERATION_BOUNDS)
        GameData.last_cactus_generated = GameData.last_tick
        GameData.cactus_positions.append(4)


def main() -> None:
    """Game entry point."""
    try:
        while not GameData.game_over:
            # Ensure 10 FPS
            now = time.time()
            if now - GameData.last_tick < 1.0 / FRAMERATE:
                continue
            GameData.last_tick = now
            get_input()
            tick()
            render()
    except KeyboardInterrupt:
        pass
    finally:
        display.clear()
        text_x = NUM_COLUMNS * COLUMN_WIDTH // 3
        text_y = 2
        display.write_string("GAME", (text_x, text_y))
        display.write_string("OVER!", (text_x, text_y + 1))
        display.close()
    input("Press enter to continue...\n")
    file_manager.log("Exitted.")


if __name__ == "__main__":
    main()
