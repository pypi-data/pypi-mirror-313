import torch
import numpy as np
import torch.nn as nn

class _sequenceEntropy___test(nn.Module):

    def __init__(self, H:object, temperature: int=1):
        super(_sequenceEntropy___test, self).__init__()
        self.hmod=H
        self.temp=temperature
        self.wndw = 3
        self.start_from = 1

    def forward(self, ex, ey):

        hx = self.hmod.unsummed(ex, ey)
        e = self.__window(hx.shape[0], self.wndw)

        q = (hx * e).sum(axis=-1)[e.sum(dim=-1)==self.wndw]

        return q.min(), e[self.start_from:][q.argmin()].bool()

    def __window(self, k:int, window_size:int):
        e = torch.eye(k)
        for i in range(len(e)):
            e[i,i:(i+self.wndw)] = 1
        return e[e.sum(dim=-1)==self.wndw]



class sequenceEntropy(nn.Module):

    def __init__(self, H:object, window_size: int=3):
        super(sequenceEntropy, self).__init__()
        self.hmod = H
        self.wndw = window_size
        self.start_from = 1

    def __window(self, k:int, window_size:int):
        e = torch.eye(k)
        for i in range(len(e)):
            e[i,i:(i+window_size)] = 1
        return e

    def forward(self, ex, ey):
        hx = self.hmod.unsummed(ex, ey)

        sel = (hx[self.start_from:].argmin()+1).detach().item()
        e = self.__window(
            k=len(hx),
            window_size=self.wndw
        )
        sel = e[:,sel]>0
        e = e[sel]
        res = (hx * e).sum(dim=-1)

        return res.min(), e[res.argmin()].bool()