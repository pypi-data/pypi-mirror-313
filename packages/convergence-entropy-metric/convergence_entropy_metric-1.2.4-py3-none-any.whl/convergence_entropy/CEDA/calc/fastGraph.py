import torch
import torch.nn as nn

import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from itertools import combinations,product
from datetime import datetime as dt

from sklearn.linear_model import Ridge as LREG



################################################################################
### Fast Graph with End-to-End H-analyzer and flat M matrix
################################################################################
# The code here also includes a number of useful extras, which includes creating
#  a matrix that corresponds to the number of tokens in each value, and a script
#  to return a residual plot after regressing the entropy scores by N-tokens.
class fastFlatGraphWithAnalyzer(nn.Module):

    def __init__(self, analyzer_object: object, timed: bool=False):
        super(fastFlatGraphWithAnalyzer, self).__init__()

        self.analyzer = analyzer_object
        self.analyzer.dim = None

        self.M, self.N, self.beta = [], [], None
        self.timed = timed

        self.id_dic = None
        self._square = False

    def fit(self, x: list, y: list):

        self.M = torch.zeros(size=(len(x), 2))
        self.N = torch.zeros(size=(len(x), 2))

        for (i, (x_, y_)) in tqdm(enumerate(list(zip(x,y)))):
            H, N = self.analyzer(x_, y_)
            self.M[i, 0] = H[0].detach().cpu()
            self.M[i, 1] = H[1].detach().cpu()

            self.N[i,0] = N[0]
            self.N[i,1] = N[1]

    def update(self,  x: list, y: list):
        K = int(len(self.M))

        self.M = torch.cat([self.M, torch.zeros(size=(len(x),2))], axis=0)
        self.N = torch.cat([self.N, torch.zeros(size=(len(x),2))], axis=0)

        for (i, (x_, y_)) in tqdm(enumerate(list(zip(x,y)))):
            H, N = self.analyzer(x_, y_)
            self.M[K+i, 0] = H[0].detach().cpu()
            self.M[K+i, 1] = H[1].detach().cpu()

            self.N[K+i,0] = N[0]
            self.N[K+i,1] = N[1]

    def __regression_beta(self):

        results = LREG(fit_intercept=False)
        y = torch.cat([self.M[:,0], self.M[:,1]]).unsqueeze(-1).numpy()
        x = torch.cat([self.N[:,0], self.N[:,1]]).unsqueeze(-1).numpy()
        results.fit(x,y)

        return results.coef_.reshape(-1)[0]

    def residual(self):
        if self.beta == None:
            self.beta = self.__regression_beta()

        M = (self.beta * self.N) - self.M

        return M



################################################################################
### Fast Graph with End-to-End H-analyzer
################################################################################
# The code here also includes a number of useful extras, which includes creating
#  a matrix that corresponds to the number of tokens in each value, and a script
#  to return a residual plot after regressing the entropy scores by N-tokens.
class fastGraphWithAnalyzer(nn.Module):

    def __init__(self, analyzer_object: object, timed: bool=False):
        super(fastGraphWithAnalyzer, self).__init__()

        self.analyzer = analyzer_object
        self.analyzer.dim = None

        self.M, self.N, self.beta = None, None, None
        self.timed = timed

        self.id_dic = None

    def fit(self, corpus: list[str]):
        self.M = torch.zeros(size=(len(corpus), len(corpus)))
        self.N = torch.zeros(size=(len(corpus), 1))

        print('creating combinations')
        combos = list(combinations(list(range(len(corpus))),2))

        if self.timed:
            start = dt.now()

        for x,y in tqdm(combos):
            H, N = self.analyzer(corpus[x], corpus[y])
            self.M[x,y] = H[0].detach().cpu()
            self.M[y,x] = H[1].detach().cpu()

            self.N[x] = N[0]
            self.N[y] = N[1]

        if self.timed:
            print(dt.now()-start)

    def asymmetric_fit(self, x: list[str], y: list[str]):
        corpus = x + y
        self.M = torch.zeros(size=(len(corpus), len(corpus)))
        self.N = torch.zeros(size=(len(corpus), 1))

        combos = combinations(list(range(len(corpus))),2)
        combos = [c for c in combos if ((c[0] < len(x)) and (c[1] >= len(x)))]

        if self.timed:
            start = dt.now()

        for x_,y_ in tqdm(combos):
            if (self.M[x_, y_] == 0) and (self.M[y_, x_] == 0):
                H, N = self.analyzer(corpus[x_], corpus[y_])
                self.M[x_, y_] = H[0].detach().cpu()
                self.M[y_, x_] = H[1].detach().cpu()

                self.N[x_] = N[0]
                self.N[y_] = N[1]

        if self.timed:
            print(dt.now()-start)

    def explicit_fit(self, x: list[str], y: list[str]):
        # ToDo: redo this such that
        #   (1) We get unique indexes for every x (x -> np.array(x)[sel] where sel=x \in np.unique(x, sort=False) )
        #   (2) We get unique indexes for every y

        x_dic = {x[idx]:i for i,idx in enumerate(np.unique(x,return_index=True)[1])}
        y_dic = {y[idx]: i+len(x_dic) for i, idx in enumerate(np.unique(y, return_index=True)[1])}

        self.M = torch.zeros(size=(len(x_dic)+len(y_dic), len(x_dic)+len(y_dic)))
        self.N = torch.zeros(size=(len(x_dic)+len(y_dic),1))

        if self.timed:
            start = dt.now()

        for x_,y_ in tqdm(list(zip(x,y))):
            if (self.M[x_dic[x_], y_dic[y_]] == 0):
                H, N = self.analyzer(x_, y_)
                self.M[x_dic[x_], y_dic[y_]] = H[0].detach().cpu()
                self.M[y_dic[y_], x_dic[x_]] = H[1].detach().cpu()

                self.N[x_dic[x_]] = N[0]
                self.N[y_dic[y_]] = N[1]

        if self.timed:
            print(dt.now()-start)

    def __regression_beta(self):

        results = LREG(fit_intercept=False)
        y = self.M.reshape(-1,1).numpy()

        # dealing with asymmetric matrices for residualization
        if self.M.shape[0] != self.M.shape[-1]:
            self.reps = int(len(y) / self.M.shape[0])
            x = self.N[:self.M.shape[0]].view(-1).repeat(1, 1, self.reps).squeeze(1).T.numpy()
        else:
            x = self.N.reshape(-1, 1).numpy()

        results.fit(
            x,
            y
        )
        return results.coef_.reshape(-1)[0]

        # return self.set_beta()

    def residual(self):
        if self.beta == None:
            self.beta = self.__regression_beta()

        if self.M.shape[0] == self.M.shape[1]:
            resid_plot = (self.beta * self.N) - self.M
        else:
            resid_plot = (self.beta * self.N[:self.M.shape[0]]) - self.M

        return resid_plot

    def fit_with_indexes(self, corpus: np.ndarray, indexes: np.ndarray):
        IDX = list(set(indexes))

        self.id_dic = {idx:i for i,idx in enumerate(IDX)}
        self.M = torch.zeros(size=(len(IDX), len(IDX)))
        self.N = torch.zeros(size=(len(IDX),))

        print('creating combinations')
        combos = list(combinations(IDX,2))

        if self.timed:
            start = dt.now()

        for x,y in tqdm(combos):
            i,j = self.id_dic[x], self.id_dic[y]
            H, N = self.analyzer(corpus[indexes==x], corpus[indexes==y])
            self.M[i,j] = H[0].detach().cpu()
            self.M[j,i] = H[1].detach().cpu()

            self.N[i] = N[0]
            self.N[j] = N[1]

        if self.timed:
            print(dt.now()-start)



