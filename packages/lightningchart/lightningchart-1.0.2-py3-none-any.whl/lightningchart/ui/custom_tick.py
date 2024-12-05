from __future__ import annotations

import lightningchart
from lightningchart.ui import UIElement

class CustomTick(UIElement):

    def __init__(self, chart, axis, tick_type: str = 'major'):
        UIElement.__init__(self, chart)
        self.instance.send(self.id, 'addCustomTick', {'axis': axis.id, 'tickType': tick_type})

    def set_value(self, value: int | float):
        """Sets the position of this custom tick on its Axis.

        Args:
            value (int | float): Value in the units of main scale.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setValue', {'value': value})
        return self

    def set_text(self, text: str):
        """Override the tick label text

        Args:
            text (str): Text to display on the tick.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTextFormatterText', {'text': str(text)})
        return self

    def set_decimal_precision(self, decimals: int):
        """Format the tick label value to certain number of decimal numbers.

        Args:
            decimals (int): Decimal precision.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTextFormatterRound', {'decimals': decimals})
        return self

    def set_allocates_axis_space(self, enabled: bool):
        """Set whether CustomTick should allocate space on its Axis.
        By default, this is true, which means that Axis will always make sure it is big enough to fit the tick.
        By setting to false, this particular CustomTick can be removed from this behaviour,
        which can be useful in applications where some custom ticks are only enabled temporarily.
        Disabling this functionality can prevent the size of the Axis from changing in unwanted ways.

        Args:
            enabled (bool): Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setAllocatesAxisSpace', {'enabled': enabled})
        return self

    def set_grid_stroke_length(self, length: int | float):
        """Set length of grid stroke in percents.

        Args:
            length (int | float): Grid line length as a % of viewport size.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setGridStrokeLength', {'length': length})
        return self

    def set_grid_stroke_style(self, thickness: int | float, color: lightningchart.Color):
        """Set style of grid stroke.

        Args:
            thickness (int | float): Thickness of the grid stroke.
            color (Color): Color of the grid stroke.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setGridStrokeStyle', {'thickness': thickness, 'color': color.get_hex()})
        return self

    def set_marker_color(self, color: lightningchart.Color):
        """Set the color of the tick label.

        Args:
            color (Color): Color of the tick label.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setMarkerColor', {'color': color.get_hex()})
        return self

    def set_marker_font(
            self,
            size: int | float,
            family: str = "Segoe UI, -apple-system, Verdana, Helvetica",
            style: str = 'normal',
            weight: str = 'normal'
    ):
        """Set font of tick label.

        Args:
            size (int | float): CSS font size. For example, 16.
            family (str): CSS font family. For example, 'Arial, Helvetica, sans-serif'.
            weight (str): CSS font weight. For example, 'bold'.
            style (str): CSS font style. For example, 'italic'

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setMarkerFont', {
            'family': family,
            'size': size,
            'weight': weight,
            'style': style
        })
        return self

    def set_marker_visible(self, visible: bool):
        """Set marker visible or not.

        Args:
            visible (bool): Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setMarkerVisible', {'visible': visible})
        return self

    def set_tick_label_padding(self, padding: int | float):
        """Set pixel padding between tick line and label.

        Args:
            padding (int | float): Amount of padding in pixels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTickLabelPadding', {'padding': padding})
        return self

    def set_tick_label_rotation(self, value: int | float):
        """Set rotation of tick label.

        Args:
            value (int | float): Rotation in degrees.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTickLabelRotation', {'value': value})
        return self

    def set_tick_length(self, length: int | float):
        """Set tick length as pixels.

        Args:
            length (int | float): Tick length as pixels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTickLength', {'length': length})
        return self
    

class CustomTick3D(UIElement):

    def __init__(self, chart, axis, tick_type: str = 'major'):
        UIElement.__init__(self, chart)
        self.instance.send(self.id, 'addCustomTick', {'axis': axis.id, 'tickType': tick_type})

    def set_value(self, value: int | float):
        """Set location of custom tick on its Axis.

        Args:
            value: Location on axis.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setValue', {'value': value})
        return self

    def set_text(self, text: str):
        """Override the tick label text

        Args:
            text (str): Text to display on the tick.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTextFormatterText', {'text': str(text)})
        return self

    def set_background_color(self, color: lightningchart.Color):
        """Set the background color of the tick.

        Args:
            color: Color value.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setBackgroundFillStyle', {'color': color.get_hex()})
        return self

    def set_background_stroke(self, thickness: int | float, color: lightningchart.Color):
        """Set stroke style of background around ticks label.

        Args:
            thickness: Thickness of the stroke.
            color: Color of the stroke.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setBackgroundStrokeStyle', {'thickness': thickness, 'color': color.get_hex()})
        return self

    def set_grid_stroke(self, thickness: int | float, color: lightningchart.Color):
        """Set style of custom ticks grid line. This line highlights the tick location under the series area.

        Args:
            thickness: Thickness of the stroke.
            color: Color of the stroke.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setGridStrokeStyle', {'thickness': thickness, 'color': color.get_hex()})
        return self
    
    def set_text_color(self, color: lightningchart.Color):
        """Set fill style of custom ticks text.

        Args:
            color: Color value.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTextFillStyle', {'color': color.get_hex()})
        return self
    
    def set_text_font(
            self,
            size: int | float,
            family: str = "Segoe UI, -apple-system, Verdana, Helvetica",
            style: str = 'normal',
            weight: str = 'normal'
    ):
        """Set font of custom ticks text.

        Args:
            size (int | float): CSS font size. For example, 16.
            family (str): CSS font family. For example, 'Arial, Helvetica, sans-serif'.
            weight (str): CSS font weight. For example, 'bold'.
            style (str): CSS font style. For example, 'italic'

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTextFont', {'family': family, 'size': size, 'weight': weight, 'style': style})
        return self

    def set_tick_length(self, length: int | float):
        """Set tick line length as pixels.

        Args:
            length: Tick line length as pixels

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTickLength', {'length': length})
        return self

    def set_tick_style(self, thickness: int | float, color: lightningchart.Color):
        """Set style of custom ticks tick line.
        This line connects the text to its Axis, generally a very short line (6 pixels, or so).

        Args:
            thickness: Thickness of the stroke.
            color: Color of the stroke.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTickStrokeStyle', {'thickness': thickness, 'color': color.get_hex()})
        return self

    def set_padding(self, padding: int | dict):
        """Set padding between tick label text and its background (if any).

        Args:
            padding: number for symmetric padding, or object with any of left, right, top, bottom paddings.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setPadding', {'padding': padding})
        return self
