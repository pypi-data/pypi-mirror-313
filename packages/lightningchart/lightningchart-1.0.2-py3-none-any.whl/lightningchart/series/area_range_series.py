from __future__ import annotations

import lightningchart
from lightningchart.charts import Chart
from lightningchart.ui.axis import Axis
from lightningchart.series import Series2D, SeriesWithAddDataPoints, SeriesWithDataCleaning, Series, \
    ComponentWithRangePaletteColoring
from lightningchart.utils import convert_to_list


class AreaRangeSeries(
    Series2D,
    SeriesWithAddDataPoints,
    SeriesWithDataCleaning,
    ComponentWithRangePaletteColoring
):
    """Series for visualizing 2D areas with ranges."""

    def __init__(
            self,
            chart: Chart,
            x_axis: Axis = None,
            y_axis: Axis = None
    ):
        Series.__init__(self, chart)
        self.instance.send(self.id, 'areaRangeSeries', {
            'chart': self.chart.id,
            'xAxis': x_axis,
            'yAxis': y_axis
        })

    def add_arrays_high_low(
            self,
            high: list[int | float],
            low: list[int | float],
            start: int | float = 0,
            step: int | float = 1
    ):
        """Add two individual Arrays, one for high values, and another for low values.

        Args:
            high (list[int | float]): List of high values.
            low (list[int | float]): List of low values. Length should be equal to length of high.
            start (int | float): Start index of x-axis.
            step (int | float: The step length for x-axis.

        Returns:
            The instance of the class for fluent interface.
        """
        high = convert_to_list(high)
        low = convert_to_list(low)

        self.instance.send(self.id, 'addArraysHighLow', {
            'high': high,
            'low': low,
            'step': step,
            'start': start
        })
        return self

    def set_high_fill_color(self, color: lightningchart.Color):
        """Set the high area style of the Series.

        Args:
            color (Color): Color of the high area.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setHighFillStyle', {'color': color.get_hex()})
        return self

    def set_high_stroke(self, thickness: int | float, color: lightningchart.Color):
        """Set the high stroke style of the Series.

        Args:
            thickness (int | float): Thickness of the high stroke.
            color (Color): Color of the high stroke.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setHighStrokeStyle', {'thickness': thickness, 'color': color.get_hex()})
        return self

    def set_low_fill_color(self, color: lightningchart.Color):
        """Set the low area style of the Series.

        Args:
            color (Color): Color of the low area.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setLowFillStyle', {'color': color.get_hex()})
        return self

    def set_low_stroke(self, thickness: int | float, color: lightningchart.Color):
        """Set the low stroke style of the Series.

        Args:
            thickness (int | flaot): Thickness of the low stroke.
            color (Color): Color of the low stroke.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setLowStrokeStyle', {'thickness': thickness, 'color': color.get_hex()})
        return self
