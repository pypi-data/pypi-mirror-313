from __future__ import annotations

import uuid
import lightningchart
from lightningchart.series import Series2D

class SegmentSeries(Series2D):
    """Series for visualizing Segments in a 2D space."""

    def __init__(self, chart):
        Series2D.__init__(self, chart)
        self.instance.send(self.id, 'addSegmentSeries', {'chart': self.chart.id})

    def add_segment(self, start_x: int | float, start_y: int | float, end_x: int | float, end_y: int | float):
        """Add new figure to the series.

        Args:
            start_x: X value of start location
            start_y: Y value of start location
            end_x: X value of end location
            end_y: Y value of end location

        Returns:
            The instance of the class for fluent interface.
        """
        segment_figure = SegmentFigure(self, {'startX': start_x, 'startY': start_y, 'endX': end_x, 'endY': end_y})
        return segment_figure

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

class SegmentFigure:
    """Class representing a visual segment figure in the RectangleSeries."""

    def __init__(self, series: SegmentSeries, dimensions: dict):
        self.series = series
        self.dimensions = dimensions
        self.instance = series.instance
        self.id = str(uuid.uuid4())  
        self.instance.send(self.id, 'addSegmentFigure', {'series': self.series.id, 'dimensions': dimensions})

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

    def set_dimensions(self, start_x: float, start_y: float, end_x: float, end_y: float):
        """Set new dimensions for figure.

        Args:
            start_x: X value of start location
            start_y: Y value of start location
            end_x: X value of end location
            end_y: Y value of end location

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setDimensionsSegment', {
            'startX': start_x,
            'startY': start_y,
            'endX': end_x,
            'endY': end_y
        })
        return self
