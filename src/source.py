import os
import sys
from pathlib import Path
from pprint import pprint

_base_path = Path(sys._MEIPASS if getattr(sys, "frozen", False) else os.path.curdir)


src_path = {
    "pics": {
        # background images
        "background": _base_path / "pics" / "background" / "background.png",
        # cards images
        "cards": {
            "back": _base_path / "pics" / "cards" / "back" / "back.png",
            "club": {
                i: _base_path / "pics" / "cards" / "club" / f"{i}.png"
                for i in range(1, 14)
            },
            "diamond": {
                i: _base_path / "pics" / "cards" / "diamond" / f"{i}.png"
                for i in range(1, 14)
            },
            "heart": {
                i: _base_path / "pics" / "cards" / "heart" / f"{i}.png"
                for i in range(1, 14)
            },
            "spade": {
                i: _base_path / "pics" / "cards" / "spade" / f"{i}.png"
                for i in range(1, 14)
            },
        },
        # buttons images
        "undo": _base_path / "pics" / "buttons" / "undo" / "undo.png",
        "suit": {
            i: _base_path / "pics" / "buttons" / "suit" / f"{i}.png" for i in (1, 2, 4)
        },
        "deals": [
            _base_path / "pics" / "buttons" / "deal" / f"{i}.png" for i in range(0, 6)
        ],
        # displays images
        "displays": [
            _base_path / "pics" / "displays" / f"{i}.png" for i in range(0, 9)
        ],
        # icon
        "icon": _base_path / "icon" / "solitaire.ico",
    },
    "sounds": {
        sound_name: _base_path / "sounds" / f"{sound_name}.wav"
        for sound_name in ["complete", "deal", "done", "error", "pick", "undo"]
    },
}


if __name__ == "__main__":
    pprint({path: src_path[path] for path in src_path})
