import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from tqdm import tqdm

from typing import Union
import numpy.typing as npt

from .end_to_end_analysis import analyzer
from .fastGraph import fastFlatGraphWithAnalyzer as FGA
from .entropy import entropy_cdf as entropy
from .wv_model import wv as embeddings
from itertools import combinations

class model(nn.Module):

    def __init__(
            self,
            sigma: float = 1.,
            device: str = 'cpu',
            wv_model: str = 'roberta-base',
            wv_layers: list[int] = [8, -1],
    ):
        super(model, self).__init__()
        self.meta_data = []  # Labels for rows and cols. Inits as null.
        self.texts = []  # retains the texts used to build cTFIDF.

        self.wvs = embeddings(  # Word vector model for reading in text
            model=wv_model,  # inputs.
            device=device,
            layers=wv_layers
        )

        self.H = analyzer(  # Class that preprocesses texts into word
            self.wvs,  # word vectors and passes them to an
            sim_model=entropy(  # entropy class object.
                sigma=sigma,
                dim=None,
                device=device
            )
        )

        self.GRAPH = FGA(  # Graph object to run complete, end-to-end
            analyzer_object=self.H  # analysis and hold a graph of connections
        )

    def fit(self, x: list, y: list, meta_data: list = [], save_texts: bool=False):

        if len(self.GRAPH.M) == 0:
            self.GRAPH.fit(x, y)

            if save_texts:
                self.texts = list(zip(x,y))

            if meta_data:
                self.meta_data = meta_data

        else:
            self.GRAPH.update(x, y)

            if save_texts:
                self.texts += list(zip(x,y))

            if meta_data:
                self.meta_data += meta_data

    def add_meta_data(self, meta_data: list[dict]):
        self.meta_data += meta_data

    def graph_df(self, residualize: bool=False):

        if residualize:
            df = pd.DataFrame(
                np.concatenate([self.GRAPH.N.numpy(), self.GRAPH.residual().numpy()], axis=-1),
                columns=['nx', 'ny', 'Hxy', 'Hyx']
            )

        else:
            df = pd.DataFrame(
                np.concatenate([self.GRAPH.N.numpy(), self.GRAPH.M.numpy()], axis=-1),
                columns=['nx', 'ny', 'Hxy', 'Hyx']
            )

        if self.meta_data and (len(self.meta_data) == len(df)):
            df = pd.concat([
                pd.DataFrame(self.meta_data),
                df
            ], axis=1)

        return df

    def checkpoint(self, file_name: str='CEDA-ckpt.pt'):
        torch.save(
            {
                'M': self.GRAPH.M,
                'N': self.GRAPH.N,
                'meta_data': self.meta_data,
                # 'y_labels': self.y_labels,
                'texts': self.texts,
                'square': self.GRAPH._square
            },
            file_name
        )

    def load_from_checkpoint(self, file_name: str='CEDA-ckpt.pt'):
        ckpt = torch.load(file_name)

        self.GRAPH.M = ckpt['M']
        self.GRAPH.N = ckpt['N']
        self.meta_data = ckpt['meta_data']
        # self.y_labels = ckpt['y_labels']
        self.texts = ckpt['texts']
        self.GRAPH._square = ckpt['square']

        # ensures freeing up of memory
        del ckpt





