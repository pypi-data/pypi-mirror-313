from __future__ import annotations

import lightningchart
from lightningchart.ui.axis import GenericAxis

class PolarAxis(GenericAxis):
    def __init__(self, chart):
        GenericAxis.__init__(self, chart)

    def set_stroke(self, thickness: int | float, color: lightningchart.Color):
        """Set Stroke style of the axis.

        Args:
            thickness (int | float): Thickness of the stroke.
            color (Color): Color of the stroke.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setStrokeStyle', {'thickness': thickness, 'color': color.get_hex()})
        return self
