"""Regenerate seed.json for precise-earase.

This seed shows 9 overlapping ellipses.
The agent task is to erase the narrowest ellipse without touching other items using Eraser tool in Excalidraw.

Run:
    python3 curriculum/tasks/precise-earase/generator.py
"""

import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_root))

from curriculum.seed_generator import SeedBuilder, ellipse

b = SeedBuilder()
b.add(ellipse(x=602, y=191, width=174, height=154))
b.add(ellipse(x=655, y=154, width=151, height=170))
b.add(ellipse(x=692, y=268, width=267, height=215))
b.add(ellipse(x=647, y=249, width=252, height=175))
b.add(ellipse(x=707, y=144, width=250, height=232))
b.add(ellipse(x=720, y=191, width=29, height=230, meta_label="narrowest"))  # narrowest ellipse
b.add(ellipse(x=612, y=369, width=252, height=124))
b.add(ellipse(x=751, y=235, width=241, height=223))
b.add(ellipse(x=686, y=361, width=179, height=168))

b.save(Path(__file__).parent / "seed.json")
