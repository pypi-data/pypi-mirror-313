import torch
import numpy as np
import torch.nn as nn

class entropy(nn.Module):
    
    def __init__(self, sigma=.8, dim=None):
        super(entropy, self).__init__()
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

    def unsummed(self,ex,ey,dim=None):
        if bool(dim):
            self.dim=dim

        C = self.cos(ex.unsqueeze(1), ey)

        C = self.N.log_prob(C.max(dim=self.dim).values)
        return -(torch.exp(C) * C)

    def on_indexes(self, ex, ey, x_indeces, y_indeces):
        C = self.cos(ex.unsqueeze(1), ey)

        C1, C2 = self.N.log_prob(C.max(dim=-1).values[x_indeces]), self.N.log_prob(C.max(dim=0).values[y_indeces])
        return -(torch.exp(C1) * C1).sum(), -(torch.exp(C2) * C2).sum()

class cudaEntropy(nn.Module):

    def __init__(self, sigma=.5, dim=None, stream_at=100):
        super(cudaEntropy, self).__init__()
        self.sigma = sigma
        self.cos = nn.CosineSimilarity(dim=-1).cuda()

        self.N = torch.distributions.HalfNormal(scale=torch.FloatTensor([sigma]).cuda(), validate_args=False)
        # self.dev = device
        self.dim = dim
        self.stream_at = stream_at
        self.stream_n = 2

    def P(self, x):
        return torch.exp(x) / (self.sigma)

    def H(self, x):
        x_ = (1 - x)/(self.sigma**2)
        return self.H_ * x_

    def streamCOS_one_sided(self, ex, ey):

        spans = int(len(ex) / self.stream_n)

        starts = [i * self.stream_n for i in range(spans)] + [spans * self.stream_n]
        ends = [(i + 1) * self.stream_n for i in range(spans)] + [len(ex)]
        steps = list(zip(starts, ends))

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

        steps = [(i * self.stream_n, (i + 1) * self.stream_n) for i in range(spans)]
        if steps[-1][-1] < len(ex):
            steps += [(steps[-1][-1], None)]

        cosMx, cosMy = torch.zeros(size=(1,)).cuda(), torch.zeros(size=(len(ey), 1)).cuda() - 1.

        for start, end in steps:
            cos = self.cos(ex[start:end].unsqueeze(1), ey)

            cosMx = torch.cat([cosMx, cos.max(dim=-1).values.view(-1)], dim=-1)
            cosMy = torch.cat([cos.max(dim=0).values.view(-1, 1), cosMy], dim=-1).max(dim=-1).values.view(-1, 1)

        return cosMx.view(-1)[1:], cosMy.view(-1)

    def one_sided(self, ex, ey, dim=None):
        if bool(dim):
            self.dim = dim

        if len(ex) >= self.stream_at:
            if self.dim == -1:
                C = self.streamCOS_one_sided(ex, ey)
            else:
                C = self.streamCOS_one_sided(ey, ex)

        else:
            C = self.cos(ex.unsqueeze(1), ey).max(dim=self.dim).values

        C = self.N.log_prob(1-C)

        return -(self.P(C) * C).sum()

    def dual_sided(self, ex, ey):

        if (len(ex) >= self.stream_at) or (len(ey) >= self.stream_at):
            C1, C2 = self.streamCOS(ex, ey)

        else:
            C = self.cos(ex.unsqueeze(1), ey)
            C1, C2 = C.max(dim=-1).values, C.max(dim=0).values

        C1, C2 = self.N.log_prob(1-C1), self.N.log_prob(1-C2)
        return -(self.P(C1) * C1).sum(), -(self.P(C2) * C2).sum()

    def forward(self, ex, ey):
        if self.dim:
            return self.one_sided(ex, ey)
        else:
            return self.dual_sided(ex, ey)





    # def forward(self, ex, ey, dim=None):
    #     if bool(dim):
    #         self.dim = dim
    #
    #     if len(ex) >= self.stream_at:
    #         C = self.streamCOS(ex, ey)
    #
    #     else:
    #         C = self.cos(ex.unsqueeze(1), ey).max(dim=self.dim).values
    #
    #     C = self.N.log_prob(1 - C)
    #
    #     return -(torch.exp(C) * C).sum()

    def unsummed(self, ex, ey, dim=None):
        if bool(dim):
            self.dim = dim

        C = self.streamCOS(ex, ey)

        C = self.N.log_prob(1 - C)
        return -(torch.exp(C) * C)

    def on_indexes(self, ex, ey, x_indeces, y_indeces):
        C = self.cos(ex.unsqueeze(1), ey)

        C1, C2 = self.N.log_prob(1 - C.max(dim=-1).values[x_indeces]), self.N.log_prob(1 - C.max(dim=0).values[y_indeces])
        del C
        return -(torch.exp(C1) * C1).sum(), -(torch.exp(C2) * C2).sum()

