import os
import sys
from pprint import pprint

_base_path = sys._MEIPASS if getattr(sys, "frozen", False) else os.path.curdir


def _get_path(*args):
    return os.path.join(_base_path, *args)


src_path = {
    "pics": {
        # cards images
        "cards": [_get_path("pics", "cards", f"{i}.png") for i in range(0, 14)],
        # buttons images
        "undo": _get_path("pics", "buttons", "undo.png"),
        "deals": [_get_path("pics", "buttons", f"deal_{i}.png") for i in range(0, 6)],
        # displays images
        "displays": [_get_path("pics", "displays", f"{i}.png") for i in range(0, 9)],
        # icon
        "icon": _get_path("icon", "solitaire.ico"),
    },
    "sounds": {
        sound_name: _get_path("sounds", f"{sound_name}.wav")
        for sound_name in ["complete", "deal", "done", "error", "pick", "undo"]
    },
}


if __name__ == "__main__":
    pprint({path: src_path[path] for path in src_path})
