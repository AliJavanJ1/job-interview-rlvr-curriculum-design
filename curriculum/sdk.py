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

    def is_rectangle(self) -> bool:
        return self.type == "rectangle"

    def is_ellipse(self) -> bool:
        return self.type == "ellipse"

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
