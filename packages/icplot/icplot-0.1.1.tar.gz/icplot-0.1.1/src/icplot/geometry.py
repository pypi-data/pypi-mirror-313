from pydantic import BaseModel

from .color import Color


class Font(BaseModel):

    family: str = "Sans"
    weight: str = "normal"
    slant: str = "normal"
    size: float = 0.5


class SceneItem(BaseModel):

    item_type: str
    location: tuple[float, float] = (0.0, 0.0)


class Shape(SceneItem):

    item_type: str = "shape"
    fill: Color = Color()
    stroke: Color = Color()
    stroke_thickness: float = 0.5


class TextPath(SceneItem):

    item_type: str = "text"
    content: str
    font: Font = Font()


class Rectangle(Shape):

    item_type: str = "rect"
    w: float
    h: float


class Scene(BaseModel):

    items: list[SceneItem] = []
    size: tuple[int, int] = (100, 100)
