import pandas as pd
import plotly
import plotly.graph_objs as go
import json

import numpy as np


def create_plot(mem):

    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe

    data = [
        go.Bar(
            x=['total', 'available', 'used', 'free'], # assign x as the dataframe column 'x'
            y=[ mem.total,  mem.available, mem.used,  mem.free]
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON