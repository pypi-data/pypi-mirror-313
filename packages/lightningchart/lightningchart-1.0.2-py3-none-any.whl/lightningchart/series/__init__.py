from __future__ import annotations

import uuid
import lightningchart
from lightningchart import charts
from lightningchart.utils import convert_to_list, convert_to_dict, convert_to_matrix


class Series:

    def __init__(self, chart: charts.Chart):
        self.chart = chart
        self.instance = chart.instance
        self.id = str(uuid.uuid4()).split('-')[0]

    def dispose(self):
        """Permanently destroy the component."""
        self.instance.send(self.id, 'dispose')

    def clear(self):
        """Clear all previously pushed data points from the series.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'clear')
        return self

    def set_visible(self, visible: bool):
        """Set element visibility.

        Args:
            visible (bool): true when element should be visible and false when element should be hidden.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setVisible', {'visible': visible})
        return self

    def set_highlight(self, highlight: bool | int | float):
        """
        Set state of component highlighting.

        Args:
            highlight (bool | int | float): Boolean or number between 0 and 1, where 1 is fully highlighted.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setHighlight', {'highlight': highlight})
        return self

    def set_name(self, name: str):
        """Sets the name of the Component updating attached LegendBox entries.

        Args:
            name (str): Name of the component.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setName', {'name': name})
        return self

    def set_mouse_interactions(self, enabled: bool):
        """Set mouse interactions enabled or disabled.

        Args:
            enabled (bool): Specifies state of mouse interactions.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setMouseInteractions', {'enabled': enabled})
        return self

    def set_draw_order(self, index: int | float):
        """Configure draw order of the series. The drawing order of series inside same chart can be configured by
        configuring their draw order index. This is a simple number that indicates which series is drawn first,
        and which last. The values can be any number, even a decimal. Higher number results in series being drawn
        closer to the top. By default, each series is assigned a running counter starting from 0 and increasing by 1
        for each series.

        Args:
            index (int | float): The draw order index.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setDrawOrder', {'index': index})
        return self


class ComponentWithPaletteColoring:

    def set_palette_coloring(
            self,
            steps: list[dict],
            look_up_property: str = 'value',
            interpolate: bool = True,
            percentage_values: bool = False
    ):
        """Define a palette for dynamically looked up fill coloring in the series.

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

        self.instance.send(self.id, 'setPalettedFillStyle', {
            'steps': steps,
            'lookUpProperty': look_up_property,
            'interpolate': interpolate,
            'percentageValues': percentage_values,
        })
        return self

    def set_color(self, color: lightningchart.Color):
        """Set a color fill for the series.

        Args:
            color (Color): Color of the series.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setSolidFillStyle', {'color': color.get_hex()})
        return self

    def set_empty_color_fill(self):
        """Set empty color fill for the series.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setEmptyFillStyle', {})
        return self


class ComponentWithPointPaletteColoring:

    def set_palette_point_coloring(
            self,
            steps: list[dict[str, any]],
            look_up_property: str = 'value',
            interpolate: bool = True,
            percentage_values: bool = False
    ):
        """Define a palette for dynamically looked up fill coloring in the series.

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

        self.instance.send(self.id, 'setPalettedPointFillStyle', {
            'steps': steps,
            'lookUpProperty': look_up_property,
            'interpolate': interpolate,
            'percentageValues': percentage_values,
        })
        return self


class ComponentWithLinePaletteColoring:

    def set_palette_line_coloring(
            self,
            steps: list[dict],
            look_up_property: str = 'value',
            interpolate: bool = True,
            percentage_values: bool = False
    ):
        """Define a palette for dynamically looked up fill coloring in the series.

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

        self.instance.send(self.id, 'setPalettedStrokeStyle', {
            'steps': steps,
            'lookUpProperty': look_up_property,
            'interpolate': interpolate,
            'percentageValues': percentage_values,
        })
        return self

class ComponentWithBipolarPaletteColoring:

    def set_negative_palette_coloring(
            self,
            steps: list[dict[str, any]],
            look_up_property: str = 'value',
            interpolate: bool = True,
            percentage_values: bool = False
    ):
        """Define a palette for dynamically looked up fill coloring in the series.

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

        self.instance.send(self.id, 'setNegativePalettedFillStyle', {
            'steps': steps,
            'lookUpProperty': look_up_property,
            'interpolate': interpolate,
            'percentageValues': percentage_values,
        })
        return self

    def set_positive_palette_coloring(
            self,
            steps: list[dict[str, any]],
            look_up_property: str = 'value',
            interpolate: bool = True,
            percentage_values: bool = False
    ):
        """Define a palette for dynamically looked up fill coloring in the series.

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

        self.instance.send(self.id, 'setPositivePalettedFillStyle', {
            'steps': steps,
            'lookUpProperty': look_up_property,
            'interpolate': interpolate,
            'percentageValues': percentage_values,
        })
        return self

class ComponentWithRangePaletteColoring:

    def set_low_palette_coloring(
            self,
            steps: list[dict[str, any]],
            look_up_property: str = 'value',
            interpolate: bool = True,
            percentage_values: bool = False
    ):
        """Define a palette for dynamically looked up fill coloring in the series.

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

        self.instance.send(self.id, 'setLowPalettedFillStyle', {
            'steps': steps,
            'lookUpProperty': look_up_property,
            'interpolate': interpolate,
            'percentageValues': percentage_values,
        })
        return self

    def set_high_palette_coloring(
            self,
            steps: list[dict[str, any]],
            look_up_property: str = 'value',
            interpolate: bool = True,
            percentage_values: bool = False
    ):
        """Define a palette for dynamically looked up fill coloring in the series.

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

        self.instance.send(self.id, 'setHighPalettedFillStyle', {
            'steps': steps,
            'lookUpProperty': look_up_property,
            'interpolate': interpolate,
            'percentageValues': percentage_values,
        })
        return self


class PointLineAreaSeries(Series, ComponentWithPointPaletteColoring, ComponentWithLinePaletteColoring):

    def append_json(self, data_array, data_properties):
        """Add several samples from dictionaries/JSON by reading values from instructed property names.

        Supported sample property types:
            * x
            * y
            * color
            * size
            * rotation
            * lookupValue
            * id

        Args:
            data_array: Array with dictionary/JSON objects which represent samples.
            data_properties: Object which informs which property names contain data.
                At least x or y property should always be specified.

        Returns:
            The instance of the class for fluent interface.
        """
        data_array = convert_to_dict(data_array)
        data_properties = convert_to_dict(data_properties)

        self.instance.send(self.id, 'appendJSON', {'array': data_array, 'properties': data_properties})
        return self

    def append_sample(
            self,
            x: int | float | str = None,
            y: int | float = None,
            lookup_value: int | float = None,
            id: int | float = None,
            size: int | float = None,
            rotation: int | float = None,
            color: str = None
    ):
        """Add one (1) sample to data set.

        Args:
            x (int | float): Single x value.
            y (int | float): Single y value.
            lookup_value (int | float): Single lookup value.
            id (int | float): Single id.
            size (int | float): Single size value.
            rotation (int | float): Single rotation value.
            color (str): Single HEX color value (NOT COLOR OBJECT)

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'appendSample', {
            'x': x,
            'y': y,
            'lookupValue': lookup_value,
            'id': id,
            'size': size,
            'rotation': rotation,
            'color': color,
        })
        return self

    def append_samples(
            self,
            x_values: list[int | float | str] = None,
            y_values: list[int | float] = None,
            lookup_values: list[int | float] = None,
            ids: list[int | float] = None,
            sizes: list[int | float] = None,
            rotations: list[int | float] = None,
            colors: list[str] = None,

            start: int | float = None,
            step: int | float = None,
            count: int | float = None,
            offset: int | float = None,
            offset_colors: int | float = None,
            offset_ids: int | float = None,
            offset_lookup_values: int | float = None,
            offset_rotations: int | float = None,
            offset_sizes: int | float = None,
    ):
        """Add a list of samples to data set.

        Args:
            x_values (list[int | float]): List of x values.
            y_values (list[int | float]): List of y values.
            lookup_values (list[int | float]): List of lookup values.
            ids (list[int | float]): List of ids.
            sizes (list[int | float]): List of size values.
            rotations (list[int | float]): List of rotation values.
            colors (list[str]): List of HEX strings (NOT COLOR OBJECTS!)
            start (int | float):
            step (int | float):
            count (int | float):
            offset (int | float):
            offset_colors (int | float):
            offset_ids (int | float):
            offset_lookup_values (int | float):
            offset_rotations (int | float):
            offset_sizes (int | float):

        Returns:
            The instance of the class for fluent interface.
        """
        x_values = convert_to_list(x_values)
        y_values = convert_to_list(y_values)
        lookup_values = convert_to_list(lookup_values)
        ids = convert_to_list(ids)
        sizes = convert_to_list(sizes)
        rotations = convert_to_list(rotations)
        colors = convert_to_list(colors)

        self.instance.send(self.id, 'appendSamples', {
            'colors': colors,
            'count': count,
            'ids': ids,
            'lookupValues': lookup_values,
            'offset': offset,
            'offsetColors': offset_colors,
            'offsetIds': offset_ids,
            'offsetLookupValues': offset_lookup_values,
            'offsetRotations': offset_rotations,
            'offsetSizes': offset_sizes,
            'rotations': rotations,
            'sizes': sizes,
            'start': start,
            'step': step,
            'xValues': x_values,
            'yValues': y_values,
        })
        return self

    def set_samples(
            self,
            x_values: list[int | float | str] = None,
            y_values: list[int | float] = None,
            lookup_values: list[int | float] = None,
            ids: list[int | float] = None,
            sizes: list[int | float] = None,
            rotations: list[int | float] = None,
            colors: list[str] = None,

            start: int | float = None,
            step: int | float = None,
            count: int | float = None,
            offset: int | float = None,
            offset_colors: int | float = None,
            offset_ids: int | float = None,
            offset_lookup_values: int | float = None,
            offset_rotations: int | float = None,
            offset_sizes: int | float = None,
    ):
        """Re-specify all values in the data set. This is a convenience method that is fundamentally equal to:

        series.clear().append_samples( ... )

        Args:
            x_values (list[int | float]): List of x values.
            y_values (list[int | float]): List of y values.
            lookup_values (list[int | float]): List of lookup values.
            ids (list[int | float]): List of ids.
            sizes (list[int | float]): List of size values.
            rotations (list[int | float]): List of rotation values.
            colors (list[str]): List of HEX strings (NOT COLOR OBJECTS!)
            start (int | float):
            step (int | float):
            count (int | float):
            offset (int | float):
            offset_colors (int | float):
            offset_ids (int | float):
            offset_lookup_values (int | float):
            offset_rotations (int | float):
            offset_sizes (int | float):

        Returns:
            The instance of the class for fluent interface.
        """
        x_values = convert_to_list(x_values)
        y_values = convert_to_list(y_values)
        lookup_values = convert_to_list(lookup_values)
        ids = convert_to_list(ids)
        sizes = convert_to_list(sizes)
        rotations = convert_to_list(rotations)
        colors = convert_to_list(colors)

        self.instance.send(self.id, 'setSamples', {
            'colors': colors,
            'count': count,
            'ids': ids,
            'lookupValues': lookup_values,
            'offset': offset,
            'offsetColors': offset_colors,
            'offsetIds': offset_ids,
            'offsetLookupValues': offset_lookup_values,
            'offsetRotations': offset_rotations,
            'offsetSizes': offset_sizes,
            'rotations': rotations,
            'sizes': sizes,
            'start': start,
            'step': step,
            'xValues': x_values,
            'yValues': y_values,
        })
        return self

    def alter_samples(
            self,
            index: int | float,
            x_values: list[int | float | str] = None,
            y_values: list[int | float] = None,
            lookup_values: list[int | float] = None,
            ids: list[int | float] = None,
            sizes: list[int | float] = None,
            rotations: list[int | float] = None,
            colors: list[str] = None,

            offset: int | float = None,
            offset_colors: int | float = None,
            offset_ids: int | float = None,
            offset_lookup_values: int | float = None,
            offset_rotations: int | float = None,
            offset_sizes: int | float = None,
    ):
        """Alter existing samples in the data set. This method also supports automatically appending samples when
        attempting to alter samples that don't exist in data set.

        This method alters existing samples by referencing sample indexes. This simply refers to an incrementing counter
        of when each sample was first introduced. For example, 0 refers to first sample that was added to data set.
        When data cleaning is enabled, sample indexes do NOT shift. They always point to unique samples, even if old
        samples are removed.

        Args:
            index: First altered sample index.
            x_values (list[int | float]): List of x values.
            y_values (list[int | float]): List of y values.
            lookup_values (list[int | float]): List of lookup values.
            ids (list[int | float]): List of ids.
            sizes (list[int | float]): List of size values.
            rotations (list[int | float]): List of rotation values.
            colors (list[str]): List of HEX strings (NOT COLOR OBJECTS!)
            offset (int | float):
            offset_colors (int | float):
            offset_ids (int | float):
            offset_lookup_values (int | float):
            offset_rotations (int | float):
            offset_sizes (int | float):

        Returns:
            The instance of the class for fluent interface.
        """
        x_values = convert_to_list(x_values)
        y_values = convert_to_list(y_values)
        lookup_values = convert_to_list(lookup_values)
        ids = convert_to_list(ids)
        sizes = convert_to_list(sizes)
        rotations = convert_to_list(rotations)
        colors = convert_to_list(colors)

        self.instance.send(self.id, 'alterSamples', {
            'index': index,
            'colors': colors,
            'ids': ids,
            'lookupValues': lookup_values,
            'offset': offset,
            'offsetColors': offset_colors,
            'offsetIds': offset_ids,
            'offsetLookupValues': offset_lookup_values,
            'offsetRotations': offset_rotations,
            'offsetSizes': offset_sizes,
            'rotations': rotations,
            'sizes': sizes,
            'xValues': x_values,
            'yValues': y_values,
        })
        return self

    def alter_samples_by_id(
            self,
            ids_to_alter: list[int | float],
            x_values: list[int | float | str] = None,
            y_values: list[int | float] = None,
            colors: list[str] = None,
            ids: list[int | float] = None,
            lookup_values: list[int | float] = None,
            rotations: list[int | float] = None,
            sizes: list[int | float] = None,
    ):
        """Alter existing samples in the data set.

        This method alters existing samples by referencing their ID properties.
        The ID property is an optional sample number property, which CAN be specified by the user.
        They have to be enabled using ids and afterwards can be added alongside other data properties, like x, y, etc.

        Args:
            ids_to_alter (list[int | float]): List of ids to alter.
            x_values (list[int | float]): List of x values.
            y_values (list[int | float]): List of y values.
            colors (list[str]): List of HEX strings (NOT COLOR OBJECTS!)
            ids (list[int | float]): List of ids.
            lookup_values (list[int | float]): List of lookup values.
            rotations (list[int | float]): List of rotation values.
            sizes (list[int | float]): List of size values.

        Returns:
            The instance of the class for fluent interface.
        """
        ids_to_alter = convert_to_list(ids_to_alter)
        x_values = convert_to_list(x_values)
        y_values = convert_to_list(y_values)
        colors = convert_to_list(colors)
        ids = convert_to_list(ids)
        lookup_values = convert_to_list(lookup_values)
        rotations = convert_to_list(rotations)
        sizes = convert_to_list(sizes)

        self.instance.send(self.id, 'alterSamplesByID', {
            'idsToAlter': ids_to_alter,
            'colors': colors,
            'ids': ids,
            'lookupValues': lookup_values,
            'rotations': rotations,
            'sizes': sizes,
            'xValues': x_values,
            'yValues': y_values,
        })
        return self

    def set_max_sample_count(self, max_sample_count: int, automatic: bool = True):
        """All real-time use cases (where data points are pushed in periodically) must define a "max sample count".
        This allocates the required amount of memory beforehand, which is crucial to get the best performance.

        Args:
            max_sample_count (int): After this sample count is reached, the oldest samples will start dropping out.
            automatic (bool): If true, the chart will first allocate only small amount of memory, and progressively
                increase memory allocation as samples come in until eventually limiting to max_sample_count.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setMaxSampleCount', {'max': max_sample_count, 'auto': automatic})
        return self


class SeriesWithAddDataPoints(Series):

    def add_dict_data(
            self,
            data: dict[str, int | float] | list[dict[str, int | float]]
    ):
        """Append a single datapoint or list of datapoints into the series.

        Args:
            data (dict[str, int | float] | list[dict[str, int | float]]): List of datapoints or a single datapoint.

        Returns:
            The instance of the class for fluent interface.
        """
        data = convert_to_dict(data)

        self.instance.send(self.id, 'addData', {'data': data})
        return self


class SeriesWithAddDataXY(Series):

    def add(self, *args: object, **kwargs: object):
        """Add xy-data to the series. Can be used in two ways:

        *  ```series.add(x, y)```, where x and y are lists containing numbers.

        * ```series.add(data)```, where data is array of dictionaries with x and y keys with numerical values.

        Returns:
            The instance of the class for fluent interface.
        """
        x = []
        y = []
        data = []

        if len(kwargs) > 0:
            if 'x' in kwargs:
                x = kwargs['x']
            if 'y' in kwargs:
                y = kwargs['y']
            if 'data' in kwargs:
                data = kwargs['data']
        elif len(args) == 2:
            x = args[0]
            y = args[1]
        elif len(args) == 1:
            data = args[0]

        x = convert_to_list(x)
        y = convert_to_list(y)

        if x or y:
            self.instance.send(self.id, 'addDataXY', {'x': x, 'y': y})
        if data:
            self.instance.send(self.id, 'addData', {'data': data})
        return self


class SeriesWithAddDataXYZ(Series):

    def add(self, *args, **kwargs):
        """Add xyz-data to the series. Can be used in two ways:

        *  ```series.add(x, y, z)```, where x, y, and z are lists containing numbers.

        * ```series.add(data)```, where data is array of dictionaries with x, y, and z keys with numerical values.

        Returns:
            The instance of the class for fluent interface.
        """
        x = []
        y = []
        z = []
        data = []

        if len(kwargs) > 0:
            if 'x' in kwargs:
                x = kwargs['x']
            if 'y' in kwargs:
                y = kwargs['y']
            if 'z' in kwargs:
                z = kwargs['z']
            if 'data' in kwargs:
                data = kwargs['data']
        elif len(args) == 3:
            x = args[0]
            y = args[1]
            z = args[2]
        elif len(args) == 1:
            data = args[0]

        x = convert_to_list(x)
        y = convert_to_list(y)
        z = convert_to_list(z)

        if x or y or z:
            self.instance.send(self.id, 'addDataXYZ', {'x': x, 'y': y, 'z': z})
        if data:
            self.instance.send(self.id, 'addData', {'data': data})
        return self


class SeriesWithDataCleaning(Series):

    def enable_data_cleaning(self, enabled: bool):
        """Enable automatic data cleaning for series.

        Args:
            enabled (bool): If true, automatic data cleaning is performed.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setDataCleaning', {'enabled': enabled})
        return self


class SeriesWithAddValues(Series):

    def add_values(
            self,
            y_values: list[list[int | float]] = None,
            intensity_values: list[list[int | float]] = None
    ):
        """Append values to the Surface Scrolling Grid Series.

        The series type can contain between 1 and 2 different data sets (Y values and Intensity values).
        This same method is used for managing both types of data;

        Args:
            y_values (list[list[int | float]]): a number matrix.
            intensity_values (list[list[int | float]]): a number matrix.

        Returns:
            The instance of the class for fluent interface.
        """
        y_values = convert_to_matrix(y_values)
        intensity_values = convert_to_matrix(intensity_values)

        self.instance.send(self.id, 'addValues', {
            'yValues': y_values,
            'intensityValues': intensity_values
        })
        return self


class SeriesWithInvalidateIntensity(Series):

    def invalidate_intensity_values(
            self,
            data: list[list[int | float]],
            column_index: int = None,
            row_index: int = None,
            sample_index: int = None
    ):
        """Invalidate range of surface intensity values starting from first column and row.

        Args:
            data (list[list[int | float]]): a number matrix.
            column_index (int): Index of first invalidated column.
            row_index (int): Index of first invalidated row.
            sample_index (int): The location along scrolling dimension is identified by a sample index.
                Sample index 0 would reference the first sample in the heatmap, whereas 1 the second sample.

        Returns:
            The instance of the class for fluent interface.
        """
        data = convert_to_matrix(data)

        self.instance.send(self.id, 'invalidateIntensityValues', {
            'data': data,
            'column': column_index,
            'row': row_index,
            'iSample': sample_index,
        })
        return self


