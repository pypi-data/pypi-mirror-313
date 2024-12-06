import numpy as np
import plotly.graph_objects as go
from tqdm import tqdm
from itertools import product


class recurrence_plot():

    def __init__(self, df, x_labels, y_labels, xid, yid, values_col, decimal=2):
        super(recurrence_plot, self).__init__()
        """
        labels need to be in the following format:
        x_labels = [
            {
                'label_name_1': value,
                . . .
                'label_name_k': value,
            },
            {
                'label_name_1': value,
                . . .
                'label_name_k': value,
            }
        ]

        or in other words, labels for x and labels for y need to be provided in the 
        form of a list of a list of dictionaries, where every dictionary contains all
        relevant label names and values.
        """
        # ToDo:
        #   (1) Create pivot table from passed odf
        #       (1.1) pivot table of Hxy values
        #       (1.2) pivot table of processed, custom labels . . . use .apply(..., axis=1) to apply function across
        #           multiple columns :)

        self.xid = xid
        self.yid = yid
        self.val = values_col
        self.hmap = df.drop_duplicates(subset=[xid,yid]).pivot(xid, yid, values_col)
        self.labels = self.__custom_data(df, x_labels, y_labels, decimals=decimal)


    def __format_num(self, x, decimals):
        if isinstance(x,float):
            return np.around(x,decimals=decimals)
        else:
            return x

    def __custom_data(self, df, x_labels, y_labels=[], decimals: int=3):
        x_data = df.apply(
            lambda x:
            '<br>'.join([
                '<b>{}:</b> {}'.format(label, self.__format_num(x[label],decimals=decimals))
            for label in x_labels]), axis=1)

        y_data = df.apply(
            lambda x:
            '<br>'.join([
                '<b>{}:</b> {}'.format(label, self.__format_num(x[label], decimals=decimals))
                for label in y_labels]), axis=1)

        core = df[self.val].apply(lambda x: str(np.around(x,decimals=decimals))).astype(str)

        df['custom_data'] = core + '<br><br>' + x_data + '<br><br>' + y_data

        return df.pivot(self.xid, self.yid, 'custom_data')

    def get_figure(self, zrange: int = 5, colorscale: str = 'brbg'):
        custom_template = '%{customdata}'

        layout = go.Layout(
            title='Recurrence Plot',
            xaxis=go.XAxis(
                title='',
                showticklabels=False
            ),
            yaxis=go.YAxis(
                title='',
                showticklabels=False
            )
        )

        heat = go.Heatmap(
            z=self.hmap.values,
            # y=data['name'].values,
            # x=data_names,
            colorscale=colorscale,
            zmax=zrange,
            zmin=-zrange,
            zmid=0,
            customdata=self.labels.values,
            hovertemplate=custom_template,
        )

        return go.Figure(heat, layout=layout)

class _recurrence_plot():

    def __init__(self, heatmap, x_labels, y_labels, decimal=2):
        super(_recurrence_plot,self).__init__()
        """
        labels need to be in the following format:
        x_labels = [
            {
                'label_name_1': value,
                . . .
                'label_name_k': value,
            },
            {
                'label_name_1': value,
                . . .
                'label_name_k': value,
            }
        ]
        
        or in other words, labels for x and labels for y need to be provided in the 
        form of a list of a list of dictionaries, where every dictionary contains all
        relevant label names and values.
        """
        self.hmap = heatmap
        self.labels = self.__custom_data(x_labels,y_labels,decimals=decimal)

    def __custom_data(self, x_labels, y_labels, decimals):
        y_custom_data = ['<br>'.join(['<b>{}:</b> {}'.format(k,v) for k,v in y_label.items()]) for y_label in y_labels]
        x_custom_data = ['<br>'.join(['<b>{}:</b> {}'.format(k,v) for k,v in x_label.items()]) for x_label in x_labels]

        combos = product(list(range(len(x_custom_data))), list(range(len(y_custom_data))))
        combos = ['{}<br>'.format(self.hmap[c[0], c[1]])+x_custom_data[c[0]]+y_custom_data[c[1]] if (self.hmap[c[0], c[1]] > 0) else '' for c in tqdm(combos)]
        combos = np.array(combos, dtype=object).reshape(len(x_custom_data), len(y_custom_data))

        return combos
        # return [['{}<br>'.format(np.around(self.hmap[i,j].item(), decimals=decimals)) + x +'<br><br>' + y for j,y in enumerate(y_custom_data)] for i,x in tqdm(enumerate(x_custom_data))]

    def get_figure(self, zrange: int=5, colorscale: str='brbg'):
        custom_template = '%{customdata}'

        layout = go.Layout(
            title='Recurrence Plot',
            xaxis=go.XAxis(
                title='',
                showticklabels=False
            ),
            yaxis=go.YAxis(
                title='',
                showticklabels=False
            )
        )

        heat = go.Heatmap(
            z=self.hmap,
            # y=data['name'].values,
            # x=data_names,
            colorscale=colorscale,
            zmax=zrange,
            zmin=-zrange,
            zmid=0,
            customdata=self.labels,
            hovertemplate=custom_template,
        )

        return go.Figure(heat,layout=layout)
