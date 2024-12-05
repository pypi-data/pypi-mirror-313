import typing

from pydantic import BaseModel

from icplot.color import Color


class PlotSeries(BaseModel):
    """
    A data series in a plot, such as a single line in a line-plot

    :param position_right: allows the series to be plotted on the right y-axis.
    :type position_right: bool, optional
    """

    label: str
    color: Color = Color()
    series_type: str = ""
    highlight: bool = False
    position_right: bool = False


class ImageSeries(PlotSeries):
    """
    A plot data series where the elements are images
    """

    data: typing.Any
    transform: typing.Any
    series_type: str = "image"


class LinePlotSeries(PlotSeries):
    """
    A plot series for line plots

    :param drawstyle: Naming comes from matplotlib API, allows for various square plots,
               default is a normal point to point line plot.
    :type drawstyle: str, optional
    """

    x: list
    y: list
    marker: str = "o"
    series_type: str = "line"
    drawstyle: str = "default"


class ScatterPlotSeries(PlotSeries):

    data: typing.Any
    series_type: str = "scatter"