class SeriesWithAddIntensityValues(Series):

    def add_intensity_values(self, new_data_points: list[list[int | float]]):
        """Push a Matrix of intensity values into the Heatmap grid. Each value describes one cell in the grid.

        Args:
            new_data_points (list[list[int | float]]): a number matrix.

        Returns:
            The instance of the class for fluent interface.
        """
        new_data_points = convert_to_matrix(new_data_points)

        self.instance.send(self.id, 'addIntensityValues', {'data': new_data_points})
        return self


class SeriesWithInvalidateData(Series):

    def add(self, data: dict[str, int | float] | list[dict[str, int | float]]):
        """Method for invalidating Box data. Accepts an Array of BoxDataCentered objects.
        Properties that must be defined for each NEW Box:

        "xCenter", "yCenter", "zCenter" | coordinates of Box in Axis values.

        "xSize", "ySize", "zSize" | size of Box in Axis values.

        Args:
            data (dict[str, int | float] | list[dict[str, int | float]]): List of BoxDataCentered objects.

        Returns:
            The instance of the class for fluent interface.
        """
        data = convert_to_dict(data)
        self.instance.send(self.id, 'invalidateData', {'data': data})
        return self


class SeriesWithAddArray(Series):

    def add_array_x(self, array: list[int | float]):
        """Append new data points into the series by only supplying X coordinates.

        Args:
            array (list[int | float]): List of numbers | Pandas DataFrame column | NumPy array

        Returns:
            The instance of the class for fluent interface.
        """
        array = convert_to_list(array)

        self.instance.send(self.id, 'addArrayX', {'array': array})
        return self

    def add_array_y(self, array: list[int | float]):
        """Append new data points into the series by only supplying Y coordinates.

        Args:
            array (list[int | float]): List of numbers | Pandas DataFrame column | NumPy array

        Returns:
            The instance of the class for fluent interface.
        """
        array = convert_to_list(array)

        self.instance.send(self.id, 'addArrayY', {'array': array})
        return self

    def add_arrays_xy(self, array_x: list[int | float], array_y: list[int | float]):
        """Append new data points into the series by supplying X and Y coordinates in two separated arrays.

        Args:
            array_x (list[int | float]): List of numbers | Pandas DataFrame column | NumPy array
            array_y (list[int | float]): List of numbers | Pandas DataFrame column | NumPy array

        Returns:
            The instance of the class for fluent interface.
        """
        array_x = convert_to_list(array_x)
        array_y = convert_to_list(array_y)

        self.instance.send(self.id, 'addArraysXY', {'arrayX': array_x, 'arrayY': array_y})
        return self