################################################################################
### Generic Fast Graph
################################################################################
class fastGraph(nn.Module):

    def __init__(self, edge_fn, mode='list'):
        super(fastGraph, self).__init__()

        self.edge = edge_fn
        self.l = None
        self.S = None
        self.mode = mode
        self.verbose_exceptions = False
        self.max_baseline_entropy = 100.0
        self.current_text = ''
        self.current_x = None

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



################################################################################
### Easy object for running reddit, unidirectional analysis.
################################################################################
def reddit_unidirectional_entropy(df, H, output_path, meta_data_cols, total_combinations, start_new_outputs_file=True, verbose=False):

    dfposteriors = pd.DataFrame(
        columns=['x', 'y', 'nx', 'ny', 'H'] + ['x_' + col for col in meta_data_cols] + ['y_' + col for col in meta_data_cols])

    if (not os.path.exists(output_path))or start_new_outputs_file:
        dfposteriors.to_csv(output_path, index=False, encoding='utf-8')

    begin, k, x_id, ex = dt.now(), 0, None, None
    with torch.no_grad():
        for (i, j) in tqdm(total_combinations):

            k += 1
            try:

                if i != x_id:
                    x_id = i
                    xsel = df['comment_id'].isin([i]).values
                    ex = df['vec'].loc[xsel].apply(
                        lambda x: str(x).replace('[', '').replace(']', '').replace(', ', 'SEP')).values
                    ex = np.concatenate([np.array(x.split('SEP')).reshape(1, -1).astype(float) for x in ex], axis=0)
                    ex = torch.FloatTensor(ex).cuda()
                    x_meta_data = df[meta_data_cols].loc[xsel].values[0].tolist()

                ysel = df['comment_id'].isin([j]).values
                ey = df['vec'].loc[ysel].apply(
                    lambda x: str(x).replace('[', '').replace(']', '').replace(', ', 'SEP')).values
                ey = np.concatenate([np.array(x.split('SEP')).reshape(1, -1).astype(float) for x in ey], axis=0)
                ey = torch.FloatTensor(ey).cuda()
                y_meta_data = df[meta_data_cols].loc[ysel].values[0].tolist()

                Hij, _ = H(ex, ey)
                Hij = Hij.detach().cpu().item()

                df_ij = [
                    [i, j, ex.shape[0], ey.shape[0], Hij] + x_meta_data + y_meta_data,
                    # [j, i, yt, xt, ey.shape[0], Hji]+y_meta_data+x_meta_data+['comment from prompt']
                ]

                df_ij = np.array(df_ij)
                df_ij = pd.DataFrame(df_ij, columns=list(dfposteriors))
                df_ij.to_csv(output_path, index=False, header=False, mode='a', encoding='utf-8')

            except Exception as ERR:
                if verbose:
                    print(ERR)
