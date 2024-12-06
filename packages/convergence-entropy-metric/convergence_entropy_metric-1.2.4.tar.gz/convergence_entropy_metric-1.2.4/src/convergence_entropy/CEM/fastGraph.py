import torch
import torch.nn as nn
import numpy as np
from datetime import datetime as dt
from itertools import combinations

class fastGraph(nn.Module):

    def __init__(self, edge_fn, mode='list'):
        super(fastGraph, self).__init__()

        self.edge = edge_fn
        self.l = None
        self.S = None
        self.mode = mode
        self.verbose_exceptions = False
        self.max_baseline_entropy = 100.0



    def _list(self, Ex, ids, timed=False):
        """

        :param Ex: Vectors used to represent each utterance.
        :param ids: 1:1 label for the example number of each vec in Ex
        :return: None. Creates dynamic socio-semantic graph
        """
        l = np.unique(ids)
        combos = []
        for i, _ in enumerate(l):
            for j, _ in enumerate(l):
                combos += [np.sort([i, j])]
        combos = np.unique(combos, axis=0)

        self.S = torch.zeros(size=(len(l), len(l))) + self.max_baseline_entropy

        if timed:
            start = dt.now()

        for i, j in combos:
            ij, ji = self.edge(Ex[ids == l[i]], Ex[ids == l[j]])
            self.S[i, j] = ij
            self.S[j, i] = ji

        if timed:
            end = dt.now()
            print(end-start)

    def _df(self, df, vec_col, timed=False):
        self.S = torch.zeros(size=(len(df), len(df)))
        combos = combinations(df.index.values, 2)

        if timed:
            start = dt.now()

        for i,j in combos:

            try:
                Ex, Ey = df[vec_col].loc[i], df[vec_col].loc[j]
                # print((i,j), Ex.shape, Ey.shape)
                ij, ji = self.edge(Ex,Ey)
                self.S[i,j] = ij
                self.S[j,i] = ji

            except Exception as ex:
                if self.verbose_exceptions:
                    print((i,j), ex)

        if timed:
            end = dt.now()
            print(end-start)

    def fit(self, Ex=None, ids=None, df=None, vec_col=None, timed=False):
        if self.mode == 'list':
            self._list(Ex=Ex,ids=ids, timed=timed)
        else:
            self._df(df=df,vec_col=vec_col,timed=timed)

    def fit_subgraph(self, Ex, labels, x_set, y_set, timed=False, max_lexical_items=None):
        self.edge.on = -1

        if timed:
            start = dt.now()

        xdic = {l:i for i,l in enumerate(np.unique(x_set))}
        ydic = {l:i for i,l in enumerate(np.unique(y_set))}

        combos = np.array(sum([[[x,y] for y in y_set] for x in x_set], []))

        self.S = torch.zeros(size=(len(xdic), len(ydic)))

        for x,y in combos:
            self.S[xdic[x], ydic[y]] = self.edge(Ex[labels == x][max_lexical_items:], Ex[labels == y][max_lexical_items:])

        if timed:
            end = dt.now()
            print(end - start)

    def __getitem__(self, item):
        return self.S[item]
