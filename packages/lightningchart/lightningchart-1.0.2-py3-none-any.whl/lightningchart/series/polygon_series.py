from __future__ import annotations

import uuid
import lightningchart
from lightningchart.series import Series2D
from lightningchart.utils import convert_to_dict


class PolygonSeries(Series2D):
    """Series for visualizing polygons in a 2D space."""

    def __init__(self, chart):
        Series2D.__init__(self, chart)
        self.instance.send(self.id, 'addPolygonSeries', {'chart': self.chart.id})

    def add(self, points: list[dict]):
        """Add new figure to the series.

        Args:
            points: Dimensions that figure must represent

        Returns:
            The instance of the class for fluent interface.
        """
        points = convert_to_dict(points)

        polygon_figure = PolygonFigure(self, points)
        return polygon_figure

    def set_highlight_on_hover(self, enabled: bool):
        """Set highlight on mouse hover enabled or disabled.

        Args:
            enabled: Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setHighlightOnHover', {'enabled': enabled})
        return self
    
    def set_draw_order(self, index: int):
        """Configure draw order of the series.

        Args:
            index: Draw order index.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setDrawOrder', {'index': index})
        return self
    
    def set_name(self, name: str):
        """Sets the name of the component for Legend.

        Args:
            name: Name of the Component.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setName', {'name': name})
        return self

class PolygonFigure:
    """Class representing a visual polygon figure in the PolygonSeries."""

    def __init__(self, series: PolygonSeries, points: list[dict]):
        self.series = series
        self.points = points
        self.instance = series.instance
        self.id = str(uuid.uuid4())
        self.instance.send(self.id, 'addPolygonFigure', {'series': self.series.id, 'points': points})

    def set_stroke(self, thickness: int | float, color: lightningchart.Color):
        """Set Stroke style of the polygon.

        Args:
            thickness (int | float): Thickness of the stroke.
            color (Color): Color of the stroke.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setStrokeStyle', {'thickness': thickness, 'color': color.get_hex()})
        return self

    def set_dimensions(self, points: list[dict]):
        """Set new dimensions for figure.

        Args:
            points: List of polygon coordinates

        Returns:
            The instance of the class for fluent interface.
        """
        points = convert_to_dict(points)

        self.instance.send(self.id, 'setDimensionsPolygon', {'points': points})
        return self

    def set_visible(self, visible: bool):
        """Set element visibility.

        Args:
            visible: Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setVisible', {'visible': visible})
        return self
    
    def set_mouse_interactions(self, enabled: bool):
        """Set mouse interactions enabled or disabled

        Args:
            enabled: Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setMouseInteractions', {'enabled': enabled})
        return self
    
    def set_color(self, color: lightningchart.Color):
        """Set a color of the polygon.

        Args:
            color (Color): Color of the band.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setSolidFillStyle', {'color': color.get_hex()})
        return self
