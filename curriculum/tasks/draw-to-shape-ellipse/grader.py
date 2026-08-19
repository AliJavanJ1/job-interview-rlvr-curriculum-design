"""
Grader: An ellipse drawn on an empty canvas using "Draw to shape" option.

Verifies that an Excalidraw project contains an ellipse drawn on an empty canvas with version number exactly 2 which means that the ellipse was drawn using "Draw to shape" option without any further modifications.

Rubrics:
- only_one_element_exists: The project contains exactly one new element.
- element_is_ellipse: The new element is an ellipse.
- ellipse_is_big_enough_to_be_visible: The ellipse is big enough to be visible (width and height are at least 5).
- ellipse_is_drawn_to_shape_without_further_modifications: The ellipse was drawn using "Draw to shape" option (version number is exactly 2)

"""

import sys
import json
from pathlib import Path

_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_root))

from curriculum.sdk import ExcalidrawProject
from curriculum import GraderInput, rubricgrader, rubrics

_MIN_ELLIPSE_WIDTH = 5
_MIN_ELLIPSE_HEIGHT = 5
_EXPECTED_ELLIPSE_VERSION = 2

@rubricgrader
def grader(input: GraderInput):
    project = ExcalidrawProject(input["snapshots"]["excalidraw"])

    elements = project.get_all_elements()
    n_elements = len(elements)
    ellipses = project.get_ellipses()
    n_ellipses = len(ellipses)

    element = elements[0] if n_elements == 1 else None
    element_type = element.type if element else None
    ellipse = ellipses[0] if n_ellipses  == 1 else None
    ellipse_width = ellipse.width if ellipse else None
    ellipse_height = ellipse.height if ellipse else None
    ellipse_version = ellipse.version if ellipse else None
    
    rubrics.assertTrue("only_one_element_exists", n_elements == 1,
        success="Project contains exactly one new element",
        failure=(
            f"No new element found in the project." 
            if n_elements == 0 else
            f"Expected 1 element, got {n_elements} — {n_elements - 1} extra element(s) wrongfully added."
        )
    )
    
    rubrics.assertTrue("element_is_ellipse", ellipse is not None,
        success="New element is an ellipse",
        failure=(
            "No new element found to check if it is an ellipse."
            if not element else
            f"Expected new element to be an ellipse, got {element_type} instead."
        )
    )
    
    rubrics.assertTrue("ellipse_is_big_enough_to_be_visible",
        ellipse and ellipse_width >= _MIN_ELLIPSE_WIDTH and ellipse_height >= _MIN_ELLIPSE_HEIGHT,
        success="Ellipse is big enough to be visible (width and height are at least 5)",
        failure=(
            "No ellipse found to check if it is big enough to be visible. (width and height are at least 5)"
            if not ellipse else
            f"Ellipse is too small to be visible — expected both width and height to be at least 5, got {ellipse_width}x{ellipse_height}"
            if ellipse_width < _MIN_ELLIPSE_WIDTH and ellipse_height < _MIN_ELLIPSE_HEIGHT else
            f"Ellipse height is big enough but width is too small — expected both width and height to be at least 5, got {ellipse_width}x{ellipse_height}"
            if ellipse_width < _MIN_ELLIPSE_WIDTH else
            f"Ellipse width is big enough but height is too small — expected height to be at least 5, got {ellipse_width}x{ellipse_height}"
        )
    )
    
    
    rubrics.assertTrue("ellipse_is_drawn_to_shape_without_further_modifications",
        ellipse.version == _EXPECTED_ELLIPSE_VERSION if ellipse else False,
        success="The ellipse was drawn using 'Draw to shape' option without further modifications (version number is exactly 2)",
        failure=(
            "No ellipse present to check version."
            if not ellipse else
            f"Expected ellipse version to be {_EXPECTED_ELLIPSE_VERSION} (drawn using 'Draw to shape' option without further modifications), got {ellipse_version} — it was modified after drawing or not drawn using 'Draw to shape' option."
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
