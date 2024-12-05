from __future__ import annotations

import uuid
import lightningchart
from lightningchart.series import Series2D

class EllipseSeries(Series2D):
    """Series for visualizing ellipses in a 2D space."""

    def __init__(self, chart):
        Series2D.__init__(self,chart)
        self.instance.send(self.id, 'addEllipseSeries', {'chart': self.chart.id})

    def add(self, x: int | float, y: int | float, radius_x: int | float, radius_y: int | float):
        """Add new figure to the series.

        Args:
            x: x-axis coordinate.
            y: y-axis coordinate.
            radius_x: x-axis radius.
            radius_y: y-axis radius.

        Returns:
            The instance of the class for fluent interface.
        """
        ellipse_figure = EllipseFigure(self, {
            'x': x,
            'y': y,
            'radiusX': radius_x,
            'radiusY': radius_y
        })
        return ellipse_figure

    def set_animation_highlight(self, enabled: bool):
        """Set component highlight animations enabled or not.

        Args:
            enabled: Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setAnimationHighlight', {'enabled': enabled})
        return self

    def set_effect(self, enabled: bool):
        """Set theme effect enabled on component or disabled.

        Args:
            enabled: Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setEffect', {'enabled': enabled})
        return self
    
    def set_auto_scrolling_enabled(self, enabled: bool):
        """Set whether series is taken into account with automatic scrolling and fitting of attached axes.

        Args:
            enabled: Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setAutoScrollingEnabled', {'enabled': enabled})
        return self

    def set_highlight_on_hover(self, enabled: bool):
        """Set highlight on mouse hover enabled or disabled.

        Args:
            enabled: Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setHighlightOnHover', {'enabled': enabled})
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

    def set_cursor_enables(self, enabled: bool):
        """Configure whether cursors should pick on this particular series or not.

        Args:
            enabled: Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setCursorEnabled', {'enabled': enabled})

class EllipseFigure:
    """Class representing a visual ellipse figure in the EllipseSeries."""

    def __init__(self, series: EllipseSeries, dimensions: dict):
        self.series = series
        self.dimensions = dimensions
        self.instance = series.instance
        self.id = str(uuid.uuid4())  
        self.instance.send(self.id, 'addEllipseFigure', {'series': self.series.id, 'dimensions': dimensions})

    def set_stroke(self, thickness: int | float, color: lightningchart.Color):
        """Set Stroke style of the ellipse

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
    
    def set_dimensions(self, x: int | float, y: int | float, radius_x: int | float, radius_y: int | float):
        """Set new dimensions for figure.

        Args:
            x: x coordinate.
            y: y coordinate.
            radius_x: x radius.
            radius_y: y radius.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setDimensionsEllipse', {
            'x': x,
            'y': y,
            'radiusX': radius_x,
            'radiusY': radius_y
        })
        return self
    
    def set_color(self, color: lightningchart.Color):
        """Set a color of the ellipse figure.

        Args:
            color (Color): Color of the band.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setSolidFillStyle', {'color': color.get_hex()})
        return self
