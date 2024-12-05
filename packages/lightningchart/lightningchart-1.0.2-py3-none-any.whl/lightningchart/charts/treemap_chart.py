from __future__ import annotations

import lightningchart
from lightningchart import conf, Themes
from lightningchart.charts import GeneralMethods, TitleMethods, Chart
from lightningchart.instance import Instance
from lightningchart.utils import convert_to_dict


class TreeMapChart(GeneralMethods, TitleMethods):
    """TreeMap Chart for visualizing hierarchical data."""

    def __init__(
            self,
            data: list[dict] = None,
            theme: Themes = Themes.White,
            title: str = None,
            license: str = None,
            license_information: str = None,
    ):
        """A TreeMapChart with optional data and configurations.

        Args:
            data (list[dict]): Initial data for the TreeMap.
            theme (Themes): Theme of the chart.
            title (str): Title of the chart.
            license (str): License key.
            license_information (str): License information.
        """
        instance = Instance()
        Chart.__init__(self, instance)
        self.instance.send(self.id, 'treeMapChart', {
            'theme': theme.value,
            'license': license or conf.LICENSE_KEY,
            'licenseInformation': license_information or conf.LICENSE_INFORMATION,
        })
        if title:
            self.set_title(title)
        if data:
            self.set_data(data)

    def set_data(self, data: list[dict]):
        """Set data for the TreeMap chart.

        Args:
            data: Array of objects with category and value properties.

        Returns:
            The instance of the class for fluent interface.
        """
        data = convert_to_dict(data)

        self.instance.send(self.id, 'setData', {'data': data})
        return self

    def set_displayed_levels_count(self, level: int):
        """Set the amount of levels of children nodes to display.

        Args:
            level: Amount of levels to display.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setDisplayedLevelsCount', {'level': level})
        return self

    def set_header_font(
            self,
            size: int | float,
            family: str = "Segoe UI, -apple-system, Verdana, Helvetica",
            style: str = 'normal',
            weight: str = 'normal'
    ):
        """Set the header font for the TreeMap chart.

        Args:
            size (int | float): CSS font size. For example, 16.
            family (str): CSS font family. For example, 'Arial, Helvetica, sans-serif'.
            weight (str): CSS font weight. For example, 'bold'.
            style (str): CSS font style. For example, 'italic'

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setHeaderFont', {
            'family': family,
            'size': size,
            'weight': weight,
            'style': style
        })
        return self

    def set_init_path_button_text(self, text: str):
        """Set the text for the back button that returns to the 1st level of Nodes.

        Args:
            text: Text for the button.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setInitPathButtonText', {'text': text})
        return self

    def set_drill_down_enabled(self, enabled: bool):
        """Enable/disable drilldown. Drill Down is enabled by default.

        Args:
            enabled: Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setDrillDownEnabled', {'enabled': enabled})
        return self

    def set_animation_highlight(self, enabled: bool):
        """Set component highlight animations enabled or not.

        Args:
            enabled: Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        """Set component highlight animations enabled or not."""
        self.instance.send(self.id, 'setAnimationHighlight', {'enabled': enabled})
        return self

    def set_animation_values(self, enabled: bool, speed_multiplier: float = 1):
        """Enable/disable animation of Nodes positions.

        Args:
            enabled: Boolean flag.
            speed_multiplier: Optional multiplier for category animation speed. 1 matches default speed.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setAnimationValues', {'enabled': enabled, 'speedMultiplier': speed_multiplier})
        return self

    def set_node_coloring(
            self,
            steps: list[dict],
            look_up_property: str = 'value',
            interpolate: bool = True,
            percentage_values: bool = False
    ):
        """Set the color of the nodes.

        Args:
            steps (list[dict]): List of {"value": number, "color": Color} dictionaries.
            interpolate (bool): Enables automatic linear interpolation between color steps.
            look_up_property (str): "value" | "x" | "y" | "z"
            percentage_values (bool): Whether values represent percentages or explicit values.

        Returns:
            The instance of the class for fluent interface.
        """
        for i in steps:
            if 'color' in i and type(i.get('color')) != 'string':
                i['color'] = i['color'].get_hex()

        self.instance.send(self.id, 'setNodeColoring', {
            'steps': steps,
            'lookUpProperty': look_up_property,
            'interpolate': interpolate,
            'percentageValues': percentage_values,
        })
        return self

    def set_path_label_color(self, color: lightningchart.Color):
        """Set Color of the path labels.

        Args:
            color: Color value.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setPathLabelFillStyle', {'color': color.get_hex()})
        return self

    def set_path_label_font(
            self,
            size: int | float,
            family: str = "Segoe UI, -apple-system, Verdana, Helvetica",
            style: str = 'normal',
            weight: str = 'normal'
    ):
        """Set Font of the path labels.

        Args:
            size (int | float): CSS font size. For example, 16.
            family (str): CSS font family. For example, 'Arial, Helvetica, sans-serif'.
            weight (str): CSS font weight. For example, 'bold'.
            style (str): CSS font style. For example, 'italic'

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setPathLabelFont', {
            'family': family,
            'size': size,
            'weight': weight,
            'style': style
        })
        return self

    def set_header_color(self, color: lightningchart.Color):
        """Set the color of the node labels.

        Args:
            color: Color value

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setHeaderFillStyle', {'color': color.get_hex()})
        return self

    def set_label_font(
            self,
            size: int | float,
            family: str = "Segoe UI, -apple-system, Verdana, Helvetica",
            style: str = 'normal',
            weight: str = 'normal'
    ):
        """Set the font of the node labels.

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

    def set_label_color(self, color: lightningchart.Color):
        """Set the color of the node labels.

        Args:
            color: Color value.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setLabelFillStyle', {'color': color.get_hex()})
        return self

    def set_node_border_style(
            self,
            thickness: int | float,
            color: lightningchart.Color
    ):
        """Set the line style of the node labels.

        Args:
            thickness (int | float): Thickness of the border.
            color (Color): Color of the border.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setNodeBorderStyle', {'thickness': thickness, 'color': color.get_hex()})
        return self

    def set_node_effect(self, enabled: bool):
        """Set theme effect enabled on component or disabled.

        Args:
            enabled: Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setNodeEffect', {'enabled': enabled})
        return self

    def set_cursor_mode(self, mode: str):
        """Set chart Cursor behavior.

        Args:
            mode (str): "disabled" | "show-all" | "show-all-interpolated" | "show-nearest" |
                "show-nearest-interpolated" | "show-pointed" | "show-pointed-interpolated"

        Returns:
            The instance of the class for fluent interface.
        """
        cursor_modes = (
            "disabled", "show-all", "show-all-interpolated", "show-nearest",
            "show-nearest-interpolated", "show-pointed", "show-pointed-interpolated"
        )
        if mode not in cursor_modes:
            raise ValueError(
                f"Expected mode to be one of {cursor_modes}"
                f", but got '{mode}'."
            )

        self.instance.send(self.id, 'setCursorMode', {'mode': mode})
        return self
