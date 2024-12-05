from __future__ import annotations

import lightningchart
from lightningchart import conf, Themes
from lightningchart.charts import GeneralMethods, TitleMethods, ChartWithLUT, Chart, ChartWithLabelStyling
from lightningchart.instance import Instance
from lightningchart.utils import convert_to_dict


class PyramidChart(GeneralMethods, TitleMethods, ChartWithLUT, ChartWithLabelStyling):
    """Visualizes proportions and percentages between categories, by dividing a pyramid into proportional segments."""

    def __init__(
            self,
            data: list[dict[str, int | float]] = None,
            slice_mode: str = 'height',
            theme: Themes = Themes.White,
            title: str = None,
            license: str = None,
            license_information: str = None,
    ):
        """Visualizes proportions and percentages between categories, by dividing a pyramid into proportional segments.

        Args:
            data (list[dict[str, int | float]]): List of {name, value} slices.
            slice_mode (str): "width" | "height"
            theme (Themes): Theme of the chart.
            title (str): Title of the chart.
            license (str): License key.
        """
        instance = Instance()
        Chart.__init__(self, instance)
        self.instance.send(self.id, 'pyramidChart', {
            'theme': theme.value,
            'license': license or conf.LICENSE_KEY,
            'licenseInformation': license_information or conf.LICENSE_INFORMATION,
        })
        self.set_slice_mode(slice_mode)
        if title:
            self.set_title(title)
        if data:
            self.add_slices(data)

    def add_slice(self, name: str, value: int | float):
        """This method is used for the adding slices in the pyramid chart.

        Args:
            name (str): Pyramid slice title.
            value (int | float): Pyramid slice value.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'addSlice', {'name': name, 'value': value})
        return self

    def add_slices(self, slices: list[dict[str, int | float]]):
        """This method is used for the adding multiple slices in the pyramid chart.

        Args:
            slices (list[dict[str, int | float]]): Array of {name, value} slices.

        Returns:
            The instance of the class for fluent interface.
        """
        slices = convert_to_dict(slices)

        self.instance.send(self.id, 'addSlices', {'slices': slices})
        return self

    def set_neck_width(self, width: int | float):
        """Set Pyramid Neck Width.

        Args:
            width (int | float): Pyramid Neck Width range from 0 to 100.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setNeckWidth', {'width': width})
        return self

    def set_slice_mode(self, mode: str = 'height'):
        """Set PyramidSliceMode. Can be used to select between different drawing approaches for Slices.

        Args:
            mode (str): "height" | "width"

        Returns:
            The instance of the class for fluent interface.
        """
        slice_modes = ("height", "width")
        if mode not in slice_modes:
            raise ValueError(
                f"Expected mode to be one of {slice_modes}"
                f", but got '{mode}'."
            )

        mode_number = 1
        if mode == 'height':
            mode_number = 0
        self.instance.send(self.id, 'setSliceMode', {'mode': mode_number})
        return self

    def set_slice_gap(self, gap: int | float):
        """Set gap between Slice / start of label connector, and end of label connector / Label.

        Args:
            gap (int | float): Gap as pixels. Clamped between [0, 20] !

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setSliceGap', {'gap': gap})
        return self

    def set_slice_stroke(
            self,
            thickness: int | float,
            color: lightningchart.Color
    ):
        """Set stroke style of Pyramid Slices border.

        Args:
            thickness (int | float): Thickness of the slice border.
            color (Color): Color of the slice border.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setSliceStrokeStyle', {'thickness': thickness, 'color': color.get_hex()})
        return self

    def set_label_side(self, side: str = 'left'):
        """Set the side where label should display.

        Args:
            side: "left" | "right"

        Returns:
            The instance of the class for fluent interface.
        """
        label_sides = ("left", "right")
        if side not in label_sides:
            raise ValueError(
                f"Expected side to be one of {label_sides}"
                f", but got '{side}'."
            )
        
        self.instance.send(self.id, 'setLabelSide', {'side': side})
        return self


class PyramidChartDashboard(PyramidChart):
    def __init__(
            self,
            instance: Instance,
            dashboard_id: str,
            column: int,
            row: int,
            colspan: int,
            rowspan: int):
        Chart.__init__(self, instance)
        self.instance.send(self.id, 'createPyramidChart', {
            'db': dashboard_id,
            'column': column,
            'row': row,
            'colspan': colspan,
            'rowspan': rowspan
        })
