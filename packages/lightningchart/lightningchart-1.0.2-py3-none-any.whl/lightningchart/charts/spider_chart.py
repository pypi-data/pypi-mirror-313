from __future__ import annotations
import uuid

import lightningchart
from lightningchart import conf, Themes, charts
from lightningchart.charts import GeneralMethods, TitleMethods, Chart
from lightningchart.instance import Instance
from lightningchart.utils import convert_to_dict


class SpiderChart(GeneralMethods, TitleMethods):

    def __init__(
            self,
            theme: Themes = Themes.White,
            title: str = None,
            license: str = None,
            license_information: str = None,
    ):
        """Chart for visualizing data in a radial form as dissected by named axes.

        Args:
            theme (Themes): Overall theme of the chart.
            title (str): Title of the chart.
            license (str): License key.
        """
        instance = Instance()
        Chart.__init__(self, instance)
        self.instance.send(self.id, 'spiderChart', {
            'theme': theme.value,
            'license': license or conf.LICENSE_KEY,
            'licenseInformation': license_information or conf.LICENSE_INFORMATION,
        })
        if title:
            self.set_title(title)

    def add_series(self):
        """Adds a new SpiderSeries to the SpiderChart.

        Returns:
            SpiderSeries instance.
        """
        series = SpiderSeries(self)
        return series

    def set_axis_interval(self, edge: int | float, center: int | float):
        """Set interval of Charts Axes

        Args:
            edge (int | float): Value at edges of chart.
            center (int | float): Value at center of chart. Defaults to zero.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setSpiderAxisInterval', {'edge': edge, 'center': center})
        return self

    def set_web_mode(self, mode: str = 'circle'):
        """Set mode of SpiderCharts web and background.

        Args:
            mode: "circle" | "normal"

        Returns:
            The instance of the class for fluent interface.
        """
        if mode == 'circle':
            mode = 1
        else:
            mode = 0
        self.instance.send(self.id, 'setWebMode', {'mode': mode})
        return self

    def set_series_background_effect(self, enabled: bool = True):
        """Set theme effect enabled on component or disabled.

        Args:
            enabled (bool): Theme effect enabled.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setSeriesBackgroundEffect', {'enabled': enabled})
        return self

    def add_axis(self, tag: str):
        """Add a new axis to Spider Chart.

        Args:
            tag (str): String tag for the axis.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'addSpiderAxis', {'tag': tag})
        return self

    def set_auto_axis_creation(self, enabled: bool):
        """Specifies if auto creation of axis is turned on or not.

        Args:
            enabled (bool): State of automatic axis creation.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setAutoAxis', {'enabled': enabled})
        return self

    def set_web_count(self, count: int):
        """Set count of 'webs' displayed.

        Args:
            count (int): Count of web lines.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setWebCount', {'count': count})
        return self

    def set_web_style(self, thickness: int | float, color: lightningchart.Color):
        """Set style of spider charts webs as LineStyle.

        Args:
            thickness (int | float): Thickness of the web lines.
            color (Color): Color of the web.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setWebStyle', {'thickness': thickness, 'color': color.get_hex()})
        return self

    def set_nib_length(self, length: int | float):
        """Set length of axis nibs in pixels.

        Args:
            length (int | float): Sum length of nibs in pixels (both directions).

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setNibLength', {'length': length})
        return self

    def set_nib_style(self, thickness: int | float, color: lightningchart.Color):
        """Set style of axis nibs.

        Args:
            thickness (int | float): Thickness of the nibs.
            color (Color): Color of the nibs.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setNibStyle', {'thickness': thickness, 'color': color.get_hex()})
        return self

    def set_axis_label_effect(self, enabled: bool):
        """Set theme effect enabled on component or disabled.

        Args:
            enabled (bool): Theme effect enabled.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setAxisLabelEffect', {'enabled': enabled})
        return self

    def set_axis_label_font(
            self,
            size: int | float,
            family: str = "Segoe UI, -apple-system, Verdana, Helvetica",
            style: str = 'normal',
            weight: str = 'normal'
    ):
        """Set font of axis labels.

        Args:
            size (int | float): CSS font size. For example, 16.
            family (str): CSS font family. For example, 'Arial, Helvetica, sans-serif'.
            weight (str): CSS font weight. For example, 'bold'.
            style (str): CSS font style. For example, 'italic'

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setAxisLabelFont', {
            'family': family,
            'size': size,
            'weight': weight,
            'style': style
        })
        return self

    def set_axis_label_padding(self, padding: int | float):
        """Set padding of axis labels.

        Args:
            padding (int | float): Padding in pixels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setAxisLabelPadding', {'padding': padding})
        return self

    def set_axis_label_color(self, color: lightningchart.Color):
        """Set the color of axis labels.

        Args:
            color (Color): Color of the labels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setAxisLabelStyle', {'color': color.get_hex()})
        return self

    def set_axis_scroll_strategy(self, strategy: str):
        """Sets the scroll strategy of charts axes.

        Args:
            strategy (str): "expansion" | "fitting" | "progressive" | "regressive" | "none"

        Returns:
            The instance of the class for fluent interface.
        """
        scroll_strategies = ("expansion", "fitting", "progressive", "regressive", "none")
        if strategy not in scroll_strategies:
            raise ValueError(
                f"Expected strategy to be one of {scroll_strategies}"
                f", but got '{strategy}'."
            )

        self.instance.send(self.id, 'setAxisScrollStrategy', {'strategy': strategy})
        return self

    def set_axis_style(self, thickness: int | float, color: lightningchart.Color):
        """Set the style of axis line.

        Args:
            thickness (int | float): Thickness of the axis line.
            color (Color): Color of the axis line.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setAxisStyle', {'thickness': thickness, 'color': color.get_hex()})
        return self

    def set_scale_label_font(
            self,
            size: int | float,
            family: str = "Segoe UI, -apple-system, Verdana, Helvetica",
            style: str = 'normal',
            weight: str = 'normal'
    ):
        """Set font of scale labels.

        Args:
            size (int | float): CSS font size. For example, 16.
            family (str): CSS font family. For example, 'Arial, Helvetica, sans-serif'.
            weight (str): CSS font weight. For example, 'bold'.
            style (str): CSS font style. For example, 'italic'

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setScaleLabelFont', {
            'family': family,
            'size': size,
            'weight': weight,
            'style': style
        })
        return self

    def set_scale_label_padding(self, padding: int | float):
        """Set padding of scale labels.

        Args:
            padding (int | float): Padding in pixels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setScaleLabelPadding', {'padding': padding})
        return self

    def set_scale_label_color(self, color: lightningchart.Color):
        """Set the color of the scale labels.

        Args:
            color (Color): Color of the scale labels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setScaleLabelStyle', {'color': color.get_hex()})
        return self


