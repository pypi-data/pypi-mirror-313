""" Main
"""

import json
from eea.jupyter.controllers.plotly import PlotlyController


def uploadPlotly(url, fig, **metadata):
    """
    Uploads a Plotly chart to a specified URL.

    Parameters:
    - url (str): The URL where the chart will be uploaded.
    - fig (plotly.graph_objs.Figure): The Plotly figure object.
    - **metadata: Additional metadata to be passed to the PlotlyController.

    Returns:
    - The result of the PlotlyController's uploadPlotly method.
    """
    if url is None:
        raise ValueError("URL cannot be None")
    if fig is None:
        raise ValueError("Figure cannot be None")
    plotlyCtrl = PlotlyController(url)
    chart_data = fig if isinstance(fig, dict) else json.loads(fig.to_json())
    return plotlyCtrl.uploadPlotly(chart_data, **metadata)
