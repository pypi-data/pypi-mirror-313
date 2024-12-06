import pandas as pd
import numpy as np
import torch
import plotly.express as px

from .recurrence_plot import recurrence_plot
from .TFIDF import TFIDF
from typing import Union


class explorer():

    def __init__(self, network_graph_object: object):
        super(explorer, self).__init__()
        self.G = network_graph_object
        self.c_tf_idf = None
        self.RMX = None
        self.odf = None


        self.minimum_similarity = 0.
        self.min_x = 5
        self.min_y = 5

    # def __recurrence_plot(self, zrange: int=5, colorscale='brbg', minimum_row_utterance_length: int=5, minimum_col_utterance_length: int=5, unidirectional: bool=False):
    #     resid = self.G.resid(flat=False)
    #     if resid.shape[0] == resid.shape[1]:
    #         resid = resid * (torch.eye(resid.shape[0]) == 0).float()
    #         row_mask = (self.G.GRAPH.N[:, 0] >= minimum_row_utterance_length).float().view(-1, 1)
    #         col_mask = (self.G.GRAPH.N[:, 0] >= minimum_col_utterance_length).float().view(1, -1)
    #
    #     else:
    #         row_mask = 1
    #         col_mask = 1
    #
    #     resid = (resid * row_mask) * col_mask
    #     if unidirectional:
    #         for i in range(resid.shape[0]):
    #             resid[i,:i] = 0.
    #
    #     if self.RMX == None:
    #         self.RMX = recurrence_plot(
    #             heatmap=resid,
    #             x_labels=self.G.x_labels,
    #             y_labels=self.G.y_labels
    #         )
    #
    #     return self.RMX.get_figure(zrange=zrange, colorscale=colorscale)

    def recurrence_plot(self, min_cutoff: int=0, zrange: int=5, colorscale='brbg', minimum_row_utterance_length: int=5, minimum_col_utterance_length: int=5, unidirectional: bool=False):
        # if not isinstance(self.odf, pd.DataFrame):
        #     self.odf = self.create_odf(
        #         min_cutoff=min_cutoff,
        #         minimum_x_length=minimum_row_utterance_length,
        #         minimum_y_length=minimum_col_utterance_length,
        #         unidirectional=unidirectional
        #     )
        #
        # self.RMX = recurrence_plot(
        #     df=self.odf,
        #     x_labels=list(self.G.x_labels[0].keys()),
        #     y_labels=list(self.G.y_labels[0].keys()),
        #     xid='idx',
        #     yid='idy',
        #     values_col='Hxy'
        # )
        #
        # return self.RMX.get_figure(zrange=zrange,colorscale=colorscale)
        return "Currently under construction!"


    def create_odf(self, min_cutoff: int=-100, minimum_x_length: int=5, minimum_y_length: int=5):
        self.odf = self.G.graph_df()

        self.odf = self.odf.loc[
            (self.odf['Hxy'] >= min_cutoff)
            & (self.odf['nx'] >= minimum_x_length)
            & (self.odf['ny'] >= minimum_y_length)
        ]

        self.odf = pd.concat(
            [
                pd.DataFrame(np.array(self.G.texts, dtype=object), columns=['text_x', 'text_y']),
                self.odf
            ], axis=1
        )


    def TFIDF(self, min_cutoff: float=0., extra_stop_words: list=[], k_topic_words: int=5, specific_texts: list=[], n_topics: Union[int,None]=None, n_cols: int=3, unidirectional: bool=False, minimum_x_length: int=5, minimum_y_length: int=5):

        if self.c_tf_idf == None:
            if (not isinstance(self.odf, pd.DataFrame)) or (min_cutoff != self.minimum_similarity) or (minimum_x_length != self.min_x) or (minimum_y_length != self.min_y):

                self.create_odf(
                    min_cutoff=min_cutoff,
                    minimum_x_length=minimum_x_length,
                    minimum_y_length=minimum_y_length
                )

            self.c_tf_idf = TFIDF(
                df=self.odf,
                text_col='text_y',
                topic_col='labels',
                stop_words=extra_stop_words
            )

            self.c_tf_idf.reverse_label_dic = {i:x for x,i in self.relabel.items()}
            # self.odf = self.c_tf_idf.df

        if specific_texts:
            return self.c_tf_idf.plot_topic_word_frequencies(
                k_words=k_topic_words,
                specific_topics=specific_texts,
                n_topics=n_topics,
                n_cols=n_cols
            )

        else:
            return self.c_tf_idf.plot_topic_word_frequencies(
                k_words=k_topic_words,
                n_topics=n_topics,
                n_cols=n_cols
            )

    def get_linked_examples(self, index: int, sample_size:int=5,                # query related
                            min_cutoff: float=0., unidirectional: bool=False,   # set-up related
                            minimum_x_length: int=5, minimum_y_length: int=5):

        if ((not isinstance(self.odf, pd.DataFrame))
                or (min_cutoff != self.minimum_similarity)
                or (minimum_x_length != self.min_x)
                or (minimum_y_length != self.min_y)):

            self.create_odf(
                min_cutoff=min_cutoff,
                minimum_x_length=minimum_x_length,
                minimum_y_length=minimum_y_length,
                unidirectional=unidirectional
            )

        sel = self.odf['labels'] == index

        return {
            'sentence': self.odf['x'].loc[sel].unique().tolist(),
            'examples': self.odf[['resid_H', 'y']].loc[sel].sample(n=sample_size).sort_values(by='resid_H').values.tolist()
        }