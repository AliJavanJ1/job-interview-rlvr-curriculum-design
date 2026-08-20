"""
Grader: Precise Erase
Verifies that an Excalidraw project has the narrowest ellipse erased without touching other items.

Rubrics:
- no_item_added: Project has not added any new items
- seed_ellipse_{idx}_preserved: Project still has the seed ellipse number {idx}
- seed_ellipse_{idx}_position_preserved: The seed ellipse number {idx} preserved its position (x, y, angle)
- seed_ellipse_{idx}_size_preserved: The seed ellipse number {idx} preserved its size (width, height)
- seed_ellipse_{idx}_color_preserved: The seed ellipse number {idx} preserved its stroke and background colors
- seed_narrowest_ellipse_erased: The narrowest ellipse was erased
"""

import sys
import json
from pathlib import Path

_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_root))

from curriculum.sdk import ExcalidrawProject
from curriculum import GraderInput, rubricgrader, rubrics

_SIZE_TOLERANCE = 1.0  # px
_MOTION_TOLERANCE = 1.0  # px
_ANGLE_TOLERANCE = 0.001  # degrees


def _size_unchanged(el, width: float, height: float) -> bool:
    return (
        abs(el.width - width) <= _SIZE_TOLERANCE
        and abs(el.height - height) <= _SIZE_TOLERANCE
    )


def _position_unchanged(el, x: float, y: float, angle: float) -> bool:
    return (
        abs(el.x - x) <= _MOTION_TOLERANCE
        and abs(el.y - y) <= _MOTION_TOLERANCE
        and abs(el.angle - angle) <= _ANGLE_TOLERANCE
    )


@rubricgrader
def grader(input: GraderInput):
    project = ExcalidrawProject(input["snapshots"]["excalidraw"])

    elemnts = project.get_all_elements()
    n_elements = len(elemnts)
    ellipses = project.get_ellipses()
    n_ellipses = len(ellipses)

    # read seed.json
    with open(Path(__file__).parent / "seed.json") as f:
        seed_data = json.load(f)

    for idx, el in enumerate(seed_data["elements"]):
        seed_ellipse = el
        seed_x = seed_ellipse["x"]
        seed_y = seed_ellipse["y"]
        seed_angle = seed_ellipse["angle"]
        seed_width = seed_ellipse["width"]
        seed_height = seed_ellipse["height"]
        is_narrowest = seed_ellipse.get("meta_label") == "narrowest"

        element = project.get_element_by_id(seed_ellipse["id"])
        x = element.x if element else None
        y = element.y if element else None
        angle = element.angle if element else None
        width = element.width if element else None
        height = element.height if element else None

        if is_narrowest:
            rubrics.assertTrue(
                f"seed_narrowest_ellipse_erased",
                element is None,
                success=f"The narrowest ellipse was erased",
                failure=f"The narrowest ellipse was not erased",
            )
        else:
            rubrics.assertTrue(
                f"seed_ellipse_{idx}_preserved",
                element is not None,
                success=f"Project still has seed ellipse number {idx}",
                failure=f"Elipse number {idx} from removed from the project.",
            )

            rubrics.assertTrue(
                f"seed_ellipse_{idx}_position_preserved",
                (
                    _position_unchanged(element, seed_x, seed_y, seed_angle)
                    if element
                    else False
                ),
                success=f"Elipse number {idx} preserved position (x={seed_x}, y={seed_y}, angle={seed_angle})",
                failure=(
                    f"Ellipse number {idx} not present to check position"
                    if element is None
                    else f"Expected ellipse number {idx} to have position (x={seed_x}, y={seed_y}, angle={seed_angle}), got (x={x}, y={y}, angle={angle})"
                ),
            )

            rubrics.assertTrue(
                f"seed_ellipse_{idx}_size_preserved",
                _size_unchanged(element, seed_width, seed_height) if element else False,
                success=f"Elipse number {idx} preserved size (width={seed_width}, height={seed_height})",
                failure=(
                    f"Ellipse number {idx} not present to check size"
                    if element is None
                    else f"Expected ellipse number {idx} to have size (width={seed_width}, height={seed_height}), got (width={width}, height={height})"
                ),
            )

            rubrics.assertTrue(
                f"seed_ellipse_{idx}_color_preserved",
                (
                    element.stroke_color.lower() == seed_ellipse["strokeColor"].lower()
                    and element.background_color.lower()
                    == seed_ellipse["backgroundColor"].lower()
                    if element
                    else False
                ),
                success=f"Elipse number {idx} preserved stroke and background colors (stroke={seed_ellipse['strokeColor']}, background={seed_ellipse['backgroundColor']})",
                failure=(
                    f"Ellipse number {idx} not present to check colors"
                    if element is None
                    else f"Expected ellipse number {idx} to have colors (stroke={seed_ellipse['strokeColor']}, background={seed_ellipse['backgroundColor']}), got (stroke={element.stroke_color}, background={element.background_color})"
                ),
            )


if __name__ == "__main__":
    path = (
        Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "seed.json"
    )
    with open(path) as f:
        data = json.load(f)
    result = grader(
        {
            "snapshots": {"excalidraw": data},
            "transcript": "",
            "extra_fields": {},
            "posted_answer": None,
        }
    )
    print(f"result={result['result']}")
    for k, v in result["metadata"]["rubrics"].items():
        print(
            f"  {'PASS' if v['pass'] else 'FAIL'} {k}: {v.get('message') or v.get('description', '')}"
        )
