from plotly import colors
from dandeliion.client.tools import misc
import math

import logging
logger = logging.getLogger(__name__)


class Plot:
    def __init__(self, data=None, reqs=None, layout=None, output=None):
        self.data = data
        self.reqs = reqs
        self.layout = layout if layout else {}
        self.output = output

    def get_datafields(self, default=None):
        if self.reqs:
            return self.reqs
        elif self.data:
            # use reqs if present, otherwise collect data fields from data
            return ([d['field'] if isinstance(d, dict) else d for d in self.data])
        return default

    def prepare_data(self, data, default=[]):
        result = []
        for d in (self.data if self.data else default):
            xcol = d.get('xcol', 0)
            ycol = d.get('ycol', 1)
            data_ = misc.get_dict(data, *d['field'].split('.'))
            if type(xcol) is int:
                xcol = list(data_.keys())[xcol]
            if type(ycol) is int:
                ycol = list(data_.keys())[ycol]
            result.append(
                {'x': data_[xcol], 'y': data_[ycol],  # get right data columns from data
                 **{i: d[i] for i in d if i not in ['field', 'xcol', 'ycol']}} if isinstance(d, dict)
                else misc.get_dict(data, *d.split('.'))
            )
        return result


def LerpColour(c1, c2, t):
    return (c1[0] + (c2[0] - c1[0]) * t, c1[1] + (c2[1] - c1[1]) * t, c1[2] + (c2[2] - c1[2]) * t)


class SequencePlot(Plot):

    def __init__(self, data, reqs=None, layout=None, output=None):
        if data:
            data = [data]
        super().__init__(data=data, reqs=reqs, layout=layout, output=output)

    def prepare_data(self, data, default=[]):
        first = self.data[0].get('first', {})
        last = self.data[0].get('last', {})
        type_ = self.data[0].get('type', 'Scatter')

        # first_color = first.get('color', '#ff0000')
        first_color = first.get('color', '#0099ff')
        if type(first_color) is str:
            first_color = colors.hex_to_rgb(first_color)
        # last_color = last.get('color', '#0099ff')
        last_color = last.get('color', '#ff0000')
        if type(last_color) is str:
            last_color = colors.hex_to_rgb(last_color)

        data = misc.get_dict(data, *self.data[0]['field'].split('.'))
        xcol = self.data[0].get('xcol', 0)
        if type(xcol) is int:
            xcol = list(data.keys())[xcol]

        columns = list(data.keys())
        columns.remove(xcol)

        result = []
        steps = list(range(0, len(columns), math.ceil(len(columns) / 1000)))
        if not steps or steps[-1] != len(columns) - 1:
            steps.append(len(columns) - 1)
        for i in steps:
            color = colors.label_rgb(
                LerpColour(first_color, last_color, float(i) / (len(columns) - 1)) if len(columns) > 1 else first_color
            )
            result.append({
                'x': data[xcol],
                'y': data[columns[i]],
                'line_color': color,
                'line_width': 3 if i == 0 or i == len(columns) - 1 else 1,
                'name': columns[i],
                'type': type_,
            })
        return result
