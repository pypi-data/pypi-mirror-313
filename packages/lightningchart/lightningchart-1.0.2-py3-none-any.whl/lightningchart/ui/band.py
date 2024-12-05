from __future__ import annotations

import lightningchart
from lightningchart.ui import UIElement, UIEWithHighlight


class Band(UIEWithHighlight):

    def __init__(self, chart, axis, on_top: bool):
        UIElement.__init__(self, chart)
        self.instance.send(self.id, 'addBand', {'axis': axis.id, 'onTop': on_top})

    def set_value_start(self, value_start: int | float):
        """Set start value of Band. This is in values of its owning Axis.

        Args:
            value_start (int | float): Value on Axis.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setValueStart', {'valueStart': value_start})
        return self

    def set_value_end(self, value_end: int | float):
        """Set end value of Band. This is in values of its owning Axis.

        Args:
            value_end (int | float): Value on Axis.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setValueEnd', {'valueEnd': value_end})
        return self

    def set_color(self, color: lightningchart.Color):
        """Set a color of the band.

        Args:
            color (Color): Color of the band.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setSolidFillStyle', {'color': color.get_hex()})
        return self

    def set_stroke(self, thickness: int | float, color: lightningchart.Color):
        """Set stroke style of Band.

        Args:
            thickness (int | float): Thickness of the stroke.
            color (Color): Color of the stroke.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setStrokeStyle', {'thickness': thickness, 'color': color.get_hex()})
        return self

    def set_name(self, name: str):
        """Sets the name of the Component updating attached LegendBox entries.

        Args:
            name (str): Name of the component.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setName', {'name': name})
        return self
