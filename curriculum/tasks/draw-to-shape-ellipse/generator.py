"""Regenerate seed.json for draw-ellipse.

The seed shows an empty canvas. The agent task is to draw an ellipse on the canvas using "Draw to shape" option.

Run:
    python3 curriculum/tasks/draw-to-shape-ellipse/generator.py
"""

import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_root))

from curriculum.seed_generator import SeedBuilder

b = SeedBuilder()

b.save(Path(__file__).parent / "seed.json")