class SeriesWithIndividualPoint(Series):

    def set_individual_point_color_enabled(self, enabled: bool):
        """Enable or disable individual point color attributes.
        When enabled, each added data point can be associated with a color attribute.

        Args:
            enabled (bool): Individual point values enabled or disabled.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setIndividualPointColorEnabled', {'enabled': enabled})
        return self


class SeriesWith2DPoints(Series):

    def set_point_shape(self, shape: str = 'circle'):
        """Set shape of displayed points.

        Args:
            shape (str): "arrow" | "circle" | "cross" | "diamond" | "minus" | "plus" | "square" | "star" | "triangle"

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setPointShape', {'shape': shape})
        return self

    def set_point_color(self, color: lightningchart.Color):
        """Set the color of all 2D datapoints within a series.

        Args:
            color (Color): The color of the points.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setPointFillStyle', {'color': color.get_hex()})
        return self

    def set_point_size(self, size: int | float):
        """Set the size of all 2D datapoints within a series.

        Args:
            size (int | float): Size of a single datapoint in pixels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setPoint2DSize', {'size': size})
        return self

    def set_point_rotation(self, degrees: int | float):
        """Set the rotation of all 2D datapoints within a series.

        Args:
            degrees (int | float): Rotation in degrees.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setPointRotation', {'angle': degrees})
        return self


class SeriesWith3DPoints(Series):

    def set_point_color(self, color: lightningchart.Color):
        """Set the color of all 2D datapoints within a series.

        Args:
            color (Color): Color of the points.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setPoint3DFillStyle', {'color': color.get_hex()})
        return self

    def set_point_size(self, size: int | float):
        """Set the size of all 3D datapoints within a series.

        Args:
            size (int | float): Size of a single datapoint.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setPoint3DSize', {'size': size})
        return self

    def set_point_shape(self, shape: str = 'sphere'):
        """Set the shape of all 3D datapoints within a series.

        Args:
            shape (str): "cube" | "sphere"

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setPoint3DShape', {'shape': shape})
        return self

    def set_palette_point_colors(
            self,
            steps: list[dict],
            look_up_property: str = 'value',
            interpolate: bool = True,
            percentage_values: bool = False
    ):
        """Define a palette for dynamically looked up fill coloring for the points.

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

        self.instance.send(self.id, 'setPoint3DPalettedFillStyle', {
            'steps': steps,
            'lookUpProperty': look_up_property,
            'interpolate': interpolate,
            'percentageValues': percentage_values,
        })
        return self


class SeriesWith2DLines(Series):

    def set_line_color(self, color: lightningchart.Color):
        """Set the color of a 2D line series.

        Args:
            color (Color): The color of the line.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setLineFillStyle', {'color': color.get_hex()})
        return self

    def set_line_thickness(self, thickness: int | float):
        """Set the thickness of a 2D line series.

        Args:
            thickness (int | float): Thickness of the line. Use -1 thickness to enable primitive line rendering.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setLineThickness', {'width': thickness})
        return self

    def set_dashed(self, pattern: str = 'Dashed', thickness: int | float = None, color: lightningchart.Color = None):
        """Change the line stroke style to dashed line.

        Args:
            pattern (str): "DashDotted" | "Dashed" | "DashedEqual" | "DashedLoose" | "Dotted" | "DottedDense"
            thickness (int | float): Thickness of the line. Use -1 thickness to enable primitive line rendering.
            color (Color): The color of the line.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setDashedStroke', {'pattern': pattern, "thickness": thickness, "color": color})
        return self


