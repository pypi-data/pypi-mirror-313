import torch
import torch.nn as nn
import numpy as np
import nltk.data
import re

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

def sentences(text):
    sents = sent_detector.tokenize(text)
    sents = [re.sub(r'[^\w\s]',' ', sent) for sent in sents]
    return sents

class analyzer(nn.Module):

    def __init__(self, wv: object, sim_model: object, device: str='cuda'):
        super(analyzer, self).__init__()
        self.dev = device
        self.wv = wv
        self.sim = sim_model
        self.x_text = None
        self.ex = None
        self.y_text = None
        self.ey = None

    def __process_text(self, x):
        texts = sentences(x)
        VECS = []
        for text in texts:
            try:
                w, tokens = self.wv._tokenize(str(text).replace('\n', ' '))
                sel = (
                        (
                                tokens == np.array(
                            ['.', '!', '?', ',', '...', ':', ';', '. . .', '>', 'Ġ']
                        ).reshape(-1,1)
                        ).sum(axis=0) == 0
                )

                w = np.array(w)[sel]

                vecs = self.wv.E(torch.LongTensor(w).view(-1))
                VECS += [vecs]

            except Exception:
                None

        if len(VECS) > 0:
            return torch.cat(VECS, dim=0)
        else:
            return torch.zeros(size=(1, self.wv.mod.embeddings.word_embeddings.weight.shape[-1]*len(self.wv.layers))).float()

    def forward(self, x=None, y=None):

        #The code below may seem strange, but it's quite helpful.
        # In cases where analyzer is used recursively, this snippet
        # of code specifically only creates a new self.ex entry iff
        # it is the case that the text provided in x is different
        # from the prior text given for x.
        if (x != None) and (x != self.x_text):
            self.x_text = x
            self.ex = self.__process_text(x).to(self.dev)

        #And while it is NOT necessary, we repeat the same process
        # for y, just in case.
        if (y != None) and (y != self.y_text):
            self.y_text = y
            self.ey = self.__process_text(y).to(self.dev)

        if self.x_text and self.y_text:
            return self.sim(self.ex, self.ey), (self.ex.shape[0], self.ey.shape[0])

        else:
            return (None, None), (0, 0)

