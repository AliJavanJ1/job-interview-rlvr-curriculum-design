"""
Grader: Yellow Circle Within Blue Box

Verifies that an Excalidraw project contains a yellow ellipse fully contained
within a blue rectangle.

Rubrics:
- seed_ellipse_{idx}_preserved: Project still has the seed ellipse number {idx}
- seed_ellipse_{idx}_position_preserved: The seed ellipse number {idx} still has the same position (x, y, angle)
- seed_ellipse_{idx}_size_preserved: The seed ellipse number {idx} still has the same size (width, height)
- seed_ellipse_{idx}_stroke_color_preserved: The seed ellipse number {idx} still has the same stroke color
- for tounge ellipses:
    - seed_ellipse_{idx}_background_color_changed: The seed ellipse number {idx} has changed its background color to #e03131 (red)
- for non-tounge ellipses:
    - seed_ellipse_{idx}_background_color_preserved: The seed ellipse number {idx} still has the same background color
    
tounge elipses indexes: 0, 1, 2
non-tounge elipses indexes: 3, 4, 5, 6, 7, 8

value mappings:
- "red" -> #e03131 (not in Excalidraw's default palette)
"""

import sys
import json
from pathlib import Path

_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_root))

from curriculum.sdk import ExcalidrawProject
from curriculum import GraderInput, rubricgrader, rubrics

_TOUNGE_COLOR = "#e03131"  # red, not in Excalidraw's default palette
_SIZE_TOLERANCE = 1.0  # pixels
_MOTION_TOLERANCE = 1.0  # pixels

def _size_unchanged(el, width: float, height: float) -> bool:
    return abs(el.width - width) <= _SIZE_TOLERANCE and abs(el.height - height) <= _SIZE_TOLERANCE

def _position_unchanged(el, x: float, y: float, angle: float) -> bool:
    return abs(el.x - x) <= _MOTION_TOLERANCE and abs(el.y - y) <= _MOTION_TOLERANCE and abs(el.angle - angle) <= _MOTION_TOLERANCE

@rubricgrader
def grader(input: GraderInput):
    project = ExcalidrawProject(input["snapshots"]["excalidraw"])

    ellipses = project.get_ellipses()
    n_e = len(ellipses)
    
    # read seed.json
    with open(Path(__file__).parent / "seed.json") as f:
        seed_data = json.load(f)
    for idx, el in enumerate(seed_data["elements"]):
            seed_ellipse = el
            seed_stroke_color = seed_ellipse["strokeColor"]
            seed_background_color = seed_ellipse["backgroundColor"]
            seed_x = seed_ellipse["x"]
            seed_y = seed_ellipse["y"]
            seed_angle = seed_ellipse["angle"]
            seed_width = seed_ellipse["width"]
            seed_height = seed_ellipse["height"]
            
            element = project.get_element_by_id(seed_ellipse["id"])
            e_stroke_color = element.stroke_color if element else None
            e_background_color = element.background_color if element else None
            e_x = element.x if element else None
            e_y = element.y if element else None
            e_angle = element.angle if element else None
            e_width = element.width if element else None
            e_height = element.height if element else None
            
            rubrics.assertTrue(f"seed_ellipse_{idx}_preserved", element is not None,
                success=f"Project still has seed ellipse number {idx}",
                failure=f"Elipse number {idx} from removed from the project."
            )
            
            rubrics.assertTrue(f"seed_ellipse_{idx}_position_preserved", _position_unchanged(element, seed_x, seed_y, seed_angle) if element else False,
                success=f"Elipse number {idx} preserved position (x={seed_x}, y={seed_y}, angle={seed_angle})",
                failure=(
                    f"Ellipse number {idx} not present to check position"
                    if element is None else
                    f"Expexted elipse number {idx} to have position (x={seed_x}, y={seed_y}, angle={seed_angle}), got (x={e_x}, y={e_y}, angle={e_angle})"
                )
            )
            
            rubrics.assertTrue(f"seed_ellipse_{idx}_size_preserved", _size_unchanged(element, seed_width, seed_height) if element else False,
                success=f"Elipse number {idx} preserved size (width={seed_width}, height={seed_height})",
                failure=(
                    f"Ellipse number {idx} not present to check size"
                    if element is None else
                    f"Expected elipse number {idx} to have size (width={seed_width}, height={seed_height}), got (width={e_width}, height={e_height})"
                )
            )
            
            rubrics.assertTrue(f"seed_ellipse_{idx}_stroke_color_preserved", e_stroke_color == seed_stroke_color,
                success=f"Elipse number {idx} preserved stroke color ({seed_stroke_color})",
                failure=(
                    f"Ellipse number {idx} not present to check stroke color"
                    if element is None else
                    f"Expected elipse number {idx} to have stroke color ({seed_stroke_color}), got ({e_stroke_color})"
                )
            )
                
            if el["meta_label"] == "same":
                rubrics.assertTrue(f"seed_ellipse_{idx}_background_color_preserved", e_background_color == seed_background_color,
                    success=f"Elipse number {idx} preserved background color ({seed_background_color})",
                    failure=(
                        f"Ellipse number {idx} not present to check background color"
                        if element is None else
                        f"Expected elipse number {idx} to have background color ({seed_background_color}), got ({e_background_color})"
                    )
                )
            else:
                rubrics.assertTrue(f"seed_ellipse_{idx}_background_color_changed", e_background_color == _TOUNGE_COLOR,
                    success=f"Elipse number {idx} changed background color to {_TOUNGE_COLOR}",
                    failure=(
                        f"Ellipse number {idx} not present to check background color"
                        if element is None else
                        f"Expected elipse number {idx} to have background color changed to {_TOUNGE_COLOR}, got ({e_background_color})"
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
