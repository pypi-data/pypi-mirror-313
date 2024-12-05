from __future__ import annotations
from lightningchart.ui import UIEWithPosition, UIEWithTitle, UIElement


class Legend(UIEWithPosition, UIEWithTitle):
    """Class for legend boxes in a chart."""

    def __init__(
            self,
            chart,
            horizontal: bool = False,
            title: str = None,
            data=None,
            x: int = None,
            y: int = None,
            position_scale: str = 'percentage',
    ):
        UIElement.__init__(self, chart)
        self.instance.send(self.id, 'legend', {
            'chart': chart.id,
            'horizontal': horizontal,
            'positionScale': position_scale,
        })
        if title:
            self.set_title(title)
        if data:
            self.add(data)
        if x and y:
            self.set_position(x, y)

    def add(self, data):
        """Add a dynamic value to LegendBox, creating a group and entries for it depending on type of value.
        Supports series, charts and dashboards.

        Args:
            data: Series | Chart | Dashboard | UIElement

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'legendAdd', {'chart': data.id})
        return self

    def set_font_size(self, font_size: int | float):
        """Set the font size of legend entries.

        Args:
            font_size (int | float): Font size of the entries.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setLegendFontSize', {'size': font_size})
        return self

    def set_padding(self, padding: int | float):
        """Set padding around Chart in pixels.

        Args:
            padding (int | float): Number with pixel margins for all sides.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setPadding', {'padding': padding})
        return self
