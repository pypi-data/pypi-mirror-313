from __future__ import annotations

import uuid
import lightningchart
from lightningchart.series import Series2D

class RectangleSeries(Series2D):
    """Series for visualizing rectangles in a 2D space."""

    def __init__(self, chart):
        Series2D.__init__(self, chart)
        self.instance.send(self.id, 'addRectangleSeries', {'chart': self.chart.id})

    def add(self, x1: int | float, y1: int | float, x2: int | float, y2: int | float):
        """Add new figure to the series.

        Args:
            x1: X coordinate of rectangles bottom-left corner.
            y1: Y coordinate of rectangles bottom-left corner.
            x2: X coordinate of rectangles top-right corner.
            y2: Y coordinate of rectangles top-right corner.

        Returns:
            The instance of the class for fluent interface.
        """
        rectangle_figure = RectangleFigure(self, {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})
        return rectangle_figure

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

class RectangleFigure:
    """Class representing a visual rectangle figure in the RectangleSeries."""

    def __init__(self, series: RectangleSeries, dimensions: dict):
        self.series = series
        self.dimensions = dimensions
        self.instance = series.instance
        self.id = str(uuid.uuid4())  
        self.instance.send(self.id, 'addRectangleFigure', {'series': self.series.id, 'dimensions': dimensions})

    def set_stroke(self, thickness: int | float, color: lightningchart.Color):
        """Set Stroke style of the figure.

        Args:
            thickness (int | float): Thickness of the stroke.
            color (Color): Color of the stroke.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setStrokeStyle', {'thickness': thickness, 'color': color.get_hex()})
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

    def set_dimensions(self, x1: int | float, y1: int | float, x2: int | float, y2: int | float):
        """Set new dimensions for figure.

        Args:
            x1: X coordinate of rectangles bottom-left corner.
            y1: Y coordinate of rectangles bottom-left corner.
            x2: X coordinate of rectangles top-right corner.
            y2: Y coordinate of rectangles top-right corner.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setDimensions', {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})
        return self
    
    def set_color(self, color: lightningchart.Color):
        """Set a color of the rectangle figure.

        Args:
            color (Color): Color of the band.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setSolidFillStyle', {'color': color.get_hex()})
        return self
