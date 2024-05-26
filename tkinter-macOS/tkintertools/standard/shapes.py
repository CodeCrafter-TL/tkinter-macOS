"""All standard Shapes"""

import math
import warnings

from .. import core


class Line(core.Shape):
    """"""

    def __init__(
        self,
        widget: core.Widget,
        rel_position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        name: str | None = None,
        width: int = 0,
        points: list[tuple[float, float]] = [],
        animation: bool = True,
        styles: dict[str | int, dict[str | int, dict[str, str]]] | None = None
    ) -> None:
        self.points = points
        self.width = width
        core.Shape.__init__(self, widget, rel_position, size,
                            name=name, styles=styles, animation=animation)

    def display(self) -> None:
        points = [(x+self.x, y+self.y) for x, y in self.points]
        self.items = [self.widget.master.create_line(
            *points, tags=("fill", "fill"), width=self.width)]


class Rectangle(core.Shape):
    """"""

    def display(self) -> None:
        self.items = [self.widget.master.create_rectangle(
            *self.region(), tags=("fill", "fill", "outline", "outline"))]


class Oval(core.Shape):
    """"""

    def display(self) -> None:
        self.items = [self.widget.master.create_oval(
            *self.region(), tags=("fill", "fill", "outline", "outline"))]


class RegularPolygon(core.Shape):
    """"""

    def __init__(
        self,
        widget: core.Widget,
        rel_position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        name: str | None = None,
        animation: bool = True,
        styles: dict[str, dict[str, str]] | None = None,
        side: int = 3,
        angle: float = 0,
    ) -> None:
        self.side = side
        self.angle = angle
        core.Shape.__init__(self, widget, rel_position, size,
                            name=name, styles=styles, animation=animation)

    def display(self) -> None:
        r = min(self.w, self.h) / 2
        if self.side < 3:
            warnings.warn("Parameters are not suitable")
        points = []
        for i in range(self.side):
            angle = math.tau*i/self.side+self.angle
            points.append(math.cos(angle)*r + self.x + self.w/2)
            points.append(math.sin(angle)*r + self.y + self.h/2)

        self.items = [self.widget.master.create_polygon(
            *points, tags=("fill", "fill", "outline", "outline"))]


class RoundedRectangle(core.Shape):
    """"""

    def __init__(
        self,
        widget: core.Widget,
        rel_position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        name: str | None = None,
        animation: bool = True,
        styles: dict[str, dict[str, str]] | None = None,
        radius: int = 5,
    ) -> None:
        self.radius = radius
        core.Shape.__init__(self, widget, rel_position, size,
                            name=name, styles=styles, animation=animation)

    def display(self) -> None:
        """"""
        x, y, w, h = self.x, self.y, self.w, self.h
        x1, y1, x2, y2 = x, y, x + w, y + h
        r, d = self.radius, self.radius*2

        if d > w or d > h:
            warnings.warn("Parameters are not suitable")
            warnings.warn("Parameters are not suitable")
        elif d == 0:
            warnings.warn("Parameters are not suitable")
        elif w < d < h or w < d < h:
            warnings.warn("Parameters are not suitable")
            warnings.warn("Parameters are not suitable")

        self.items = [
            self.widget.master.create_arc(
                x1, y1, x1+d, y1+d, outline="", start=90, tags=("fill", "fill")),
            self.widget.master.create_arc(
                x2-d, y1, x2, y1+d, outline="", start=0, tags=("fill", "fill")),
            self.widget.master.create_arc(
                x1, y2-d, x1+d, y2, outline="", start=180, tags=("fill", "fill")),
            self.widget.master.create_arc(
                x2-d, y2-d, x2, y2, outline="", start=-90, tags=("fill", "fill")),
            self.widget.master.create_rectangle(
                x1+r, y1, x2-r+1, y2, outline="", tags=("fill", "fill")),
            self.widget.master.create_rectangle(
                x1, y1+r, x2, y2-r+1, outline="", tags=("fill", "fill")),
            self.widget.master.create_line(
                x1+r, y1, x2-r+1, y1, tags=("fill", "outline")),
            self.widget.master.create_line(
                x1+r, y2, x2-r+1, y2, tags=("fill", "outline")),
            self.widget.master.create_line(
                x1, y1+r, x1, y2-r+1, tags=("fill", "outline")),
            self.widget.master.create_line(
                x2, y1+r, x2, y2-r+1, tags=("fill", "outline")),
            self.widget.master.create_arc(
                x1, y1, x1+d, y1+d, style="arc", start=90, tags=("outline", "outline")),
            self.widget.master.create_arc(
                x2-d, y1, x2, y1+d, style="arc", start=0, tags=("outline", "outline")),
            self.widget.master.create_arc(
                x1, y2-d, x1+d, y2, style="arc", start=180, tags=("outline", "outline")),
            self.widget.master.create_arc(
                x2-d, y2-d, x2, y2, style="arc", start=-90, tags=("outline", "outline")),
        ]


