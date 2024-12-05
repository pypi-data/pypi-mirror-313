from __future__ import annotations

import uuid

import lightningchart
from lightningchart.series import ComponentWithLinePaletteColoring
from lightningchart.ui import UIEWithTitle, UIElement
from lightningchart.ui.band import Band
from lightningchart.ui.constant_line import ConstantLine
from lightningchart.ui.custom_tick import CustomTick
from lightningchart.ui.custom_tick import CustomTick3D


class GenericAxis(UIEWithTitle):

    def __init__(self, chart):
        UIElement.__init__(self, chart)

    def set_title(self, title: str):
        """Specifies an Axis title string

        Args:
            title: Axis title as a string

        Returns:
            Axis itself for fluent interface
        """
        self.instance.send(self.id, 'setTitle', {'title': title})
        return self

    def set_title_color(self, color: lightningchart.Color):
        """Set the color of the Chart title.

        Args:
            color (Color): Color of the title.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTitleColor', {'color': color.get_hex()})
        return self

    def set_title_effect(self, enabled: bool):
        """Set theme effect enabled on component or disabled.

        Args:
            enabled: Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTitleEffect', {'enabled': enabled})
        return self

    def set_visible(self, visible: bool = True):
        """Set element visibility.

        Args:
            visible (bool): True when element should be visible and false when element should be hidden.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setVisible', {
            'visible': visible
        })
        return self

    def set_scroll_strategy(self, strategy: str = 'progressive'):
        """Specify ScrollStrategy of the Axis.
        This decides where the Axis scrolls based on current view and series boundaries.

        Args:
            strategy (str):  "expansion" | "fitting" | "progressive" | "regressive"

        Returns:
            The instance of the class for fluent interface.
        """
        strategies = ("expansion", "fitting", "progressive", "regressive")
        if strategy not in strategies:
            raise ValueError(
                f"Expected strategy to be one of {strategies}"
                f", but got '{strategy}'."
            )

        self.instance.send(self.chart.id, 'setScrollStrategy', {
            'strategy': strategy,
            'axis': self.id
        })
        return self

    def set_interval(
            self,
            start: int | float,
            end: int | float,
            stop_axis_after: bool = False,
            animate: bool = False
    ):
        """Set axis interval.

        Args:
            start (int): Start of the axis.
            end (int): End of the axis.
            stop_axis_after (bool): If false, the axis won't stop from scrolling.
            animate (bool): Boolean for animation enabled, or number for animation duration in milliseconds.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.chart.id, 'setAxisInterval', {
            'start': start,
            'end': end,
            'axis': self.id,
            'stop': stop_axis_after,
            'animate': animate
        })
        return self

    def fit(self, animate: int | bool = 0, stop_axis_after: bool = False):
        """Fit axis view to attached series.

        Args:
            animate (int | bool): Boolean for animation enabled, or number for animation duration in milliseconds.
            stop_axis_after (bool): If true, stops Axis after fitting.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'fit', {'animate': animate, 'stopAxisAfter': stop_axis_after})
        return self

    def set_animations_enabled(self, enabled: bool = True):
        """Disable/Enable all animations of the Chart.

        Args:
            enabled (bool): Boolean value to enable or disable animations.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setAnimationsEnabled', {'enabled': enabled})
        return self

    def set_stroke(self, thickness: int | float, color: lightningchart.Color):
        """Set the Axis line stroke.

        Args:
            thickness (int | float): Thickness of the stroke.
            color (Color): Color of the stroke.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setStrokeStyle', {'thickness': thickness, 'color': color})
        return self

    def set_default_interval(self, start: int | float, end: int | float):
        """Set Axis default interval. This does the same as setInterval method, but is also applied again whenever
        fit is triggered, or the "zoom to fit" user interaction is triggered.

        Args:
            start (int | float): Interval start point.
            end (int | float): Interval end point.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setDefaultInterval', {'start': start, 'end': end})
        return self

    def set_interval_restrictions(
            self,
            interval_min: int | float = None,
            interval_max: int | float = None,
            start_min: int | float = None,
            start_max: int | float = None,
            end_min: int | float = None,
            end_max: int | float = None,
    ):
        """Set restrictions on Axis interval (start/end). These are not applied immediately,
        but affect all axis scrolling and user interactions afterwards.

        Args:
            interval_min (int | float): Minimum interval length.
            interval_max (int | float): Maximum interval length.
            start_min (int | float): Minimum interval start value.
            start_max (int | float): Maximum interval start value.
            end_min (int | float): Minimum interval end value.
            end_max (int | float): Maximum interval end value.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setIntervalRestrictions', {
            'endMax': end_max,
            'endMin': end_min,
            'intervalMax': interval_max,
            'intervalMin': interval_min,
            'startMax': start_max,
            'startMin': start_min,
        })


class Axis(GenericAxis, ComponentWithLinePaletteColoring):

    def __init__(
            self,
            chart,
            axis: str,
            stack_index: int,
            parallel_index: int,
            opposite: bool,
            type: str,
            base: int
    ):
        GenericAxis.__init__(self, chart)
        self.instance.send(self.id, 'addAxis', {
            'chart': self.chart.id,
            'axis': axis,
            'opposite': opposite,
            'iStack': stack_index,
            'iParallel': parallel_index,
            'type': type,
            'base': base
        })

    def set_decimal_precision(self, decimals: int):
        """Format the axis ticks to certain number of decimal numbers.

        Args:
            decimals (int): Decimal precision.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTickStrategyFormattingRound', {'decimals': decimals})
        return self
    def set_tick_formatting(self, text: str):
        """

        Args:
            text (str):

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTickStrategyFormattingText', {'text': text})
        return self

    def set_length(self, length: int | float, relative: bool):
        """Configure length of axis. E.g. height for Y axis, width for X axis.

        Args:
            length (int | float): Length value
            relative (bool): If true, length value is interpreted as relative length across multiple axes. If false,
                length value is interpreted as length in pixels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setLength', {'length': length, 'relative': relative})
        return self

    def set_margins(self, start: int | float, end: int | float):
        """Add empty space at either end of the axis, without affecting the relative size of the Axis.

        Args:
            start (int | float): Start margin in pixels.
            end (int | float): End margin in pixels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setMargins', {'start': start, 'end': end})
        return self

    def add_band(self, on_top: bool = True):
        """Add a highlighter Band to the Axis. A Band can be used to highlight an interval on the Axis.

        Args:
            on_top (bool): Is Band rendered above Series, or below. Default to above.

        Returns:
            Reference to Band class.
        """
        return Band(self.chart, self, on_top)

    def add_constant_line(self, on_top: bool = True):
        """Add a highlighter ConstantLine to the Axis.
        A ConstantLine can be used to highlight a specific value on the Axis.

        Args:
            on_top (bool): Is ConstantLine rendered above Series, or below. Default to above.

        Returns:
            Reference to ConstantLine class.
        """
        return ConstantLine(self.chart, self, on_top)

    def add_custom_tick(self, tick_type: str = 'major'):
        """Add custom tick to Axis. Custom ticks can be used to expand on default tick placement,
        or completely override Axis ticks placement with custom logic.

        Args:
            tick_type (str): "major" | "minor" | "box"

        Returns:
            Reference to CustomTick class.
        """
        types = ("major", "minor", "box")
        if tick_type not in types:
            raise ValueError(
                f"Expected tick_type to be one of {types}"
                f", but got '{tick_type}'."
            )

        return CustomTick(self.chart, self, tick_type)

    def set_tick_strategy(self, strategy: str, time_origin: int | float = None, utc: bool = False):
        """Set TickStrategy of Axis. The TickStrategy defines the positioning and formatting logic of Axis ticks
        as well as the style of created ticks.

        Args:
            strategy (str): "Empty" | "Numeric" | "DateTime" | "Time"
            time_origin (int | float): Use with "DateTime" or "Time" strategy.
                If a time origin is defined, data points will be interpreted as milliseconds since time_origin.
            utc (bool): Use with DateTime strategy. By default, false, which means that tick placement is applied
                according to clients local time-zone/region and possible daylight saving cycle.
                When true, tick placement is applied in UTC which means no daylight saving adjustments &
                timestamps are displayed as milliseconds without any time-zone region offsets.

        Returns:
            The instance of the class for fluent interface.
        """
        strategies = ("Empty", "Numeric", "DateTime", "Time")
        if strategy not in strategies:
            raise ValueError(
                f"Expected strategy to be one of {strategies}"
                f", but got '{strategy}'."
            )

        self.instance.send(self.chart.id, 'setTickStrategy', {
            'strategy': strategy,
            'axis': self.id,
            'timeOrigin': time_origin,
            'utc': utc,
        })
        return self

    def pan(self, amount: int | float):
        """Pan scale by pixel value delta.

        Args:
            amount (int | float): Amount to shift scale of axis in pixels

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'panAxis', {'amount': amount})
        return self

    def zoom(self, reference_position: int | float, zoom_direction: int | float):
        """Zoom scale from/to a position.

        Args:
            reference_position (int | float): Position to zoom towards or from on axis.
            zoom_direction (int | float): Amount and direction of zoom [-1, 1] as a guideline.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'zoomAxis', {
            'referencePosition': reference_position,
            'zoomDirection': zoom_direction
        })
        return self

    def set_major_tick_font(
            self,
            size: int | float,
            family: str = "Segoe UI, -apple-system, Verdana, Helvetica",
            style: str = 'normal',
            weight: str = 'normal'
    ):
        """Set the font of major axis tick labels.

        Args:
            size (int | float): CSS font size. For example, 16.
            family (str): CSS font family. For example, 'Arial, Helvetica, sans-serif'.
            weight (str): CSS font weight. For example, 'bold'.
            style (str): CSS font style. For example, 'italic'

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setMajorTickFont', {
            'family': family,
            'size': size,
            'weight': weight,
            'style': style
        })
        return self

    def set_minor_tick_font(
            self,
            size: int | float,
            family: str = "Segoe UI, -apple-system, Verdana, Helvetica",
            style: str = 'normal',
            weight: str = 'normal'
    ):
        """Set the font of minor axis tick labels.

        Args:
            size (int | float): CSS font size. For example, 16.
            family (str): CSS font family. For example, 'Arial, Helvetica, sans-serif'.
            weight (str): CSS font weight. For example, 'bold'.
            style (str): CSS font style. For example, 'italic'

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setMinorTickFont', {
            'family': family,
            'size': size,
            'weight': weight,
            'style': style
        })
        return self

    def set_major_tick_color(self, color: lightningchart.Color):
        """Set the color of major axis tick labels.

        Args:
            color (Color): Color of the labels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setMajorTickFillStyle', {'color': color.get_hex()})
        return self

    def set_minor_tick_color(self, color: lightningchart.Color):
        """Set the color of minor axis tick labels.

        Args:
            color (Color): Color of the labels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setMinorTickFillStyle', {'color': color.get_hex()})
        return self

    def set_chart_interaction_fit_by_drag(self, enabled: bool):
        """Set is mouse-interaction enabled: Fitting by capturing rectangle on chart.

        Args:
            enabled (bool): Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setChartInteractionFitByDrag', {'enabled': enabled})
        return self

    def set_chart_interaction_pan_by_drag(self, enabled: bool):
        """Set is mouse-interaction enabled: Panning by dragging on chart.

        Args:
            enabled (bool): Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setChartInteractionPanByDrag', {'enabled': enabled})
        return self

    def set_chart_interaction_zoom_by_drag(self, enabled: bool):
        """Set is mouse-interaction enabled: Zooming by capturing rectangle on chart.

        Args:
            enabled (bool): Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setChartInteractionZoomByDrag', {'enabled': enabled})
        return self

    def set_chart_interaction_zoom_by_wheel(self, enabled: bool):
        """Set is mouse-interaction enabled: Zooming by mouse-wheeling on chart.

        Args:
            enabled (bool): Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setChartInteractionZoomByWheel', {'enabled': enabled})
        return self

    def set_axis_interaction_pan_by_dragging(self, enabled: bool):
        """Set is mouse-interaction enabled: Panning by dragging on axis. (RMB)

        Args:
            enabled (bool): Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setAxisInteractionPanByDragging', {'enabled': enabled})
        return self

    def set_axis_interaction_release_by_double_clicking(self, enabled: bool):
        """Set is mouse-interaction enabled: Release axis by double-clicking on axis.

        Args:
            enabled (bool): Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setAxisInteractionReleaseByDoubleClicking', {'enabled': enabled})
        return self

    def set_axis_interaction_zoom_by_dragging(self, enabled: bool):
        """Set is mouse-interaction enabled: Zooming by dragging on axis. (LMB)

        Args:
            enabled (bool): Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setAxisInteractionZoomByDragging', {'enabled': enabled})
        return self

    def set_axis_interaction_zoom_by_wheeling(self, enabled: bool):
        """Set is mouse-interaction enabled: Zooming by mouse-wheeling on axis.

        Args:
            enabled (bool): Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setAxisInteractionZoomByWheeling', {'enabled': enabled})
        return self

    def set_thickness(self, thickness: int | float):
        """Set Axis thickness as pixels.

        Args:
            thickness (int | float): Explicit thickness of Axis as pixels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setThickness', {'thickness': thickness})
        return self

    def set_title_margin(self, margin: int | float):
        """Specifies padding after chart title.

        Args:
            margin (int | float): Gap after the chart title in pixels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTitleMargin', {'margin': margin})
        return self

    def set_chart_interactions(self, enabled: bool):
        """Set all states of chart mouse interactions on axis at once.

        Args:
            enabled (bool): Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setChartInteractions', {'enabled': enabled})
        return self

    def set_nib_interaction_scale_by_dragging(self, enabled: bool):
        """Set is mouse-interaction enabled: Scaling by dragging on nib.

        Args:
            enabled (bool): Boolean.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setNibInteractionScaleByDragging', {'enabled': enabled})
        return self

    def set_nib_interaction_scale_by_wheeling(self, enabled: bool):
        """Set is mouse-interaction enabled: Scaling by mouse-wheeling on nib.

        Args:
            enabled (bool): Boolean.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setNibInteractionScaleByWheeling', {'enabled': enabled})
        return self

    def set_nib_length(self, length: int | float):
        """Specifies Axis nib stroke length in pixels.

        Args:
            length (int | float): Axis nib stroke length in pixels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setNibLength', {'length': length})
        return self

    def set_nib_mouse_picking_area_size(self, size: int | float):
        """Set ideal size of nib mouse-picking area in pixels.

        Args:
            size (int | float): Size in pixels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setNibMousePickingAreaSize', {'size': size})
        return self


