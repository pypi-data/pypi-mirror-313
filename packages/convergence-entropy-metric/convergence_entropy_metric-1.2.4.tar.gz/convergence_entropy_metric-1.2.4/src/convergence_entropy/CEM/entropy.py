import torch
import numpy as np
import torch.nn as nn

class entropy_BRM(nn.Module):
    
    def __init__(self, sigma=.8, dim=None):
        super(entropy_BRM, self).__init__()
        self.cos = nn.CosineSimilarity(dim=-1)
        self.N = torch.distributions.Normal(1,scale=sigma, validate_args=False)
        self.dim = dim

    def forward(self, ex, ey):

        # Get cosine similarity comparison between lexical items
        C = self.cos(ex.unsqueeze(1), ey)

        if self.dim != None:
            #along a single dimension,
            # (1) Get max cosine similarity
            # (2) Get log prob of similarity
            # (3) Calculate log prob and entropy
            C = self.N.log_prob(1-C.max(dim=self.dim).values)
            return -(torch.exp(C) * C).sum()

        else:
            C1, C2 = self.N.log_prob(1-C.max(dim=-1).values), self.N.log_prob(1-C.max(dim=0).values)
            C = None
            return -(torch.exp(C1) * C1).sum(), -(torch.exp(C2) * C2).sum()

    def unsummed(self, ex, ey, dim=None):
        if bool(dim):
            self.dim = dim
        else:
            self.dim = -1

        C = self.cos(ex.unsqueeze(1), ey)

        C = self.N.log_prob(1 - C.max(dim=self.dim).values)
        return -(torch.exp(C) * C)

class entropy(nn.Module):

    def __init__(self, sigma=1, dim=None, stream_at=1000, device='cpu'):
        super(entropy, self).__init__()
        self.device = device
        self.sigma = sigma
        self.cos = nn.CosineSimilarity(dim=-1).to(self.device)

        self.N = torch.distributions.HalfNormal(scale=torch.FloatTensor([sigma]).to(self.device), validate_args=False)
        # self.dev = device
        self.dim = dim
        self.stream_at = stream_at
        self.stream_n = 2

    def streamCOS_one_sided(self, ex, ey):

        spans = int(len(ex) / self.stream_n)

        starts = [i * self.stream_n for i in range(spans)] + [spans * self.stream_n]
        ends = [(i+1) * self.stream_n for i in range(spans)] + [len(ex)]
        steps = list(zip(starts,ends))

        cosM = self.cos(ex[steps[0][0]:steps[0][1]].unsqueeze(1), ey).max(dim=-1).values.view(-1)
        for start, end in steps[1:]:
            if start != len(ex):
                cosM = torch.cat([
                    cosM,
                    self.cos(ex[start:end].unsqueeze(1), ey).max(dim=-1).values.view(-1)
                ], dim=-1)

        return cosM

    def streamCOS(self, ex, ey):

        spans = int(np.floor(len(ex) / self.stream_n))

        steps = [(i* self.stream_n, (i+1)*self.stream_n) for i in range(spans)]
        if steps[-1][-1] < len(ex):
            steps += [(steps[-1][-1], None)]

        cosMx, cosMy = torch.zeros(size=(1,)).to(self.device), torch.zeros(size=(len(ey),1)).to(self.device)-1.

        for start, end in steps:
            cos = self.cos(ex[start:end].unsqueeze(1), ey)

            cosMx = torch.cat([cosMx, cos.max(dim=-1).values.view(-1)], dim=-1)
            cosMy = torch.cat([cos.max(dim=0).values.view(-1,1), cosMy], dim=-1).max(dim=-1).values.view(-1,1)

        return cosMx.view(-1)[1:], cosMy.view(-1)

    def one_sided(self, ex, ey, dim=None):
        if bool(dim):
            self.dim = dim

        if (len(ex) >= self.stream_at) or (len(ey) >= self.stream_at):
            if self.dim == -1:
                C = self.streamCOS_one_sided(ex, ey)
            else:
                C = self.streamCOS_one_sided(ey, ex)

        else:
            C = self.cos(ex.unsqueeze(1), ey).max(dim=self.dim).values

        C = 1-self.N.cdf(1 - C)

        return -(torch.log2(C) * C).sum()

    def dual_sided(self, ex, ey):

        if (len(ex) >= self.stream_at) or (len(ey) >= self.stream_at):
            C1, C2 = self.streamCOS(ex, ey)

        else:
            C = self.cos(ex.unsqueeze(1), ey)
            C1, C2 = C.max(dim=-1).values, C.max(dim=0).values

        C1, C2 = 1 - self.N.cdf(1 - C1), 1 - self.N.cdf(1 - C2)
        return -(torch.log2(C1) * C1).sum(), -(torch.log2(C2) * C2).sum()

    def forward(self, ex, ey):
        if self.dim:
            return self.one_sided(ex, ey), None
        else:
            return self.dual_sided(ex, ey)

    def unsummed(self, ex, ey, dim=None):
        if bool(dim):
            self.dim=dim
        else:
            self.dim=-1

        C = self.cos(ex.unsqueeze(1), ey)

        C = 1-self.N.cdf(1-C.max(dim=self.dim).values)
        return -(torch.log2(C) * C)