class SemicircularRectangle(core.Shape):
    """"""

    def display(self) -> None:
        """"""
        x, y, w, h = self.x, self.y, self.w, self.h
        x1, y1, x2, y2 = x, y, x + w, y + h
        d = h
        r = d/2

        if d < 0:
            warnings.warn("Parameters are not suitable")
        elif d == 0:
            warnings.warn("Parameters are not suitable")

        self.items = [
            self.widget.master.create_arc(
                x1, y1, x1+d, y1+d, outline="", extent=180, start=90, tags=("fill", "fill")),
            self.widget.master.create_arc(
                x2-d, y1, x2, y1+d, outline="", extent=180, start=-90, tags=("fill", "fill")),
            self.widget.master.create_rectangle(
                x1+r, y1, x2-r+1, y2, outline="", tags=("fill", "fill")),
            self.widget.master.create_arc(
                x1, y1, x1+d, y1+d, style="arc", extent=180, start=90, tags=("outline", "outline")),
            self.widget.master.create_arc(
                x2-d, y2-d, x2, y2, style="arc", extent=180, start=-90, tags=("outline", "outline")),
            self.widget.master.create_line(
                x1+r, y1, x2-r+1, y1, tags=("fill", "outline")),
            self.widget.master.create_line(
                x1+r, y2, x2-r+1, y2, tags=("fill", "outline")),
        ]


class SharpRectangle(core.Shape):
    """"""

    def __init__(
        self,
        widget: core.Widget,
        rel_position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        name: str | None = None,
        animation: bool = True,
        styles: dict[str, dict[str, str]] | None = None,
        theta: float = math.pi/6,
        ratio: tuple[float, float] = (0.5, 0.5),
    ) -> None:
        self.theta = theta
        self.ratio = ratio
        if not 0 <= theta <= math.pi/3:
            warnings.warn("Parameters are not suitable")
        if math.isclose(abs(self.ratio[0] - self.ratio[1]), 1):
            warnings.warn("Parameters are not suitable")
        core.Shape.__init__(self, widget, rel_position, size,
                            name=name, styles=styles, animation=animation)

    def display(self) -> None:
        """"""
        x, y, w, h = self.x, self.y, self.w, self.h

        if w < h:
            warnings.warn("Parameters are not suitable")

        dy = [h*value for value in self.ratio]
        dx = [math.tan(self.theta)*y for y in dy]

        if sum(dx) > w:
            warnings.warn("Parameters are not suitable")

        x1, y1, x2, y2 = x, y, x + w, y + h

        points = [
            x1, y1+dy[0],
            x1+dx[0], y1,
            x2-dx[1], y1,
            x2, y2-dy[1],
            x2-dx[1], y2,
            x1+dx[0], y2
        ]

        self.items = [self.widget.master.create_polygon(
            *points, tags=("fill", "fill", "outline", "outline"))]


class Parallelogram(core.Shape):
    """"""

    def __init__(
        self,
        widget: core.Widget,
        rel_position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        name: str | None = None,
        animation: bool = True,
        styles: dict[str, dict[str, str]] | None = None,
        theta: float = math.pi/6,
    ) -> None:
        self.theta = theta
        if not abs(theta) <= math.pi/3:
            warnings.warn("Parameters are not suitable")
        core.Shape.__init__(self, widget, rel_position, size,
                            name=name, styles=styles, animation=animation)

    def display(self) -> None:
        """"""
        x, y, w, h = self.x, self.y, self.w, self.h

        if (dx := h*math.tan(self.theta)) >= w:
            warnings.warn("Parameters are not suitable")

        x1, y1, x2, y2 = x, y, x + w, y + h

        points = [
            x1+dx, y1,
            x2, y1,
            x2-dx, y2,
            x1, y2
        ]

        self.items = [self.widget.master.create_polygon(
            *points, tags=("fill", "fill", "outline", "outline"))]
