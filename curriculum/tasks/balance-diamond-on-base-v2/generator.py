"""Regenerate seed.json for balance-diamond-on-base.

The seed shows a rectangle as ground with a text label next to it.
Anouther narrow rectangle is placed on top of the ground rectangle with a text label next to it.
Aditionally, a diamond is placed on top of the ground rectangle.

The task is to balance the diamond on the narrow rectangle.


Run:
    python3 curriculum/tasks/balance-diamond-on-base/generator.py
"""


import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_root))

from curriculum.seed_generator import SeedBuilder, rectangle, diamond, text

b = SeedBuilder()
b.add(rectangle(562, 554, 754, 222, meta_label="ground"))
b.add(text(1336, 658, "ground", meta_label="ground_text"))
b.add(rectangle(795, 370, 10, 181, meta_label="base"))
b.add(text(734, 448, "base", meta_label="base_text"))
b.add(diamond(1119, 296, 218, 266, meta_label="diamond"))

b.save(Path(__file__).parent / "seed.json")
