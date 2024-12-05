from __future__ import annotations

from lightningchart.charts import Chart
from lightningchart.ui.axis import Axis
from lightningchart.series import Series2D, SeriesWithAddDataPoints, SeriesWithAddDataXY, SeriesWith2DPoints, \
    SeriesWithIndividualPoint, Series, PointLineAreaSeries


class PointSeries(
    Series2D,
    SeriesWithAddDataPoints,
    SeriesWithAddDataXY,
    SeriesWith2DPoints,
    SeriesWithIndividualPoint,
    PointLineAreaSeries,
):
    """Series for visualizing 2D datapoints."""

    def __init__(
            self,
            chart: Chart,
            data_pattern: str = None,
            colors: bool = False,
            lookup_values: bool = False,
            ids: bool = False,
            sizes: bool = False,
            rotations: bool = False,
            auto_sorting_enabled: bool = False,
            x_axis: Axis = None,
            y_axis: Axis = None,
    ):
        Series.__init__(self, chart)
        self.instance.send(self.id, 'pointSeries2D', {
            'chart': self.chart.id,
            'dataPattern': data_pattern,
            'colors': colors,
            'lookupValues': lookup_values,
            'ids': ids,
            'sizes': sizes,
            'rotations': rotations,
            'autoSortingEnabled': auto_sorting_enabled,
            'xAxis': x_axis,
            'yAxis': y_axis,
        })