class entropy_cdf(nn.Module):

    def __init__(self, sigma=1, dim=None, device='cpu'):
        super(entropy_cdf, self).__init__()

        self.sigma = sigma
        # self.dev = device
        self.dim = dim
        self.stream_n = 2

        if device != 'cpu':
            self.cos = nn.CosineSimilarity(dim=-1).cuda()
            self.N = torch.distributions.HalfNormal(scale=torch.FloatTensor([sigma]).cuda(), validate_args=False)

        else:
            self.cos = nn.CosineSimilarity(dim=-1)
            self.N = torch.distributions.HalfNormal(scale=torch.FloatTensor([sigma]), validate_args=False)


    def __stream_cos_one_sided(self, ex, ey):

        spans = int(len(ex) / self.stream_n)

        starts = [i * self.stream_n for i in range(spans)] + [spans * self.stream_n]
        ends = [(i + 1) * self.stream_n for i in range(spans)] + [len(ex)]
        steps = list(zip(starts, ends))

        cosM = self.cos(ex[steps[0][0]:steps[0][1]].unsqueeze(1), ey).max(dim=-1).values.view(-1)
        for start, end in steps[1:]:
            if start != len(ex):
                cosM = torch.cat([
                    cosM,
                    self.cos(ex[start:end].unsqueeze(1), ey).max(dim=-1).values.view(-1)
                ], dim=-1)

        return cosM

    def __stream_cos_two_sided(self, ex, ey):

        spans = int(np.floor(len(ex) / self.stream_n))

        steps = [(i * self.stream_n, (i + 1) * self.stream_n) for i in range(spans)]
        if steps[-1][-1] < len(ex):
            steps += [(steps[-1][-1], None)]

        cosMx, cosMy = torch.zeros(size=(1,)).cuda(), torch.zeros(size=(len(ey), 1)).cuda() - 1.

        for start, end in steps:
            cos = self.cos(ex[start:end].unsqueeze(1), ey)

            cosMx = torch.cat([cosMx, cos.max(dim=-1).values.view(-1)], dim=-1)
            cosMy = torch.cat([cos.max(dim=0).values.view(-1, 1), cosMy], dim=-1).max(dim=-1).values.view(-1, 1)

        return cosMx.view(-1)[1:], cosMy.view(-1)

    def one_sided(self, ex, ey, dim=None):
        if bool(dim):
            self.dim = dim

        try:
            C = self.cos(ex.unsqueeze(1), ey).max(dim=self.dim).values
        except Exception:
            C = self.__stream_cos_one_sided(ex,ey)

        C = 1-self.N.cdf(1 - C)

        return -(torch.log(C) * C).sum()

    def dual_sided(self, ex, ey):
        try:
            C = self.cos(ex.unsqueeze(1), ey)
            C1, C2 = C.max(dim=-1).values, C.max(dim=0).values
        except Exception:
            torch.cuda.empty_cache()
            C1, C2 = self.__stream_cos_two_sided(ex,ey)


        C1, C2 = 1 - self.N.cdf(1 - C1), 1 - self.N.cdf(1 - C2)
        return -(torch.log(C1) * C1).sum(), -(torch.log(C2) * C2).sum()

    def forward(self, ex, ey):
        if self.dim:
            return self.one_sided(ex, ey)
        else:
            return self.dual_sided(ex, ey)

class cudaEntropy_cdf(nn.Module):

    def __init__(self, sigma=1, dim=None, stream_at=100):
        super(cudaEntropy_cdf, self).__init__()
        self.sigma = sigma
        self.cos = nn.CosineSimilarity(dim=-1).cuda()

        self.N = torch.distributions.HalfNormal(scale=torch.FloatTensor([sigma]).cuda(), validate_args=False)
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

        cosMx, cosMy = torch.zeros(size=(1,)).cuda(), torch.zeros(size=(len(ey),1)).cuda()-1.

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


#################################################################################

class DKL(nn.Module):

    def __init__(self, sigma=.3, dim=None):
        super(DKL, self).__init__()
        self.cos = nn.CosineSimilarity(dim=-1)
        self.N = torch.distributions.Normal(1, scale=sigma, validate_args=False)
        self.N0 = self.N.log_prob(torch.FloatTensor([0.]))      # distribution for a term in its original context
        self.dim = dim

    def forward(self, ex, ey, dim=None):
        if bool(dim):
            self.dim = dim

        # Get cosine similarity comparison between lexical items
        C = self.cos(ex.unsqueeze(1), ey)

        if self.dim != None:
            # along a single dimension,
            # (1) Get max cosine similarity
            # (2) Get log prob of similarity
            # (3) Calculate log prob and entropy
            C = self.N.log_prob(1 - C.max(dim=self.dim).values)
            return (torch.exp(C) * (C - self.N0)).sum()

        else:
            C1, C2 = self.N.log_prob(1 - C.max(dim=-1).values), self.N.log_prob(1 - C.max(dim=0).values)
            C = None
            return -(torch.exp(C1) * C1).sum(), -(torch.exp(C2) * C2).sum()

    def unsummed(self, ex, ey, dim=None):
        if bool(dim):
            self.dim = dim

        C = self.cos(ex.unsqueeze(1), ey)

        C = self.N.log_prob(C.max(dim=self.dim).values)
        return -(torch.exp(C) * C)

    def on_indexes(self, ex, ey, x_indeces, y_indeces):
        C = self.cos(ex.unsqueeze(1), ey)

        C1, C2 = self.N.log_prob(C.max(dim=-1).values[x_indeces]), self.N.log_prob(C.max(dim=0).values[y_indeces])
        return -(torch.exp(C1) * C1).sum(), -(torch.exp(C2) * C2).sum()

