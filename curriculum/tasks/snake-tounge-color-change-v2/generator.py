"""Regenerate seed.json for snake-tounge-color-change.

The seed shows a scetch of a snake that is not colored created using only a few ellips. 
The agent task is to identify the group of ellips that make up the snake's tongue and change their background color to #e03131 (red) which is not a default color in Excalidraw's palette.

Run:
    python3 curriculum/tasks/snake-tounge-color-change/generator.py
"""


import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_root))

from curriculum.seed_generator import SeedBuilder, ellipse, BLUE

b = SeedBuilder()

b.add(ellipse(x=1278.125, y=320.77020144940695, width=63.75, height=10.959597101186095, angle=0.5667292175235064, meta_label="tongue"))
b.add(ellipse(x=1284.8772231204528, y=294.0563776822283, width=63.75, height=10.959597101186095, angle=6.0244144152158885, meta_label="tongue"))
b.add(ellipse(x=1192.5, y=303.75, width=93.75, height=12.5, meta_label="tongue"))
b.add(ellipse(x=1145, y=317.5, width=17.5, height=15, meta_label="same"))
b.add(ellipse(x=1143.75, y=285, width=17.5, height=15, meta_label="same"))
b.add(ellipse(x=1078.75, y=265, width=112.5, height=92.5, meta_label="same"))
b.add(ellipse(x=846.25, y=270, width=233.75, height=86.25000000000001, meta_label="same"))
b.add(ellipse(x=613.125, y=269.375, width=233.75, height=86.25000000000001, meta_label="same"))
b.add(ellipse(x=378.125, y=274.375, width=233.75, height=86.25000000000001, meta_label="same"))

b.save(Path(__file__).parent / "seed.json")
