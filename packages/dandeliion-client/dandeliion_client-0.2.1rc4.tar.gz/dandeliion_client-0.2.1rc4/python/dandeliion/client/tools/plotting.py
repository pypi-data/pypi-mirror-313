import logging
import json
import os
import numpy as np
import plotly.graph_objects as go
from plotly.graph_objs.layout import Template
from . import misc

logger = logging.getLogger(__name__)

default_html_output = {
    'format': 'html',
    'args': {
        'include_mathjax': False,
        'include_plotlyjs': False,
        'full_html': False,
    }
}

default_layout = {
    'yaxis_tickformat': '~g'
}


def make_plot(data, layout=None, output=None):

    # output = misc.update_dict(target=default_output, updates=output, inline=False)
    layout = misc.update_dict(target=default_layout, updates=layout, inline=False)

    fig = go.Figure(layout=layout)

    for d in data:
        try:
            type_ = d['type'] if 'type' in d else 'Scatter'
            if type_ == 'Line':
                type_ = 'Scatter'
                d['mode'] = 'lines'
            elif type_ == 'Scatter' and 'mode' not in d:
                d['mode'] = 'markers'
            fig.add_trace(
                getattr(go, type_)(
                    **{i: d[i] for i in d if i not in ['type']}
                )
            )
        except Exception:
            pass  # skip if error happens

    if not output or 'format' not in output:
        return fig
    elif output['format'] == 'html':
        return fig.to_html(**(output['args'] if 'args' in output else {}))
    elif output['format'] in ['png', 'jpg', 'svg', 'pdf']:
        return fig.to_image(format=output['format'], **(output['args'] if 'args' in output else {}))


def plot_dat_file(file_path, **kwargs):
    try:
        data = np.loadtxt(file_path, skiprows=1)

    except OSError:
        logger.warning('Simulation output file not found: %s', file_path)
        return '<span>Simulation output file not found</span>'

    # casting tolist() makes testing easier
    return make_plot([{'x': data[:, 0].tolist(), 'y': data[:, 1].tolist()}], **kwargs)


with open(os.path.join(os.path.dirname(__file__), 'plotly_dandeliion_default.json')) as f:
    DANDELIION_THEME = Template(json.load(f), _validate=False)