class SeriesWith3DLines(Series):

    def set_line_color(self, color: lightningchart.Color):
        """Set the color of a 3D line series.

        Args:
            color (Color): The color of the line.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setLineFillStyle', {'color': color.get_hex()})
        return self

    def set_line_thickness(self, thickness: int | float):
        """Set the thickness of a 3D line series.

        Args:
            thickness (int | float): Thickness of the line. Use -1 thickness to enable primitive line rendering.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setLineThickness', {'width': thickness})
        return self


class SeriesWithWireframe(Series):

    def set_wireframe_stroke(self, thickness: int | float, color: lightningchart.Color):
        """Set the style of wireframe of the series.

        Args:
            thickness (int | float): Thickness of the wireframe.
            color (Color): Color of the wireframe.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setWireframeStyle', {'thickness': thickness, 'color': color.get_hex()})
        return self

    def hide_wireframe(self):
        """Hide the wireframe.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setEmptyWireframeStyle', {})
        return self


class SeriesWithInvalidateHeight(Series):

    def invalidate_height_map(
            self,
            data: list[list[int | float]],
            column_index: int = None,
            row_index: int = None
    ):
        """Invalidate range of surface height values starting from first column and row.
        These values correspond to coordinates along the Y axis.

        Args:
            data (list[list[int | float]]): a number matrix of height values.
            column_index (int): Index of the first column to be validated.
            row_index (int): Index of the first row to be validated.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'invalidateHeightMap', {
            'data': data,
            'column': column_index,
            'row': row_index
        })
        return self


class SeriesWithIntensityInterpolation(Series):

    def set_intensity_interpolation(self, enabled: bool):
        """Set surface intensity interpolation mode.

        Args:
            enabled (bool): If True, each pixel is colored based on a bi-linearly interpolated
                intensity value based on the 4 closest real intensity values.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setIntensityInterpolation', {'enabled': enabled})
        return self