class analytic_entropy(nn.Module):

    def __init__(self, sigma=.3, dim=None):
        super(analytic_entropy, self).__init__()
        self.cos = nn.CosineSimilarity(dim=-1)
        self.sigma = sigma
        self.H_ = (.5 * np.log(2*np.pi*(sigma**2))) + .5
        self.dim = dim

    def H(self, x):
        x_ = (1 - x)/(self.sigma)
        return self.H_ * x_


    def forward(self, ex, ey, dim=None):
        if bool(dim):
            self.dim = dim

        # Get cosine similarity comparison between lexical items
        C = self.cos(ex.unsqueeze(1), ey)

        if self.dim != None:
            # along a single dimension,
            # (1) Get max cosine similarity
            # (2) Get log prob of similarity
            # (3) Calculate log prob and entropy
            C = C.max(dim=self.dim).values
            C = self.H(C)
            return C.sum()

        else:
            C1, C2 = self.H(C.max(dim=-1).values), self.H(C.max(dim=0).values)
            C = None
            return C1.sum(), C2.sum()

    def unsummed(self, ex, ey, dim=None):
        if bool(dim):
            self.dim = dim

        C = self.cos(ex.unsqueeze(1), ey)

        C = self.N.log_prob(C.max(dim=self.dim).values)
        return -(torch.exp(C) * C)

    def on_indexes(self, ex, ey, x_indeces, y_indeces):
        C = self.cos(ex.unsqueeze(1), ey)

        C1, C2 = self.N.log_prob(C.max(dim=-1).values[x_indeces]), self.N.log_prob(C.max(dim=0).values[y_indeces])
        return -(torch.exp(C1) * C1).sum(), -(torch.exp(C2) * C2).sum()

class I(nn.Module):

    def __init__(self, sigma=.3, dim=None):
        super(I, self).__init__()
        self.cos = nn.CosineSimilarity(dim=-1)
        self.N = torch.distributions.Normal(1, scale=sigma, validate_args=False)
        self.dim = dim

    def forward(self, ex, ey, dim=None):
        if bool(dim):
            self.dim = dim

        # Get cosine similarity comparison between lexical items
        C = self.cos(ex.unsqueeze(1), ey)

        if self.dim != None:
            # along a single dimension,
            # (1) Get max cosine similarity
            # (2) Get log prob of similarity
            # (3) Calculate log prob and entropy
            C = self.N.log_prob(C.max(dim=self.dim).values)
            return C.sum()

        else:
            C1, C2 = self.N.log_prob(C.max(dim=-1).values), self.N.log_prob(C.max(dim=0).values)
            C = None
            return C1.sum(), C2.sum()

    def unsummed(self, ex, ey, dim=None):
        if bool(dim):
            self.dim = dim

        C = self.cos(ex.unsqueeze(1), ey)

        return self.N.log_prob(C.max(dim=self.dim).values)

    def on_indexes(self, ex, ey, x_indeces, y_indeces):
        C = self.cos(ex.unsqueeze(1), ey)

        C1, C2 = self.N.log_prob(C.max(dim=-1).values[x_indeces]), self.N.log_prob(C.max(dim=0).values[y_indeces])
        return C1.sum(), C2.sum()

class cudaI(nn.Module):

    def __init__(self, sigma=.3, dim=None, stream_at=50):
        super(cudaI, self).__init__()
        self.cos = nn.CosineSimilarity(dim=-1).cuda()
        self.N = torch.distributions.HalfNormal(scale=torch.FloatTensor([sigma]).cuda(), validate_args=False)
        # self.dev = device
        self.dim = dim
        self.stream_at = stream_at
        self.stream_n = 2

    def streamCOS__(self, ex, ey):
        cosM = [self.cos(exi, ey).max().view(-1) for exi in ex]
        return torch.cat(cosM,dim=-1)

    def streamCOS(self, ex, ey):

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

    def forward(self, ex, ey, dim=None):
        if bool(dim):
            self.dim = dim

        if len(ex) >= self.stream_at:
            C = self.streamCOS(ex, ey)

        else:
            C = self.cos(ex.unsqueeze(1), ey).max(dim=-1).values

        C = self.N.log_prob(1 - C)

        return (C).sum()

    def unsummed(self, ex, ey, dim=None):
        if bool(dim):
            self.dim = dim

        C = self.streamCOS(ex, ey)

        C = self.N.log_prob(1 - C)
        return (C)

    def on_indexes(self, ex, ey, x_indeces, y_indeces):
        C = self.cos(ex.unsqueeze(1), ey)

        C1, C2 = self.N.log_prob(1 - C.max(dim=-1).values[x_indeces]), self.N.log_prob(1 - C.max(dim=0).values[y_indeces])
        del C
        return (C1).sum(), (C2).sum()