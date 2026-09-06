# LoL Minimap Mirror

Mirror a cropped region of your primary monitor (the League of Legends minimap) fullscreen onto a second monitor. Handy for glancing at map state without eye-darting to the corner of your main display.

![platform](https://img.shields.io/badge/platform-Windows-blue) ![python](https://img.shields.io/badge/python-3.10%2B-yellow)

## How it works

Grabs a configurable rectangle from monitor 1 with [`mss`](https://python-mss.readthedocs.io/) and blits it upscaled to a borderless pygame window pinned to monitor 2. Runs at 60 FPS.

## Requirements

- Windows with two monitors (defaults tuned for 1920x1080 on both)
- Python 3.10+
- `pip install mss pygame`

## Usage

Double-click `run.bat` (or create a desktop shortcut to it). Launch League in **Borderless** windowed mode on monitor 1, then drag the crop rectangle over the minimap once and save.

### Hotkeys

| Key                | Action                          |
|--------------------|---------------------------------|
| Arrow keys         | Move crop region (5 px)         |
| Shift + Arrows     | Resize crop (right/bottom edge) |
| Ctrl + Arrows      | Fine adjust (1 px)              |
| S                  | Save crop to `config.json`      |
| R                  | Reset to default region         |
| Esc / Q            | Quit                            |

## Config

`config.json` stores your crop rectangle:

```json
{ "left": 1620, "top": 810, "width": 300, "height": 270 }
```

Defaults assume the League minimap in the bottom-right of a 1920x1080 display. Delete the file to reset.

## Notes

- Works for any game or app — not League-specific. Just crop whatever region you want mirrored.
- If your second monitor has a different resolution, edit `TARGET_SIZE` in `minimap.py`.
- Monitor arrangement is read from the OS, so mirroring works regardless of whether monitor 2 is to the left or right.
