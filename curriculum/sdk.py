"""sdk.py — Excalidraw grading helpers."""

from __future__ import annotations

from typing import Any


class ExcalidrawElement:
    """Wrapper around an Excalidraw element."""

    def __init__(self, data: dict[str, Any]):
        self._data = data

    @property
    def type(self) -> str:
        return self._data.get("type", "")

    @property
    def id(self) -> str:
        return self._data.get("id", "")

    @property
    def x(self) -> float:
        return self._data.get("x", 0)

    @property
    def y(self) -> float:
        return self._data.get("y", 0)
    
    @property
    def angle(self) -> float:
        return self._data.get("angle", 0)

    @property
    def width(self) -> float:
        return self._data.get("width", 0)

    @property
    def height(self) -> float:
        return self._data.get("height", 0)

    @property
    def background_color(self) -> str:
        return self._data.get("backgroundColor", "")

    @property
    def stroke_color(self) -> str:
        return self._data.get("strokeColor", "")
    
    @property
    def version(self) -> int:
        return self._data.get("version", 0)

    def is_rectangle(self) -> bool:
        return self.type == "rectangle"
    
    def is_diamond(self) -> bool:
        return self.type == "diamond"

    def is_ellipse(self) -> bool:
        return self.type == "ellipse"
    
    def is_arrow(self) -> bool:
        return self.type == "arrow"
    
    def is_line(self) -> bool:
        return self.type == "line"
    
    def is_freedraw(self) -> bool:
        return self.type == "freedraw"
    
    def is_text(self) -> bool:
        return self.type == "text"
    
    def is_image(self) -> bool:
        return self.type == "image"
    
    def is_frame(self) -> bool:
        return self.type == "frame"
    
    def is_embeddable(self) -> bool:
        return self.type == "embeddable"
    
    def is_magicframe(self) -> bool:
        return self.type == "magicframe"
    

    def has_background_color(self, hex_color: str) -> bool:
        return self.background_color.lower() == hex_color.lower()

    def is_within(self, other: "ExcalidrawElement") -> bool:
        """Return True if this element is fully contained within other."""
        return (
            self.x >= other.x
            and self.y >= other.y
            and self.x + self.width <= other.x + other.width
            and self.y + self.height <= other.y + other.height
        )


class ExcalidrawProject:
    """Wrapper for an Excalidraw project snapshot."""

    def __init__(self, data: dict[str, Any]):
        self._elements = [
            ExcalidrawElement(el)
            for el in data.get("elements", [])
            if not el.get("isDeleted", False)
        ]

    def get_rectangles(self) -> list[ExcalidrawElement]:
        return [el for el in self._elements if el.is_rectangle()]

    def get_ellipses(self) -> list[ExcalidrawElement]:
        return [el for el in self._elements if el.is_ellipse()]
    
    def get_all_elements(self) -> list[ExcalidrawElement]:
        return [el for el in self._elements]
    
    def get_element_by_id(self, element_id: str) -> ExcalidrawElement | None:
        for el in self._elements:
            if el.id == element_id:
                return el
        return None
