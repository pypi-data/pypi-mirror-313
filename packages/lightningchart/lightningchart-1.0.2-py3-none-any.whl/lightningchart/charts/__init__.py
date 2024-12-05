from __future__ import annotations
import datetime
import uuid
from IPython import get_ipython

import lightningchart
from lightningchart import conf
from lightningchart.instance import Instance, start_server
from lightningchart.series import Series
from lightningchart.ui.axis import DefaultAxis, DefaultAxis3D, Axis
from lightningchart.ui.legend import Legend
from lightningchart.ui.text_box import TextBox

class Chart:

    def __init__(self, instance: Instance):
        self.id = str(uuid.uuid4()).split('-')[0]
        self.instance = instance

    def open(self, method: str = None, live=False, width: int | str = '100%', height: int | str = 600):
        """Open the rendering view.
        Method "browser" will open the rendering view in your browser.
        Method "notebook" will open the rendering view an iframe component for notebook environment.

        Args:
            method (str): "browser" | "notebook"
            live (bool): Whether to use real-time rendering or not.
            width (int): The width of the IFrame component in pixels.
            height (int): The height of the IFrame component in pixels.

        Returns:
            Either opens a new tab on your browser or returns an IFrame component for Jupyter Notebook.
        """
        if method not in ('browser', "notebook"):
            if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
                method = 'notebook'
            else:
                method = 'browser'

        if live and not conf.server_is_on:
            start_server()
            conf.server_is_on = True

        if live and not self.instance.live:
            self.instance.live = True
            for i in self.instance.items:
                self.instance.send(i['id'], i['command'], i['args'])

        if method == 'notebook':
            return self.instance.open_in_notebook(width=width, height=height)
        else:
            self.instance.open_in_browser()
            return self

    def open_in_notebook(self, width: int | str = '100%', height: int | str = 600):
        """Render the chart in notebook environment using iframe component.

        Args:
            width (int): The width of the IFrame component in pixels.
            height (int): The height of the IFrame component in pixels.

        Returns:
            IFrame
        """
        if not conf.server_is_on:
            start_server()
            conf.server_is_on = True
        if not self.instance.live:
            self.instance.live = True
            for i in self.instance.items:
                self.instance.send(i['id'], i['command'], i['args'])
        return self.instance.open_in_notebook(width=width, height=height)

    def close(self):
        """Close the connection to a chart with real-time display mode.

        Note: This will terminate the current Python instance!
        """
        if self.instance.live:
            self.instance.send(self.id, 'shutdown')

    def open_live_server(self):
        """Initialize a real-time chart, but don't open the render view.

        Returns:
            URL where the real-time chart is hosted.
        """
        if not conf.server_is_on:
            start_server()
            conf.server_is_on = True
        if not self.instance.live:
            self.instance.live = True
            for i in self.instance.items:
                self.instance.send(i['id'], i['command'], i['args'])
        return f'http://{conf.LOCALHOST}:{conf.server_port}?id={self.instance.id}'

    def set_data_preservation(self, enabled: bool):
        """Enable or disable server-side data preservation for real-time visualization use cases.

        Enabled by default!

        Args:
            enabled (bool): Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        if not conf.server_is_on:
            raise Exception("set_data_preservation must be called after live chart has been opened!")
        self.instance.set_preservation(enabled)
        return self


class GeneralMethods(Chart):

    def save_to_file(
            self,
            file_name: str = None,
            image_format: str = 'image/png',
            image_quality: float = 0.92
    ):
        """Save the current rendering view as a screenshot.

        Args:
            file_name (str): Name of prompted download file as string. File extension shouldn't be included as it is
                automatically detected from 'type'-argument.
            image_format (str): A DOMString indicating the image format. The default format type is image/png.
            image_quality (float): A Number between 0 and 1 indicating the image quality to use for image formats that
                use lossy compression such as image/jpeg and image/webp. If this argument is anything else,
                the default value for image quality is used. The default value is 0.92.

        Returns:
            The instance of the class for fluent interface.
        """
        if file_name is None:
            file_name = f'LightningChart_Python_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}'
        self.instance.send(self.id, 'saveToFile', {
            'fileName': file_name,
            'type': image_format,
            'encoderOptions': image_quality
        })
        return self

    def dispose(self):
        """Permanently destroy the component."""
        self.instance.send(self.id, 'dispose')

    def set_animations_enabled(self, enabled: bool = True):
        """Disable/Enable all animations of the Chart.

        Args:
            enabled (bool): Boolean value to enable or disable animations.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setAnimationsEnabled', {'enabled': enabled})
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

    def set_background_color(
            self,
            color: lightningchart.Color
    ):
        """Set the background color of the chart.

        Args:
            color (Color): Color of the background.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setBackgroundFillStyle', {'color': color.get_hex()})
        return self

    def set_background_stroke(
            self,
            thickness: int | float,
            color: lightningchart.Color
    ):
        """Set the background stroke style of the chart.

        Args:
            thickness (int | float): Thickness of the stroke.
            color (Color): The color of the stroke.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setBackgroundStrokeStyle', {
            'thickness': thickness,
            'color': color.get_hex()
        })
        return self

    def add_legend(
            self,
            horizontal: bool = False,
            title: str = None,
            data: Chart | Series = None,
            x: int = None,
            y: int = None,
            position_scale: str = 'percentage'
    ) -> Legend:
        """Add legend box to the chart.

        Args:
            horizontal (bool): Whether the legend box is horizontally aligned or not.
            title (str): Title of the legend.
            data (Chart/Series): Reference either to Chart of Series class which the legend will display.
            x (int): X position in percentages (0-100).
            y (int): Y position in percentages (0-100).
            position_scale (str): "percentage" | "pixel" | "axis"

        Returns:
            Reference to Legend Box class.
        """
        return Legend(chart=self, horizontal=horizontal, title=title, data=data, x=x, y=y, position_scale=position_scale)

    legend = add_legend

    def add_textbox(
            self,
            text: str = None,
            x: int = None,
            y: int = None,
            position_scale: str = 'axis'
    ):
        """Add text box to the chart.

        Args:
            text (str): Text of the text box.
            x (int): X position in percentages (0-100).
            y (int): Y position in percentages (0-100).
            position_scale (str): "percentage" | "pixel" | "axis"

        Returns:
            Reference to Text Box class.
        """
        return TextBox(chart=self, text=text, x=x, y=y, position_scale=position_scale)

    textbox = add_textbox


