import numpy as np
import torch
import torch.nn as nn
from typing import List, Union

from .entropy import entropy as H
from .language_model import languageModel
from .multi_level_language_model import model as languageModelLayers

class CEM(nn.Module):

    def __init__(self, wv_model: object, sigma: float=.3, entropy_dim: Union[int,None]=-1):
        super(CEM, self).__init__()
        self.wv = wv_model
        self.H = H(
            sigma=sigma,
            dim=entropy_dim
        )

    def forward(self, sentence_x, sentence_y):
        return self.H(self.wv(sentence_x), self.wv(sentence_y))

    def batch(self, utterances: Union[list, np.ndarray]):
        0