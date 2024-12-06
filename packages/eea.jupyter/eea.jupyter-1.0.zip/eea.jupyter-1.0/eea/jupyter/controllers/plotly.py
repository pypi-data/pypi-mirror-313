"""PlotlyController
"""
from urllib.parse import urlparse
import os
import json
import requests
import IPython


class PlotlyController:
    """
    A class that represents a Plotly controller.

    Attributes:
      url (str): The URL of the plotly visualization to be added or edited.

    Methods:
      __init__(self, url): new instance of the PlotlyController class.
      uploadPlotly(self, chart_data, metadata): Uploads Plotly chart data.
    """

    def __init__(self, url):
        """
        Initializes a Plotly object with the given URL.

        Args:
            url (str): The URL to be parsed and used to initalize the object.
        """
        self.url_tuple = urlparse(url)
        self.host = self.url_tuple.scheme + "://" + self.url_tuple.netloc
        self.path = self.__sanitizePath(self.url_tuple.path)
        self.path_parts = self.path.split('/')

    def __sanitizePath(self, path):
        """
        Sanitizes the given path.

        Args:
            path (str): The path to be sanitized.

        Returns:
            str: The sanitized path.
        """
        return path.replace("/edit", "").replace("/add", "").rstrip('/')

    def uploadPlotly(self, chart_data, **metadata):
        """
        Uploads a Plotly chart to a specified path and show iframe.

        Args:
            metadata (dict): Additional metadata for the chart.

        Returns:
            IPython.display.HTML: The HTML code to display the Plotly chart.
        """
        parent_path = self.path_parts[:-1]
        parent_status = requests.get(
            self.host + '/'.join(parent_path)).status_code

        if parent_status == 404:
            print(
                "The path %s does not exist! Please try again." %
                ('/'.join(parent_path)))
            return None
        url = self.host

        status = requests.get(self.host + self.path).status_code

        if status in [200, 401, 403]:
            url += self.path + '/edit'
        else:
            url += '/'.join(parent_path) + '/add?type=visualization'

        html = """
        <div>
            <script>({})()</script>
            <iframe name="jupyter" src="{}" width="100%" height="1080""/>
        </div>""".format(
            self.__getOnLoadHandlerJS(chart_data, **metadata),
            url
        )
        return IPython.display.HTML(html)

    def __getOnLoadHandlerJS(self, chart_data, **metadata):
        """
        Returns the JavaScript code for the onLoad handler.

        Args:
            chart_data (dict): The chart data.
            metadata (dict, optional): Additional metadata. Defaults to {}.

        Returns:
            str: The JavaScript code for the onLoad handler.
        """
        metadata["id"] = self.path_parts[-1]
        with open(
            os.path.dirname(
                os.path.abspath(__file__)
            ) + '/../scripts/plotly.js',
            'r'
        ) as file:
            js_template = file.read()

        js_code = js_template.replace('__PROPS__', json.dumps({
            "host": self.host,
            "content": {
                **(metadata or {}),
                "visualization": {
                    "chartData": chart_data
                }
            }
        }))

        return js_code
