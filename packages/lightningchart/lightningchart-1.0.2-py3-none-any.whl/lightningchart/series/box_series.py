from __future__ import annotations

import uuid
import lightningchart
from lightningchart.charts import Chart
from lightningchart.ui.axis import Axis
from lightningchart.series import Series2D, Series
from lightningchart.utils import convert_to_dict


class BoxSeries(Series2D):
    """Series type for visualizing data groups through quartiles."""

    def __init__(
            self,
            chart: Chart,
            x_axis: Axis = None,
            y_axis: Axis = None
    ):
        Series.__init__(self, chart)
        self.instance.send(self.id, 'boxSeries2D', {
            'chart': self.chart.id,
            'xAxis': x_axis,
            'yAxis': y_axis
        })

    def add(
            self,
            start: int | float,
            end: int | float,
            median: int | float,
            lower_quartile: int | float,
            upper_quartile: int | float,
            lower_extreme: int | float,
            upper_extreme: int | float
    ):
        """Add new figure to the series.

        Args:
            start (int | float): Start x-value.
            end (int | float): End x-value.
            median (int | float): Median y-value.
            lower_quartile (int | float): Lower quartile y-value.
            upper_quartile (int | float): Upper quartile y-value.
            lower_extreme (int | float): Lower extreme y-value.
            upper_extreme (int | float): Upper extreme y-value.

        Returns:
            BoxFigure instance.
        """
        box = BoxFigure(self, {
            'start': start,
            'end': end,
            'median': median,
            'lowerQuartile': lower_quartile,
            'upperQuartile': upper_quartile,
            'lowerExtreme': lower_extreme,
            'upperExtreme': upper_extreme
        })
        return box

    def add_multiple(self, data: list[dict]):
        """Add multiple figures to the series.

        Args:
            data: list of {start, end, median, lowerQuartile, upperQuartile, lowerExtreme, upperExtreme} objects

        Returns:
            The instance of the class for fluent interface.
        """
        data = convert_to_dict(data)

        self.instance.send(self.id, 'addMultipleBox2D', {'data': data})
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

class BoxFigure:
    """Class representing a visual box figure in the BoxSeries."""

    def __init__(self, series: BoxSeries, dimensions: dict):
        self.series = series
        self.dimensions = dimensions
        self.instance = series.instance
        self.id = str(uuid.uuid4())
        self.instance.send(self.id, 'addBoxFigure', {'series': self.series.id, 'dimensions': dimensions})

    def set_stroke(self, thickness: int | float, color: lightningchart.Color):
        """Set Stroke style of the box whiskers and tails.

        Args:
            thickness (int | float): Thickness of the stroke.
            color (Color): Color of the stroke.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setStrokeStyle', {'thickness': thickness, 'color': color.get_hex()})
        return self

    def set_body_width(self, width: int | float):
        """Set width of box body as a % of the width of its interval width.

        Args:
            width: Ratio between box body width and the segments interval

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setBodyWidth', {'width': width})
        return self

    def set_tail_width(self, width: int | float):
        """Set width of box tails as a % of the width of its interval width.

        Args:
            width: Ratio between box tail width and the segments interval

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTailWidth', {'width': width})
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

    def set_body_color(self, color: lightningchart.Color):
        """Set the color of the box body.

        Args:
            color: Color value.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setBodyFillStyle', {'color': color.get_hex()})
        return self

    def set_median_stroke(self, thickness: int | float, color: lightningchart.Color):
        """Set stroke style of Series median line.

        Args:
            thickness (int | float): Thickness of the stroke.
            color (Color): Color of the stroke.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setMedianStrokeStyle', {
            'thickness': thickness,
            'color': color.get_hex()
        })
        return self

    def set_body_stroke(self, thickness: int | float, color: lightningchart.Color):
        """Set border style of Series.

        Args:
            thickness (int | float): Thickness of the stroke.
            color (Color): Color of the stroke.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setBodyStrokeStyle', {
            'thickness': thickness,
            'color': color.get_hex()
        })
        return self
