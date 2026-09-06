"""
LoL Minimap Mirror — captures a region of monitor 1 and displays it fullscreen on monitor 2.

Hotkeys (while the mirror window is focused):
  Arrow keys       — move crop region by 5px
  Shift+Arrows     — resize crop region by 5px (right/down edge)
  Ctrl+Arrows      — fine adjust by 1px
  S                — save current crop to config.json
  R                — reset to default minimap region
  Esc / Q          — quit
"""

import json
import sys
from pathlib import Path

import mss
import pygame

CONFIG_PATH = Path(__file__).parent / "config.json"

DEFAULT_CROP = {"left": 1620, "top": 810, "width": 300, "height": 270}
SOURCE_MONITOR = 1
TARGET_MONITOR = 2
TARGET_SIZE = (1920, 1080)
FPS = 60


def load_crop():
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text())
        except Exception:
            pass
    return dict(DEFAULT_CROP)


def save_crop(crop):
    CONFIG_PATH.write_text(json.dumps(crop, indent=2))
    print(f"Saved crop: {crop}")


def main():
    crop = load_crop()

    with mss.mss() as sct:
        monitors = sct.monitors
        if len(monitors) < 3:
            print("Need 2 monitors. Detected:", monitors)
            sys.exit(1)

        src_mon = monitors[SOURCE_MONITOR]
        tgt_mon = monitors[TARGET_MONITOR]

        import os
        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{tgt_mon['left']},{tgt_mon['top']}"

        pygame.init()
        screen = pygame.display.set_mode(TARGET_SIZE, pygame.NOFRAME)
        pygame.display.set_caption("LoL Minimap Mirror")
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    mods = pygame.key.get_mods()
                    step = 1 if (mods & pygame.KMOD_CTRL) else 5
                    resize = bool(mods & pygame.KMOD_SHIFT)

                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        running = False
                    elif event.key == pygame.K_s:
                        save_crop(crop)
                    elif event.key == pygame.K_r:
                        crop = dict(DEFAULT_CROP)
                        print("Reset:", crop)
                    elif event.key == pygame.K_LEFT:
                        if resize: crop["width"] = max(20, crop["width"] - step)
                        else:      crop["left"] -= step
                    elif event.key == pygame.K_RIGHT:
                        if resize: crop["width"] += step
                        else:      crop["left"] += step
                    elif event.key == pygame.K_UP:
                        if resize: crop["height"] = max(20, crop["height"] - step)
                        else:      crop["top"] -= step
                    elif event.key == pygame.K_DOWN:
                        if resize: crop["height"] += step
                        else:      crop["top"] += step

            region = {
                "left": src_mon["left"] + crop["left"],
                "top":  src_mon["top"]  + crop["top"],
                "width":  crop["width"],
                "height": crop["height"],
            }
            raw = sct.grab(region)

            img = pygame.image.frombuffer(raw.rgb, raw.size, "RGB")
            img = pygame.transform.smoothscale(img, TARGET_SIZE)
            screen.blit(img, (0, 0))
            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
