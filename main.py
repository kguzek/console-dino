#!/usr/bin/env python
"""Main game process."""

# Standard library imports
import time
import random

# Third-party imports
try:
    import keyboard
    from corny_commons import file_manager, console_graphics
except ImportError as impt_e:
    raise SystemExit(
        f"\nERROR: You have to install the required dependency '{impt_e.name}' to run this program."
    ) from impt_e

NUM_COLUMNS = 5
NUM_ROWS = 5
COLUMN_WIDTH = 3
# Number of milliseconds between each game cycle
FRAMETIME = 150
# Min and max bounds for time between generation, milliseconds
CACTUS_GENERATION_BOUNDS = (500, 2000)

DINO_CHAR = "◼"
CACTUS_CHAR = "8"

display = console_graphics.Display(NUM_COLUMNS * COLUMN_WIDTH, NUM_ROWS)


ACTION_JUMP = "jump"
ACTION_DUCK = "duck"


class GameData:  # pylint: disable=too-few-public-methods
    """Container for the current game process information."""

    game_over = False
    last_tick: float = 0
    jump_stage: int = 1
    score: int = 0
    last_cactus_generated: float = time.time()  # seconds since epoch
    cactus_generation_cooldown: int = -1  # milliseconds
    cactus_positions: list[int] = []
    key_mappings: dict[str, str] = {
        "w": ACTION_JUMP,
        "up": ACTION_JUMP,
        "space": ACTION_JUMP,
        "s": ACTION_DUCK,
        "down": ACTION_DUCK,
    }
    was_pressed: set[str] = set()


def write_char(text, x_pos, y_pos) -> None:
    """Wrapper function for adjusting printed content according to column width."""
    pos = x_pos * 3, y_pos
    whitespace = " " * (COLUMN_WIDTH // 3)
    display.write_string(whitespace + text + whitespace, pos)


def render() -> None:
    """Rerenders the game window."""
    jump_stage = GameData.jump_stage
    if jump_stage > 2:
        jump_stage = 1
    dino_y = NUM_ROWS - jump_stage - 1
    cactus_y = NUM_ROWS - 1
    score_text = str(GameData.score).rjust(5, "0")
    score_text_x = COLUMN_WIDTH * NUM_COLUMNS - len(score_text) - 1
    score_text_y = 0

    display.clear()
    write_char(DINO_CHAR, 0, dino_y)
    if jump_stage != -1:
        write_char(DINO_CHAR, 0, dino_y - 1)
    for cactus_x in GameData.cactus_positions:
        write_char(CACTUS_CHAR, cactus_x, cactus_y)
    display.write_string(score_text, (score_text_x, score_text_y))


# def get_input() -> None:
#     """Checks for user input for each defined action key."""
#     for action, keys_tuple in GameData.keys.items():
#         if any(keyboard.is_pressed(key) for key in keys_tuple):
#             GameData.was_pressed.add(action)


def set_input_handlers() -> None:
    """Creates input handlers for each defined action key."""

    def handler(event):
        if event.event_type == "down":
            func = GameData.was_pressed.add
        else:
            func = GameData.was_pressed.discard
        func(GameData.key_mappings[event.name])

    for key in GameData.key_mappings:
        keyboard.hook_key(key, handler)


def tick() -> None:
    """Executes one cycle of the game process."""
    # Handle dinosaur control
    if GameData.jump_stage == 3:
        GameData.jump_stage = 0
    elif GameData.jump_stage > 0:
        GameData.jump_stage += 1
    elif ACTION_JUMP in GameData.was_pressed:
        GameData.jump_stage = 1
    elif ACTION_DUCK in GameData.was_pressed:
        GameData.jump_stage = -1
    else:
        GameData.jump_stage = 0
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
    if GameData.cactus_generation_cooldown < 0:
        GameData.cactus_generation_cooldown = random.randint(*CACTUS_GENERATION_BOUNDS)
    if (
        GameData.last_tick - GameData.last_cactus_generated
        > GameData.cactus_generation_cooldown / 1000
    ):
        GameData.cactus_generation_cooldown = -1
        GameData.last_cactus_generated = GameData.last_tick
        GameData.cactus_positions.append(NUM_COLUMNS - 1)


def main() -> None:
    """Game entry point."""
    game_started_at = time.time()
    set_input_handlers()
    try:
        while not GameData.game_over:
            # Ensure 10 FPS
            now = time.time()
            # Make frametime shorter the longer the game has been going
            actual_frame_time = FRAMETIME - now + game_started_at
            if now - GameData.last_tick < actual_frame_time / 1000:
                continue
            GameData.last_tick = now
            tick()
            render()
            GameData.score += 1
    except KeyboardInterrupt:
        pass
    finally:
        display.clear()
        text_x = NUM_COLUMNS * COLUMN_WIDTH // 3
        text_y = 2
        display.write_string("GAME", (text_x, text_y))
        display.write_string("OVER!", (text_x, text_y + 1))
        display.close()
    try:
        input("Press enter to continue...\n")
    except KeyboardInterrupt:
        pass
    file_manager.log("Exitted.")


if __name__ == "__main__":
    main()