class TitleMethods(Chart):

    def set_title(self, title: str):
        """Set text of Chart title.

        Args:
            title (str): Chart title as a string.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTitle', {'title': title})
        return self

    def hide_title(self):
        """Hide title and remove padding around it.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'hideTitle')
        return self

    def set_title_color(self, color: lightningchart.Color):
        """Set color of Chart title.

        Args:
            color (Color): Color of the title.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTitleColor', {'color': color.get_hex()})
        return self

    def set_title_font(
            self,
            size: int | float,
            family: str = "Segoe UI, -apple-system, Verdana, Helvetica",
            style: str = 'normal',
            weight: str = 'normal'
    ):
        """Set font of Chart title.

        Args:
            size (int | float): CSS font size. For example, 16.
            family (str): CSS font family. For example, 'Arial, Helvetica, sans-serif'.
            weight (str): CSS font weight. For example, 'bold'.
            style (str): CSS font style. For example, 'italic'

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTitleFont', {
            'family': family,
            'size': size,
            'weight': weight,
            'style': style
        })
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

    def set_title_rotation(self, degrees: int | float):
        """Set rotation of Chart title.

        Args:
            degrees (int | float): Rotation in degrees.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTitleRotation', {'value': degrees})
        return self

    def set_title_effect(self, enabled: bool = True):
        """Set theme effect enabled on component or disabled.

        Args:
            enabled (bool): Theme effect enabled.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTitleEffect', {'enabled': enabled})
        return self


class ChartWithXYAxis(Chart):

    def __init__(self):
        self.default_x_axis = DefaultAxis(self, 'x')
        self.default_y_axis = DefaultAxis(self, 'y')

    def get_default_x_axis(self) -> Axis:
        """Get the reference to the default x-axis of the chart.

        Returns:
            Reference to Axis class.
        """
        return self.default_x_axis

    def get_default_y_axis(self) -> Axis:
        """Get the reference to the default y-axis of the chart.

        Returns:
            Reference to Axis class.
        """
        return self.default_y_axis

    def synchronize_axis_intervals(self, axis_array: list[Axis]):
        """Convenience function for synchronizing the intervals of n amount of ´Axis´.

        Args:
            axis_array (list[Axis]): List of Axis to synchronize.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'synchronizeAxes', {'axes': axis_array})
        return self


class ChartWithXYZAxis(Chart):

    def __init__(self):
        self.default_x_axis = DefaultAxis3D(self, 'x')
        self.default_y_axis = DefaultAxis3D(self, 'y')
        self.default_z_axis = DefaultAxis3D(self, 'z')

    def get_default_x_axis(self) -> DefaultAxis3D:
        """Get the reference to the default x-axis of the chart.

        Returns:
            Reference to Axis3D class.
        """
        return self.default_x_axis

    def get_default_y_axis(self) -> DefaultAxis3D:
        """Get the reference to the default y-axis of the chart.

        Returns:
            Reference to Axis3D class.
        """
        return self.default_y_axis

    def get_default_z_axis(self) -> DefaultAxis3D:
        """Get the reference to the default y-axis of the chart.

        Returns:
            Reference to Axis3D class.
        """
        return self.default_z_axis


class ChartWithSeries(Chart):

    def __init__(self, instance: Instance):
        Chart.__init__(self, instance)
        self.series_list = []

    def set_series_background_effect(self, enabled: bool = True):
        """Set theme effect enabled on component or disabled.

        Args:
            enabled (bool): Theme effect enabled.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setSeriesBackgroundEffect', {'enabled': enabled})
        return self

    def set_series_background_color(
            self,
            color: lightningchart.Color
    ):
        """Set the color of chart series background.

        Args:
            color (Color): Color of the series background.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setSeriesBackgroundFillStyle', {'color': color.get_hex()})
        return self

    def set_mouse_interactions(self, enabled: bool = True):
        """Set mouse interactions enabled or disabled.

        Args:
            enabled (bool): Specifies state of mouse interactions.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setMouseInteractions', {'enabled': enabled})
        return self


