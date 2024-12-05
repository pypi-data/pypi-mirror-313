from __future__ import annotations

import lightningchart
from lightningchart.ui import UIElement, UIEWithHighlight


class ConstantLine(UIEWithHighlight):

    def __init__(self, chart, axis, on_top: bool):
        UIElement.__init__(self, chart)
        self.instance.send(self.id, 'addConstantLine', {'axis': axis.id, 'onTop': on_top})

    def set_interaction_move_by_dragging(self, enabled: bool):
        """Enable or disable default interaction of moving constant line by dragging with mouse or touch.

        Args:
            enabled (bool): Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setInteractionMoveByDragging', {'enabled': enabled})
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

    def set_stroke(self, thickness: int | float, color: lightningchart.Color):
        """Set the Axis line stroke.

        Args:
            thickness (int | float): Thickness of the stroke.
            color (Color): Color of the stroke.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setStrokeStyle', {'thickness': thickness, 'color': color.get_hex()})
        return self

    def set_value(self, value: int | float):
        """Set value of ConstantLine. This is in values of its owning Axis.

        Args:
            value (int | float): Value on Axis.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setValue', {'value': value})
        return self