class SeriesWithPixelInterpolation(Series):

    def set_pixel_interpolation(self, enabled: bool):
        """Set pixel interpolation mode.

         Args:
            enabled (bool): If True, each pixel is colored individually by bilinear interpolation.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setPixelInterpolationMode', {'enabled': enabled})
        return self


class SeriesWithCull(Series):

    def set_cull_mode(self, mode: str = 'disabled'):
        """Set culling of the series.

        Args:
            mode (str): "disabled" | "cull-back" | "cull-front"

        Returns:
            The instance of the class for fluent interface.
        """
        cull_modes = ("disabled", "cull-back", "cull-front")
        if mode not in cull_modes:
            raise ValueError(
                f"Expected mode to be one of {cull_modes}"
                f", but got '{mode}'."
            )

        self.instance.send(self.id, 'setCullMode', {'mode': mode})
        return self


class SeriesWith3DShading(Series):

    def set_depth_test_enabled(self, enabled: bool):
        """Set 3D depth test enabled for this series. By default, this is enabled,
        meaning that any series that is rendered after this series and is behind this series will not be rendered.
        Can be disabled to alter 3D rendering behavior.

        Args:
            enabled (bool): Depth test enabled?

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setDepthTestEnabled', {'enabled': enabled})
        return self

    def set_color_shading_style(
            self,
            phong_shading: bool = True,
            specular_reflection: float = 0.5,
            specular_color: lightningchart.Color = lightningchart.Color('#ffffff')
    ):
        """Set Color Shading Style for series.

        Args:
            phong_shading (bool): If True, use Phong shading style. If False, use simple shading style.
            specular_reflection (float): Controls specular reflection strength. Value ranges from 0 to 1.
                Default is 0.1.
            specular_color (Color): Specular highlight color.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setColorShadingStyle', {
            'phongShading': phong_shading,
            'specularReflection': specular_reflection,
            'specularColor': specular_color.get_hex()
        })
        return self


class Series2D(Series):

    def set_cursor_enabled(self, enabled: bool):
        """Configure whether cursors should pick on this particular series or not.

        Args:
            enabled (bool): Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setCursorEnabled', {'enabled': enabled})
        return self
