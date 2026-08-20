"""
Grader: Create Silver Chain

Verifies that an Excalidraw project contains a closed chain of 10 silver (#C0C0C0) circular ellipses

Rubrics:
- ten_ellipses_created: Project has exactly 10 ellipses
- ellipse_{idx}_is_circle: The ellipse number {idx} is a circle (width == height)
- ellipse_{idx}_is_silver: The ellipse number {idx} has a silver stroke color (#C0C0C0)
- ellipse_{idx}_size_matches_first: The ellipse number {idx} has the same size (width, height) as the first ellipse
- ellipse_{idx}_overlaps_two_ellipses: The ellipse number {idx} overlaps with exactly 2 other ellipses
- chain_with_10_ellipses_exists: The ellipses form a closed chain of 10 ellipses

Value mappings:
- "silver" -> #c0c0c0 (not in Excalidraw's default palette)
"""

from statistics import median
import sys
import json
from pathlib import Path

_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_root))

from curriculum.sdk import ExcalidrawProject
from curriculum import GraderInput, rubricgrader, rubrics

_ELLIPSE_COLOR = "#c0c0c0"  # silver, not in Excalidraw's default palette
_SIZE_TOLERANCE = 1.0  # px — absorbs float drift on save/reload, not enough to hide a resize


def _size_unchanged(el, width: float, height: float) -> bool:
    return abs(el.width - width) <= _SIZE_TOLERANCE and abs(el.height - height) <= _SIZE_TOLERANCE


@rubricgrader
def grader(input: GraderInput):
    project = ExcalidrawProject(input["snapshots"]["excalidraw"])

    elements = project.get_all_elements()
    n_elements = len(elements)
    ellipses = project.get_ellipses()
    n_ellipses = len(ellipses)

    rubrics.assertTrue("ten_ellipses_created", n_elements == 10 and n_ellipses == 10,
        success="Project has exactly 10 ellipses",
        failure=(
            f"Expected only 10 ellipses, got {n_ellipses} ellipses and {n_elements - n_ellipses} other elements"
            if n_ellipses != n_elements else
            f"Expected 10 ellipses, got {n_ellipses} — {n_ellipses - 10} extra ellipse(s) wrongfully added."
            if n_ellipses > 10 else
            f"Expected 10 ellipses, got {n_ellipses} — {10 - n_ellipses} missing ellipse(s)."
        )
    )
    
    default_diameter = median([ellipses[i].width for i in range(n_ellipses)]) if n_ellipses > 0 else None
    adjacency = [set() for _ in range(n_ellipses)]
    center_points = [(el.x + el.width / 2, el.y + el.height / 2) for el in ellipses]
    for i in range(n_ellipses):
        for j in range(i + 1, n_ellipses):
            if (
                (center_points[i][0] - center_points[j][0])**2 + (center_points[i][1] - center_points[j][1])**2
                < 
                (min(ellipses[i].width, ellipses[i].height) / 2 + min(ellipses[j].width, ellipses[j].height) / 2)**2
            ):
                adjacency[i].add(j)
                adjacency[j].add(i)
    
    
    for idx, el in enumerate(ellipses):
        rubrics.assertTrue(f"ellipse_{idx}_is_circle", _size_unchanged(el, el.height, el.height),
            success=f"Ellipse number {idx} is a circle (width == height)",
            failure=(
                f"Expected ellipse number {idx} to be a circle (width == height), got width={el.width}, height={el.height}"
            )
        )
        rubrics.assertTrue(f"ellipse_{idx}_is_silver", el.stroke_color.lower() == _ELLIPSE_COLOR.lower(),
            success=f"Ellipse number {idx} has a silver stroke color ({_ELLIPSE_COLOR})",
            failure=(
                f"Expected ellipse number {idx} to have a silver stroke color ({_ELLIPSE_COLOR}), got ({el.stroke_color})"
            )
        )
        rubrics.assertTrue(f"ellipse_{idx}_size_matches_first", _size_unchanged(el, default_diameter, default_diameter),
            success=f"Ellipse number {idx} has the same size as the first ellipse",
            failure=(
                f"Expected ellipse number {idx} to have the same size as the first ellipse, got width={el.width}, height={el.height}"
            )
        )
        rubrics.assertTrue(f"ellipse_{idx}_overlaps_two_ellipses", len(adjacency[idx]) == 2,
            success=f"Ellipse number {idx} overlaps with exactly 2 other ellipses",
            failure=(
                f"Expected ellipse number {idx} to overlap with exactly 2 other ellipses, got {len(adjacency[idx])}"
            )
        )
    
    visited = set()
    chain_length = 0
    closed_chain_found = False
    if len(adjacency) > 0 and len(adjacency[0]) > 0:
        previous = None
        current = 0
        while True:
            visited.add(current)
            chain_length += 1
            
            neighbors = adjacency[current]
            next_ellipses = [n for n in neighbors if n != previous]
            if previous is None and len(next_ellipses) == 2:
                next_node = next_ellipses[0]
            elif len(next_ellipses) == 1:
                next_node = next_ellipses[0]
            else:
                break
            
            if next_node in visited:
                if next_node == 0:
                    closed_chain_found = True
                break
            
            previous = current
            current = next_node
        
    rubrics.assertTrue("chain_with_10_ellipses_exists", closed_chain_found and chain_length == 10,
        success="The ellipses form a closed chain of 10 ellipses",
        failure=(
            f"Expected the ellipses to form a closed chain of 10 ellipses, got no closed chain"
            if not closed_chain_found else
            f"Expected the ellipses to form a closed chain of 10 ellipses, got a clsoed chain of length {chain_length}"
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