class DefaultAxis(Axis):

    def __init__(self, chart, axis: str):
        self.chart = chart
        self.dimension = axis
        self.id = str(uuid.uuid4()).split('-')[0]
        self.instance = chart.instance
        self.instance.send(self.chart.id, 'getDefaultAxisReference', {
            'dimension': self.dimension,
            'axisID': self.id
        })


class DefaultAxis3D(GenericAxis):

    def __init__(self, chart, axis: str):
        self.chart = chart
        self.dimension = axis
        self.id = str(uuid.uuid4()).split('-')[0]
        self.instance = chart.instance
        self.instance.send(self.chart.id, 'getDefaultAxisReference', {
            'dimension': self.dimension,
            'axisID': self.id
        })

    def set_tick_strategy(self, strategy: str, time_origin: int | float = None, utc: bool = False):
        """Set TickStrategy of Axis. The TickStrategy defines the positioning and formatting logic of Axis ticks
        as well as the style of created ticks.

        Args:
            strategy (str): "Empty" | "Numeric" | "DateTime" | "Time"
            time_origin (int | float): Define with time.time(). If a time origin is defined,
                data-points will instead be interpreted as milliseconds since time origin.
            utc (bool): Use with DateTime strategy. By default, false, which means that tick placement is applied
                according to clients local time-zone/region and possible daylight saving cycle.
                When true, tick placement is applied in UTC which means no daylight saving adjustments &
                timestamps are displayed as milliseconds without any time-zone region offsets.

        Returns:
            The instance of the class for fluent interface.
        """
        strategies = ("Empty", "Numeric", "DateTime", "Time")
        if strategy not in strategies:
            raise ValueError(
                f"Expected strategy to be one of {strategies}"
                f", but got '{strategy}'."
            )

        self.instance.send(self.chart.id, 'setTickStrategy', {
            'strategy': strategy,
            'axis': self.id,
            'timeOrigin': time_origin,
            'utc': utc,
        })
        return self
    
    def add_custom_tick(self, tick_type: str = 'major'):
        """Add a 3D custom tick to the Axis.
        Custom ticks can be used to completely control tick placement, text, and styles in a 3D environment.

        Args:
            tick_type (str): "major" | "minor" | "box"

        Returns:
            Reference to CustomTick3D class.
        """
        types = ("major", "minor", "box")
        if tick_type not in types:
            raise ValueError(f"Expected tick_type to be one of {types}, but got '{tick_type}'.")

        return CustomTick3D(self.chart, self, tick_type)


