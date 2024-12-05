from __future__ import annotations

from lightningchart.charts import Chart
from lightningchart.ui.axis import Axis
from lightningchart.series import Series2D, SeriesWithAddDataPoints, SeriesWith2DLines, SeriesWith2DPoints, \
    SeriesWithAddDataXY, SeriesWithIndividualPoint, Series, PointLineAreaSeries


class SplineSeries(
    Series2D,
    SeriesWithAddDataPoints,
    SeriesWithAddDataXY,
    SeriesWith2DLines,
    SeriesWith2DPoints,
    SeriesWithIndividualPoint,
    PointLineAreaSeries,
):
    """Series for visualizing 2D splines."""

    def __init__(
            self,
            chart: Chart,
            resolution: int | float = 20,
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
        self.instance.send(self.id, 'splineSeries', {
            'chart': self.chart.id,
            'resolution': resolution,
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
