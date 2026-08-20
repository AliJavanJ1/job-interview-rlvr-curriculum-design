"""
Grader: Balance Diamond on Base

Verifies that an Excalidraw project contains a diamond balanced on a base.

Rubrics:
- seed_{item_name}_preserved: Project still has the seed {item_name}
- seed_{item_name}_size_preserved: The seed {item_name} still has the same size (width, height)
- seed_{item_name}_color_preserved: The seed {item_name} still has the same stroke and background colors (stroke, background)
- seed_{item_name}_position_preserved: The seed {item_name} still has the same position (x, y, angle)
- seed_label_{item_name}_preserved: The seed {item_name} still has the same text
- seed_diamond_is_balanced_on_base: The diamond is balanced on the base (the bottom vertex of the diamond is within the top edge of the base)

item_names:
- diamond (does not include seed_diamond_position_preserved)
- base
- ground
- base_text (has seed_label_base_text_preserved)
- ground_text (has seed_label_ground_text_preserved)
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
_ANGLE_TOLERANCE = 0.001  # radians
_DEFAULT_ANGLE = 0.0  # radians


def _size_unchanged(el, width: float, height: float) -> bool:
    return abs(el.width - width) <= _SIZE_TOLERANCE and abs(el.height - height) <= _SIZE_TOLERANCE

def _position_unchanged(el, x: float, y: float, angle: float) -> bool:
    return abs(el.x - x) <= _MOTION_TOLERANCE and abs(el.y - y) <= _MOTION_TOLERANCE and abs(el.angle - angle) <= _ANGLE_TOLERANCE


@rubricgrader
def grader(input: GraderInput):
    project = ExcalidrawProject(input["snapshots"]["excalidraw"])

    elements = project.get_all_elements()
    
    # read seed.json
    with open(Path(__file__).parent / "seed.json") as f:
        seed_data = json.load(f)
        
    diamond_x = diamond_y = diamond_width = diamond_height = diamond_angle = None
    base_x = base_y = base_width = base_angle = None

    for el in seed_data["elements"]:
        seed_element = el
        seed_x = seed_element["x"]
        seed_y = seed_element["y"]
        seed_angle = seed_element["angle"]
        seed_width = seed_element["width"]
        seed_height = seed_element["height"]
        seed_stroke_color = seed_element["strokeColor"]
        seed_background_color = seed_element["backgroundColor"]
        seed_text = seed_element.get("text", "")
        seed_item_name = seed_element["meta_label"]
        
        element = project.get_element_by_id(seed_element["id"])
        e_x = element.x if element else None
        e_y = element.y if element else None
        e_angle = element.angle if element else None
        e_width = element.width if element else None
        e_height = element.height if element else None
        e_stroke_color = element.stroke_color if element else None
        e_background_color = element.background_color if element else None
        e_text = element.text if element else None
        
        rubrics.assertTrue(f"seed_{seed_item_name}_preserved", element is not None,
            success=f"Project still has element {seed_item_name}",
            failure=f"Element {seed_item_name} removed from the project."
        )
        
        rubrics.assertTrue(f"seed_{seed_item_name}_size_preserved", _size_unchanged(element, seed_width, seed_height) if element else False,
            success=f"Element {seed_item_name} preserved size (width={seed_width}, height={seed_height})",
            failure=f"Expected element {seed_item_name} to have size (width={seed_width}, height={seed_height}), got (width={e_width}, height={e_height})"
        )
        
        rubrics.assertTrue(f"seed_{seed_item_name}_color_preserved", element and e_stroke_color == seed_stroke_color and e_background_color == seed_background_color,
            success=f"Element {seed_item_name} preserved color (stroke={seed_stroke_color}, background={seed_background_color})",
            failure=f"Expected element {seed_item_name} to have color (stroke={seed_stroke_color}, background={seed_background_color}), got (stroke={e_stroke_color}, background={e_background_color})"
        )
        
        if seed_item_name != "diamond":
            rubrics.assertTrue(f"seed_{seed_item_name}_position_preserved", _position_unchanged(element, seed_x, seed_y, seed_angle) if element else False,
                success=f"Element {seed_item_name} preserved position (x={seed_x}, y={seed_y}, angle={seed_angle})",
                failure=f"Expected element {seed_item_name} to have position (x={seed_x}, y={seed_y}, angle={seed_angle}), got (x={e_x}, y={e_y}, angle={e_angle})"
            )
        else:
            diamond_x = e_x
            diamond_y = e_y
            diamond_width = e_width
            diamond_height = e_height
            diamond_angle = e_angle
        if seed_item_name and seed_item_name.endswith("_text"):
            rubrics.assertTrue(f"seed_label_{seed_item_name}_preserved", e_text == seed_text,
                success=f"Element {seed_item_name} preserved text ({seed_text})",
                failure=f"Expected element {seed_item_name} to have text ({seed_text}), got ({e_text})"
            )
        if seed_item_name == "base":
            base_x = e_x
            base_y = e_y
            base_width = e_width
            base_angle = e_angle
            
    
    is_balanced = True
    if None in (diamond_x, diamond_y, diamond_width, diamond_height, diamond_angle, base_x, base_y, base_width, base_angle):
        is_balanced = False
    else:
        if not (abs(_DEFAULT_ANGLE - diamond_angle) <= _ANGLE_TOLERANCE and abs(_DEFAULT_ANGLE - base_angle) <= _ANGLE_TOLERANCE):
            is_balanced = False
        if not (base_x - _MOTION_TOLERANCE < diamond_x + diamond_width / 2 < base_x + base_width + _MOTION_TOLERANCE):
            is_balanced = False
        if not (base_y - _MOTION_TOLERANCE <= diamond_y + diamond_height <= base_y + _MOTION_TOLERANCE):
            is_balanced = False
        
    rubrics.assertTrue("seed_diamond_is_balanced_on_base", is_balanced,
        success="The diamond is successfully balanced on the base.",
        failure="The diamond is not balanced on the base."
    )


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "seed.json"
    with open(path) as f:
        data = json.load(f)
    result = grader({"snapshots": {"excalidraw": data}, "transcript": "", "extra_fields": {}, "posted_answer": None})
    print(f"result={result['result']}")
    for k, v in result["metadata"]["rubrics"].items():
        print(f"  {'PASS' if v['pass'] else 'FAIL'} {k}: {v.get('message') or v.get('description', '')}")
