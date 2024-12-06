import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwords
import ssl
from typing import Union

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')

class TFIDF():
    def __init__(self, df, text_col, topic_col, stop_words=[]):
        super(TFIDF, self).__init__()
        self.df = df.copy()
        self.topic = topic_col
        self.text = text_col
        self.pred_lambda = 1
        self.stop_words = list(stopwords.words())
        self.stop_words += stop_words

        self.df[self.text] = self.df[self.text].str.lower()

        self.tfidf, self.count, self.dft = self.c_tf_idf(self.df)
        # self.topn = self.extract_top_n_words_per_topic(n=topk)

    def c_tf_idf(self, df):
        dft = df.groupby([self.topic], as_index=False).agg({self.text: ' '.join})

        count = CountVectorizer(
            stop_words=self.stop_words
        ).fit(dft[self.text].values)

        t = count.transform(dft[self.text].values).toarray()
        w = t.sum(axis=1)
        tf = np.divide(t.T, w)
        sum_t = (t > 0).astype(float).sum(axis=0)
        idf = np.log(np.divide(len(dft), sum_t + 1)).reshape(-1, 1)
        tf_idf = np.multiply(tf, idf)

        return tf_idf, count, dft

    def pred_batch(self, sentences):
        val = self.count.transform(sentences).toarray()
        res = val @ self.tfidf

        return np.exp(self.pred_lambda * res) / np.exp(self.pred_lambda * res).sum(axis=-1).reshape(-1, 1)

    def pred(self, sentence, k_justifications=5):
        justification_words = self.count.get_feature_names_out()

        val = self.count.transform([sentence]).toarray()
        M = val * self.tfidf.T
        res = M.sum(axis=-1)
        justification = M[res.argmax()].argsort()[-k_justifications:][::-1]
        justification = str([w for w in justification_words[justification] if w.lower() in sentence.lower()])
        normalized_p = np.exp(self.pred_lambda * res) / np.exp(self.pred_lambda * res).sum()

        return self.dft[self.topic].values[res.argmax()], justification, res[res.argmax()], normalized_p[res.argmax()]

    def extract_top_n_words_per_topic(self, n=20):
        words = self.count.get_feature_names_out()
        labels = list(self.dft[self.topic])
        tf_idf_transposed = self.tfidf.T
        indices = tf_idf_transposed.argsort()[:, -n:]
        top_n_words = {label: [(words[j], tf_idf_transposed[i][j]) for j in indices[i]][::-1] for i, label in
                       enumerate(labels)}

        return top_n_words

    def get_topic_names(self):
        names = self.extract_top_n_words_per_topic(n=3)
        return {k: '_'.join([str(k)] + [str(j[0]) for j in v]) for k, v in names.items()}

    def plot_topic_word_frequencies(self, k_words: int=5, n_cols:int=3, specific_topics:list=[], n_topics: Union[int,None]=None, height:int=250, width:int=250, round_to:int=9):
        topics = self.extract_top_n_words_per_topic(n=100)
        topics = {k: [(word, pct) for word, pct in v if word not in self.stop_words][:k_words] for k,v in topics.items()}
        if len(specific_topics) > 0:
            topics = {topic: topics[topic] for topic in specific_topics
                      if topic in topics.keys()}

        if n_topics:
            topics = {k:v for k,v in list(topics.items())[:n_topics]}

        df_ = sum([[[k, vi[0], vi[1]] for vi in values] for k, values in topics.items()], [])
        df_ = [[vi[0], '<PPI>', vi[2]] if vi[1] in self.stop_words else vi for vi in df_]
        df_ = pd.DataFrame(
            np.array(df_),
            columns=['TOPIC', 'lexeme', 'frequency']
        )

        df_['frequency'] = df_['frequency'].astype(float).round(round_to)

        fig = make_subplots(
            rows=int(np.ceil(len(topics) / n_cols)),
            cols=n_cols,
            subplot_titles=df_['TOPIC'].unique(),
        )

        row_n, col_n = 1, 1
        for i, topic in enumerate(df_['TOPIC'].unique()):
            sub_df = df_.loc[df_['TOPIC'].isin([topic])]

            trace = go.Bar(
                y=sub_df['lexeme'],
                x=sub_df['frequency'].astype(float),
                hovertext=sub_df['lexeme'],
                orientation='h',
            )

            fig.add_trace(trace, row=row_n, col=col_n)

            col_n += 1

            if (col_n == 4):
                row_n += 1
                col_n = 1

        fig.update_layout(
            template="plotly_white",
            showlegend=False,
            title={
                'text': "Topic Word Scores",
                'x': .5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(
                    size=22,
                    color="Black")
            },
            width=width * 4,
            height=height * row_n if row_n > 1 else height * 1.3,
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            ),
        )

        return fig