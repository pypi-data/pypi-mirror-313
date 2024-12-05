from __future__ import annotations

from lightningchart.charts import Chart
from lightningchart.series import SeriesWithAddDataPoints, Series, SeriesWithAddDataXYZ, SeriesWith3DPoints, \
    SeriesWith3DShading


class PointSeries3D(
    SeriesWithAddDataPoints,
    SeriesWithAddDataXYZ,
    SeriesWith3DPoints,
    SeriesWith3DShading
):
    """Series for visualizing 3D datapoints."""

    def __init__(
            self,
            chart: Chart,
            render_2d: bool = False,
            individual_lookup_values_enabled: bool = False,
            individual_point_color_enabled: bool = False,
            individual_point_size_axis_enabled: bool = False,
            individual_point_size_enabled: bool = False
    ):
        Series.__init__(self, chart)
        self.instance.send(self.id, 'pointSeries3D', {
            'chart': self.chart.id,
            'individualLookupValuesEnabled': individual_lookup_values_enabled,
            'individualPointColorEnabled': individual_point_color_enabled,
            'individualPointSizeAxisEnabled': individual_point_size_axis_enabled,
            'individualPointSizeEnabled': individual_point_size_enabled,
            'pointCloudSeries': render_2d
        })
