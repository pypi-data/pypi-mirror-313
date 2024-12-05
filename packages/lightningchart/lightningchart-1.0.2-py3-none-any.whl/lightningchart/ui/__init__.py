from __future__ import annotations
import uuid

import lightningchart


class UIElement:

    def __init__(self, chart):
        self.chart = chart
        self.instance = chart.instance
        self.id = str(uuid.uuid4()).split('-')[0]

    def dispose(self):
        """Permanently destroy the component.

        Returns:
            True
        """
        self.instance.send(self.id, 'dispose')
        return True

    def set_visible(self, visible: bool = True):
        """Set element visibility.

        Args:
            visible (bool): True when element should be visible and false when element should be hidden.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setVisible', {'visible': visible})
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


class UIEWithPosition(UIElement):

    def set_position(self, x: int | float, y: int | float):
        """Sets the position of this UiElement relative to its origin

        Args:
            x (int): Location in X-dimension.
            y (int): Location in Y-dimension.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setPosition', {'x': x, 'y': y})
        return self

    def set_origin(self, origin: str):
        """Sets the position of this UiElement relative to its origin.

        Args:
            origin (str): "Center" | "CenterBottom" | "CenterTop" | "LeftBottom" | "LeftCenter" |
                "LeftTop" | "RightBottom" | "RightCenter" | "RightTop"

        Returns:
            The instance of the class for fluent interface.
        """
        origins = (
            "Center", "CenterBottom", "CenterTop", "LeftBottom", "LeftCenter",
            "LeftTop", "RightBottom", "RightCenter", "RightTop"
        )
        if origin not in origins:
            raise ValueError(
                f"Expected origin to be one of {origins}"
                f", but got '{origin}'."
            )

        self.instance.send(self.id, 'setOrigin', {'origin': origin})
        return self

    def set_margin(self, margin: int | float):
        """Set margin around object in pixels.

        Args:
            margin (int | float): Number with pixel margins for all sides.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setMargin', {'margin': margin})
        return self

    def set_dragging_mode(self, mode: str):
        """Set dragging mode of object. Defines how the object can be dragged by mouse.

        Args:
            mode (str): "draggable" | "notDraggable" | "onlyHorizontal" | "onlyVertical"

        Returns:
            The instance of the class for fluent interface.
        """
        modes = ("draggable", "notDraggable", "onlyHorizontal", "onlyVertical")
        if mode not in modes:
            raise ValueError(
                f"Expected mode to be one of {modes}"
                f", but got '{mode}'."
            )

        self.instance.send(self.id, 'setDraggingMode', {'mode': mode})
        return self


class UIEWithTitle(UIElement):

    def set_title(self, title: str):
        """Set text of LegendBox title.

        Args:
            title (str): LegendBox title as a string.

        Returns:
            The instance of the class for fluent interface.
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

    def set_title_rotation(self, degrees: int | float):
        """Set rotation of Chart title.

        Args:
            degrees (int | float): Rotation in degrees.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setTitleRotation', {'value': degrees})
        return self


class UIEWithHighlight(UIElement):

    def set_highlight(self, highlight: bool | int | float):
        """Set state of component highlighting.

        Args:
            highlight (bool | int | float): Boolean or number between 0 and 1, where 1 is fully highlighted.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setHighlight', {'highlight': highlight})
        return self

    def set_highlight_on_hover(self, enabled: bool):
        """Set highlight on mouse hover enabled or disabled.

        Args:
            enabled (bool): Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setHighlightOnHover', {'enabled': enabled})
        return self
