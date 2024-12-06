# Entropy-conVergence Metric

The following is a full implementation of the convergence-entropy measurement framework (here referred to as Entropy-conVergence Metric, or EVM) as described in Rosen and Dale 2023. We've taken strides to make this package as easy to implement as possible.

At its core there are two things that researchers need to define for the most basic version of the EVM algorithm. Those are:

1. A word vector model (we suggest those implemented in the HuggingFace transformer library)
2. An entropy object

Demonstrating how this would look in code:

```python
from convergence_entropy.CEM import CEM, languageModelLayers
from transformers import AutoTokenizer, AutoModel

wv = languageModelLayers('roberta-base', layers=[7])

mod = CEM(
    wv_model = wv
)

mod('No action can be taken without first consulting the voters', 'it is the prerogative of politicians alone to make decisions'), \
mod('No action can be taken without first consulting the voters', 'ultimately the people have to have the right to decide what we do next')
```

The above returns the entropy for the first sentence upon having read the second sentence, consistent with the equations and formulation listed in Rosen and Dale 2023.

# End-to-End data exploration using Convergence-Entropy 
The Convergence Entropy Data Analysis package (CEDA) is an end-to-end shell designed to facilitate GPU assisted, fast analyses. Implementationally, it is quite simple.

```python
from convergence_entropy.CEDA import ceda_model

GRAPH = ceda_model(
    sigma=1.,
    device='cuda',
    wv_model='roberta-base',
    wv_layers=[7]
)
```

Where `wv_model` is parameter for the string name of any model available from the HuggingFace library of language models, and `wv_layers` selects which hidden layers to attenuate to from the language model when producing a representation of lexical units.

On run-time, one can pass to the model a list of strings for both utterances $x$ and $y$ (see Rosen & Dale 2023 for terminology).

```python
x_sentences = ['a list of', 'sentences']
y_sentences = ['another list', 'of more sentences']

GRAPH.fit(x_sentences, y_sentences)
GRAPH.add_meta_data(
    meta_data = [
        {'a': 1, 'b': 2}, # a records oriented json object for metadata for each comparison in the graph.
                          #   Not required.
    ]
)
```

If there are repeated sentences in `x_sentence` or `y_sentences` it is worthwhile to sort the lists so as to cluster repetitions. This is because the model is designed to optimize for repeated examples by only generating vector representations for an utterance once in either the $x$ or $y$ variable so long as that element is repeated. Thus if you have a list of comparisons

```python
x_sentences = ['Sentence A', 'Sentence A', 'Sentence B']
y_sentences = ['sentence c', 'sentence d', 'sentence e']
```

`ceda_model` will generate vectors for 'Sentence A' once, until it reaches 'Sentence B' in `x_sentences`.

This creates a graph that can be used for any number of convergence-entropy based analyses, complete with metadata.

Finally, one can save a checkpoint for the graph using the checkpoint function

```python
CKPT_PATH = 'path/to/checkpoint.pt'
GRAPH.checkpoint(CKPT_PATH)
```

Saving a graph using the `.checkpoint()` has the added benefit, too, of allowing you to load a CEDA graph object from that checkpoint later.

```python
CKPT_PATH = 'path/to/checkpoint.pt'
GRAPH.load_from_checkpoint(CKPT_PATH)
```

You can also create a dataframe for the graph to be saved as a .csv or other format.

```python
CKPT_PATH = 'path/to/checkpoint.csv'
df = GRAPH.graph_df()
df.to_csv(CKPT_PATH, index=False, encoding='utf-8')
```

A number of built-in visualization tools are included as well in the `EDA` package. We will expand on that documentation at a later date.

# Citation for usage

Any use of this package should cite it using the following:

```
@article{rosen_dale_berts_2023,
	title = {{BERTs} of a feather: {Studying} inter- and intra-group communication via information theory and language models},
	shorttitle = {{BERTs} of a feather},
	url = {https://link.springer.com/10.3758/s13428-023-02267-2},
	doi = {10.3758/s13428-023-02267-2},
	journal = {Behavior Research Methods},
	author = {Rosen, Zachary P and Dale, Rick},
	year = {2023},
}
```

If you're interested in the most up-to-date version of this package or are interested in contributing to it, you can find
[the github repository for it here](https://github.com/zaqari/EVM).
