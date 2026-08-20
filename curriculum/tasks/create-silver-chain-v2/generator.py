"""Regenerate seed.json for create-silver-chain.

The seed shows an empty canvas. The agent task is to create a chain of 10 identical circular ellipses linked together to form a closed chain. with silver color (#C0C0C0).
Run:
    python3 curriculum/tasks/create-silver-chain/generator.py
"""

import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_root))

from curriculum.seed_generator import SeedBuilder

b = SeedBuilder()

b.save(Path(__file__).parent / "seed.json")
