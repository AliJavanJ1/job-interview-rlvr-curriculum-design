"""
Grader: Yellow Circle Within Blue Box

Verifies that an Excalidraw project contains a yellow ellipse fully contained
within a blue rectangle.

Rubrics:
- seed_one_ellipse_preserved: Project still has exactly 1 ellipse
- seed_one_rectangle_preserved: Project still has exactly 1 rectangle
- seed_ellipse_is_yellow: The ellipse still has a yellow background (#ffec99)
- seed_rectangle_is_blue: The rectangle still has a blue background (#a5d8ff)
- seed_ellipse_radius_preserved: The ellipse's radius (width/height) is unchanged
- seed_rectangle_sides_preserved: The rectangle's sides (width/height) are unchanged
- ellipse_within_rectangle: The ellipse is fully contained within the rectangle (task goal)

Value mappings:
- "yellow" -> #ffec99 (Excalidraw's default yellow)
- "blue"   -> #a5d8ff (Excalidraw's default light blue)

Original dimensions (from seed.json, must not change):
- ellipse:   306.62109375 x 305.36328125 (radius)
- rectangle: 323.36718749999994 x 321.2734375 (sides)
"""

import sys
import json
from pathlib import Path

_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_root))

from curriculum.sdk import ExcalidrawProject
from curriculum import GraderInput, rubricgrader, rubrics

_ELLIPSE_WIDTH = 306.62109375
_ELLIPSE_HEIGHT = 305.36328125
_RECTANGLE_WIDTH = 323.36718749999994
_RECTANGLE_HEIGHT = 321.2734375
_SIZE_TOLERANCE = 1.0  # px — absorbs float drift on save/reload, not enough to hide a resize


def _size_unchanged(el, width: float, height: float) -> bool:
    return abs(el.width - width) <= _SIZE_TOLERANCE and abs(el.height - height) <= _SIZE_TOLERANCE


@rubricgrader
def grader(input: GraderInput):
    project = ExcalidrawProject(input["snapshots"]["excalidraw"])

    ellipses = project.get_ellipses()
    rectangles = project.get_rectangles()
    n_e, n_r = len(ellipses), len(rectangles)

    ellipse = ellipses[0] if n_e == 1 else None
    rectangle = rectangles[0] if n_r == 1 else None

    rubrics.assertTrue("seed_one_ellipse_preserved", n_e == 1,
        success="Project still has exactly 1 ellipse",
        failure=(
            "Expected 1 ellipse, got 0 — original ellipse was removed."
            if n_e == 0 else
            f"Expected 1 ellipse, got {n_e} — {n_e - 1} extra ellipse(s) wrongfully added."
        )
    )
    rubrics.assertTrue("seed_one_rectangle_preserved", n_r == 1,
        success="Project still has exactly 1 rectangle",
        failure=(
            "Expected 1 rectangle, got 0 — original rectangle was removed."
            if n_r == 0 else
            f"Expected 1 rectangle, got {n_r} — {n_r - 1} extra rectangle(s) wrongfully added."
        )
    )
    rubrics.assertTrue("seed_ellipse_is_yellow",
        ellipse.has_background_color("#ffec99") if ellipse else False,
        success="Ellipse preserved yellow background (#ffec99)",
        failure=(
            "No ellipse present to check color."
            if not ellipse else
            f"Expected ellipse background to stay yellow (#ffec99), got {ellipse.background_color!r}"
        )
    )
    rubrics.assertTrue("seed_rectangle_is_blue",
        rectangle.has_background_color("#a5d8ff") if rectangle else False,
        success="Rectangle preserved blue background (#a5d8ff)",
        failure=(
            "No rectangle present to check color."
            if not rectangle else
            f"Expected rectangle background to stay blue (#a5d8ff), got {rectangle.background_color!r}"
        )
    )
    rubrics.assertTrue("seed_ellipse_radius_preserved",
        _size_unchanged(ellipse, _ELLIPSE_WIDTH, _ELLIPSE_HEIGHT) if ellipse else False,
        success="Ellipse preserved its original radius",
        failure=(
            "No ellipse present to check radius."
            if not ellipse else
            f"Expected ellipse to keep its radius ({_ELLIPSE_WIDTH:.1f}x{_ELLIPSE_HEIGHT:.1f}), "
            f"got {ellipse.width:.1f}x{ellipse.height:.1f} — it was resized."
        )
    )
    rubrics.assertTrue("seed_rectangle_sides_preserved",
        _size_unchanged(rectangle, _RECTANGLE_WIDTH, _RECTANGLE_HEIGHT) if rectangle else False,
        success="Rectangle preserved its original sides",
        failure=(
            "No rectangle present to check sides."
            if not rectangle else
            f"Expected rectangle to keep its sides ({_RECTANGLE_WIDTH:.1f}x{_RECTANGLE_HEIGHT:.1f}), "
            f"got {rectangle.width:.1f}x{rectangle.height:.1f} — it was resized."
        )
    )
    rubrics.assertTrue("ellipse_within_rectangle",
        ellipse.is_within(rectangle) if ellipse and rectangle else False,
        success="Ellipse is fully contained within the rectangle",
        failure=(
            "Cannot check containment — ellipse or rectangle is missing."
            if not ellipse or not rectangle else
            "Ellipse is not fully contained within the rectangle — it extends outside its bounds."
        )
    )


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "seed.json"
    with open(path) as f:
        data = json.load(f)
    result = grader({"snapshots": {"excalidraw": data}, "transcript": "", "extra_fields": {}, "posted_answer": None})
    print(f"result={result['result']}")
    for k, v in result["metadata"]["rubrics"].items():
        print(f"  {'PASS' if v['pass'] else 'FAIL'} {k}: {v.get('message') or v.get('description', '')}")