class ChartWithLUT(Chart):

    def set_lookup_table(
            self,
            steps: list[dict[str, any]],
            interpolate: bool = True,
            percentage_values: bool = False
    ):
        """ Attach lookup table (LUT) to fill the slices with Colors based on value.

        Args:
            steps (list[dict]): List of {"value": number, "color": Color} dictionaries.
            interpolate (bool): Whether color interpolation is used
            percentage_values (bool): Whether values represent percentages or explicit values.

        Returns:
            The instance of the class for fluent interface.
        """
        for i in steps:
            if 'color' in i and type(i.get('color')) != 'string':
                i['color'] = i['color'].get_hex()

        self.instance.send(self.id, 'setLUT', {
            'steps': steps,
            'interpolate': interpolate,
            'percentageValues': percentage_values,
        })
        return self


class ChartWithLabelStyling(Chart):

    def set_label_formatter(self, formatter: str = 'NamePlusValue'):
        """Set formatter of Slice Labels.

        Args:
            formatter: "Name" | "NamePlusValue" | "NamePlusRelativeValue"

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setLabelFormatter', {'formatter': formatter})
        return self

    def set_label_color(self, color: lightningchart.Color):
        """Set the color of Slice Labels.

        Args:
            color (Color): Color of the labels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setLabelColor', {'color': color.get_hex()})
        return self

    def set_label_font(
            self,
            size: int | float,
            family: str = "Segoe UI, -apple-system, Verdana, Helvetica",
            style: str = 'normal',
            weight: str = 'normal'
    ):
        """Set font of Slice Labels.

        Args:
            size (int | float): CSS font size. For example, 16.
            family (str): CSS font family. For example, 'Arial, Helvetica, sans-serif'.
            weight (str): CSS font weight. For example, 'bold'.
            style (str): CSS font style. For example, 'italic'

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setLabelFont', {
            'family': family,
            'size': size,
            'weight': weight,
            'style': style
        })
        return self

    def set_label_effect(self, enabled: bool):
        """Set theme effect enabled on label or disabled. A theme can specify an Effect to add extra visual
        oomph to chart applications, like Glow effects around data or other components.

        Args:
            enabled (bool): Theme effect enabled.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setLabelEffect', {'enabled': enabled})
        return self

    def set_slice_effect(self, enabled: bool):
        """Set theme effect enabled on slice or disabled. A theme can specify an Effect to add extra visual
        oomph to chart applications, like Glow effects around data or other components.

        Args:
            enabled (bool): Theme effect enabled.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setSliceEffect', {'enabled': enabled})
        return self

    def set_slice_colors(self, color_list: list[lightningchart.Color]):
        """Set the colors of all slices at once.

        Args:
            color_list (list[Color]): list of Colors. The length must match the current number of slices!

        Returns:
            The instance of the class for fluent interface.
        """
        hex_array = []
        for color in color_list:
            hex_array.append(color.get_hex())

        self.instance.send(self.id, 'setSliceFuncFillStyle', {'hexArray': hex_array})
        return self

    def set_slice_sorter(self, sorter: str):
        """Define the sorting logic for slices.

        Args:
            sorter (str): "name" | "valueAscending" | "valueDescending" | "none"

        Returns:
            The instance of the class for fluent interface.
        """
        slice_sorters = ("name", "valueAscending", "valueDescending", "none")
        if sorter not in slice_sorters:
            raise ValueError(
                f"Expected sorter to be one of {slice_sorters}"
                f", but got '{sorter}'."
            )

        self.instance.send(self.id, 'setSliceSorter', {'sorter': sorter})
        return self

    def set_label_connector_gap(self, gap: int | float):
        """Set gap between Slice / start of label connector, and end of label connector / Label.

        Args:
            gap (int | float): Gap as pixels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setLabelConnectorGap', {'gap': gap})
        return self

    def set_label_connector_style(self, style: str, thickness: int | float, color: lightningchart.Color):
        """Set style of Label connector lines.

        Args:
            style (str): "solid" | "dashed" | "empty"
            thickness (int | float): Thickness of the connector line.
            color (Color): Color of the connector line.

        Returns:
            The instance of the class for fluent interface.
        """
        styles = ("solid", "dashed", "empty")
        if style not in styles:
            raise ValueError(
                f"Expected sorter to be one of {styles}"
                f", but got '{style}'."
            )

        self.instance.send(self.id, 'setLabelConnectorStyle', {
            'style': style,
            'thickness': thickness,
            'color': color.get_hex()
        })
        return self