class SpiderChartDashboard(SpiderChart):

    def __init__(
            self,
            instance: Instance,
            dashboard_id: str,
            column: int,
            row: int,
            colspan: int,
            rowspan: int):
        Chart.__init__(self, instance)
        self.instance.send(self.id, 'createSpiderChart', {
            'db': dashboard_id,
            'column': column,
            'row': row,
            'colspan': colspan,
            'rowspan': rowspan
        })


class SpiderSeries:

    def __init__(self, chart: charts.Chart):
        self.chart = chart
        self.instance = chart.instance
        self.id = str(uuid.uuid4()).split('-')[0]
        self.instance.send(self.id, 'addSpiderSeries', {'chart': self.chart.id})

    def set_name(self, name: str):
        """Sets the name of the Component updating attached LegendBox entries.

        Args:
            name (str): Name of the component.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setName', {'name': name})
        return self

    def add_points(self, points: list[dict[str, int | float]]):
        """Adds an arbitrary amount of SpiderPoints to the Series.

        Args:
            points (str): List of SpiderPoints as {'axis': string, 'value': number}

        Returns:
            The instance of the class for fluent interface.
        """
        points = convert_to_dict(points)

        self.instance.send(self.id, 'addPoints', {'points': points})
        return self

    def dispose(self):
        """Permanently destroy the component.

        Returns:
            True
        """
        self.instance.send(self.id, 'dispose')
        return True

    def set_fill_color(self, color: lightningchart.Color):
        """Set color of the polygon that represents the shape of the Series.

        Args:
            color (Color): Color of the polygon.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setSolidFillStyle', {'color': color.get_hex()})
        return self

    def set_point_color(self, color: lightningchart.Color):
        """Set color of the series points.

        Args:
            color (Color): Color of the points.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setPointFillStyle', {'color': color.get_hex()})
        return self

    def set_line_color(self, color: lightningchart.Color):
        """Set the series polygon line color.

        Args:
            color (Color): Color of the lines.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setLineFillStyle', {'color': color.get_hex()})
        return self

    def set_line_thickness(self, thickness: int):
        """Set the series polygon line thickness.

        Args:
            thickness (int): Thickness of the lines.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setLineThickness', {'width': thickness})
        return self

    def set_point_size(self, size: int | float):
        """Set size of point in pixels

        Args:
            size (int | float): Size of point in pixels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setPoint2DSize', {'size': size})
        return self
