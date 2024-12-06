import torch.nn as nn
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig


class classifier(nn.Module):

    def __init__(self, model='Hate-speech-CNERG/dehatebert-mono-english', special_tokens=True, device='cpu', layers=[7,-1], max_sequence_length=500, clip_at=400, pre_sequence_stride=100):
        super(classifier, self).__init__()
        self.dev = device                   # whether running on 'cuda' or 'cpu' or some other device

        # BERT Model components
        self.config = AutoConfig.from_pretrained(model, output_hidden_states=True)
        self.tokenizer = AutoTokenizer.from_pretrained("Hate-speech-CNERG/dehatebert-mono-english")
        self.mod = AutoModelForSequenceClassification.from_pretrained(model, config=self.config).to(self.dev)

        # Vector manipulations
        self.layers = layers                # which hidden layers to attenuate to
        self.flat = nn.Flatten(-2,-1)       # protocol for flattening attenuated hidden layers


        # Sequence manipulations
        self.max_steps = 5                  # the maximum number of steps for overflow tokens to take
        self.sptoks = special_tokens        # whether or not to return special tokens
        self.max_seq = max_sequence_length  # maximum unclipped sequence length
        self.stride = pre_sequence_stride   # how many tokens to include prior to sequence
        self.clip = clip_at                 # window length in tokens (excluding pre_sequence_stride)
        self.clip_cls = True                # whether to omit CLS tokens from output.

    def _tokenize(self, text):
        ids = self.tokenizer.encode(text, add_special_tokens=self.sptoks)
        tokens = np.array(self.tokenizer.convert_ids_to_tokens(ids))
        return ids, tokens

    def _vectorize(self, ids):

        res = self.mod(torch.LongTensor(ids).unsqueeze(0).to(self.dev))

        # logits, outputs = res.logits, res.hidden_states
        # print(logits, outputs)
        outputs = torch.cat(res.hidden_states,dim=0)[self.layers].transpose(0, 1)

        return res.logits, self.flat(outputs)

    def E(self, ids):

        if len(ids) <= self.max_seq:
            logits, outputs = self._vectorize(ids)

        else:

            nSpans = int(len(ids) / self.clip)
            start = [i * self.clip for i in range(nSpans)] + [nSpans * self.clip]
            fins = [(i + 1) * self.clip for i in range(nSpans)] + [len(ids)]
            steps = list(zip(start, fins))

            logits, outputs = self._vectorize(ids[steps[0][0]:steps[0][1]])

            for step in steps[1:self.max_steps]:
                logits_, y_i = self._vectorize(ids[step[0]-self.stride:step[1]])
                outputs = torch.cat([outputs, y_i[self.stride:]], dim=0)
                logits = torch.cat([logits, logits_], dim=0)

        return logits, outputs

    def forward(self, text, prompt=None, level=None):

        if level != None:
            self.layers = level

        ids, tokens = self._tokenize(text)
        delta = None

        if prompt != None:
            _ids,_tokens = self._tokenize(prompt)

            if self.sptoks:
                _ids, _tokens = _ids[:-1],_tokens[:-1]
                ids,tokens = ids[1:],tokens[1:]

            ids, tokens = _ids+ids, np.concatenate([_tokens, tokens])
            delta = len(_ids)

        logits, Ex = self.E(ids)

        if self.clip_cls and self.sptoks:

            if (delta != None) and (delta > 0):
                delta -= 1

            Ex, tokens = Ex[1:-1], tokens[1:-1]

        return logits, Ex, tokens, delta


