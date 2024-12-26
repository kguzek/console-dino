# Console Dino

This a simple Python implementation of the Google Chrome Dino game, completely playable from within your terminal!

## Dependencies

This application uses the following packages:

1. `keyboard` -- for allowing keyboard input
2. `corny-commons` -- a package authored by me which contains an easy-to-use console graphics engine

## Installation

Clone this repository and install the above mentioned dependencies.

```bash
git clone --depth 1 https://github.com/kguzek/console-dino
pip install keyboard corny-commons
```

## How to launch

To play the game, simply call `main.py`. It has no other modules; the game is fully contained within that file.

```bash
./main.py
```

or

```bash
python main.py
```

### Virtual environments and Linux

If you are using a Python virtual environment on Linux, you might come across an error while trying to run the program.
The `keyboard` module expects you to be the superuser (root), but when using `sudo` your virtual environment isn't preserved.
You can get around this by explicitly using the virtual environment Python binary.

```bash
.venv/bin/python main.py
```

Depending on the specific virtual environment, the exact location of the binary might be different.
If all else fails, simply install the dependencies as sudo and run the program without a virtual environment.

## How to play

The only actions you can perform in this game are jumping and ducking. Below are the default keyboard mappings.

- jump: `w`, up arrow, or space
- duck: `s` or down arrow

You can change these keybinds by modifying `GameData.key_mappings` in `main.py`.
Jump to make your character (the two box characters in a column) avoid the "cactuses" (`8`-characters). I made this game quite a while ago, and I don't think I actually implemented the "bats" -- so the ducking is currently an unnecessary game mechanic.

Thanks for reading!