class BarChartAxis(GenericAxis):

    def __init__(self, chart):
        GenericAxis.__init__(self, chart)

    def set_thickness(self, thickness: int | float):
        """Set Axis thickness as pixels.

        Args:
            thickness (int | float): Explicit thickness of Axis as pixels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setThickness', {'thickness': thickness})
        return self


class CategoryAxis(BarChartAxis):

    def __init__(self, chart):
        BarChartAxis.__init__(self, chart)
        self.instance.send(self.id, 'getCategoryAxisReference', {'chart': self.chart.id})


class ValueAxis(BarChartAxis):
    def __init__(self, chart):
        BarChartAxis.__init__(self, chart)
        self.instance.send(self.id, 'getValueAxisReference', {'chart': self.chart.id})

    def set_tick_strategy(self, strategy: str):
        """Set TickStrategy of Axis. The TickStrategy defines the positioning and formatting logic of Axis ticks
        as well as the style of created ticks.

        Args:
            strategy (str): "Empty" | "Numeric"

        Returns:
            The instance of the class for fluent interface.
        """
        strategies = ("Empty", "Numeric")
        if strategy not in strategies:
            raise ValueError(
                f"Expected strategy to be one of {strategies}"
                f", but got '{strategy}'."
            )

        self.instance.send(self.chart.id, 'setTickStrategy', {
            'strategy': strategy,
            'axis': self.id,
        })
        return self
