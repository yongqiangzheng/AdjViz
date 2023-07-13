import sys

import benepar, spacy
import numpy as np
from spacy.tokens import Doc

import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib

matplotlib.use('agg')


class WhitespaceTokenizer(object):
    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self, text):
        words = text.split()
        # All tokens 'own' a subsequent space character in this tokenizer
        spaces = [True] * len(words)
        return Doc(self.vocab, words=words, spaces=spaces)


# spaCy + Berkeley
nlp = spacy.load('en_core_web_md')
nlp.tokenizer = WhitespaceTokenizer(nlp.vocab)
nlp.add_pipe("benepar", config={"model": "benepar_en3"})
print('load spacy and benepar !')


def dep_adj(text):
    # https://spacy.io/docs/usage/processing-text
    tokens = nlp(text)
    words = text.split()
    matrix = np.zeros((len(words), len(words))).astype('float32')
    assert len(words) == len(list(tokens))

    for token in tokens:
        matrix[token.i][token.i] = 1
        for child in token.children:
            matrix[token.i][child.i] = 1
            matrix[child.i][token.i] = 1

    return matrix


def cons_adj(text):
    # https://spacy.io/docs/usage/processing-text
    tokens = nlp(text)
    words = text.split()
    matrix = np.zeros((len(words), len(words))).astype('float32')
    assert len(words) == len(list(tokens))

    for sent in list(tokens.sents):
        for cons in sent._.constituents:
            print(cons)
            if len(cons) == 1:
                continue
            matrix[cons.start:cons.end, cons.start:cons.end] += np.ones([len(cons), len(cons)])

    # max_edge = np.amax(matrix, axis=1, keepdims=True)
    # matrix = matrix / max_edge

    # sum_edge_ = np.sum(matrix, axis=1, keepdims=True)
    # matrix = matrix / (sum_edge_+1e-12)

    return matrix


def generate_fig(text):
    dep_matrix = dep_adj(text)
    cons_matrix = cons_adj(text)
    dep_cons_matrix = dep_matrix + cons_matrix
    # sum_edge_ = np.sum(dep_cons_matrix, axis=1, keepdims=True)
    # dep_cons_matrix = dep_cons_matrix / sum_edge_

    ticks = text.split()

    # DepGCN
    plt.figure(figsize=(16, 16))
    sns.heatmap(dep_matrix, cmap="cool", linewidths=.5, xticklabels=ticks, yticklabels=ticks, annot=True, square=True,
                cbar_kws={"ticks": list(range(0, 21))})
    plt.title("depGCN")
    plt.xticks(rotation=60)
    plt.yticks(rotation=0)
    plt.savefig('static/depgcn.png')
    plt.close()

    # ConsGCN
    plt.figure(figsize=(16, 16))
    sns.heatmap(cons_matrix, cmap="cool", linewidths=.5, xticklabels=ticks, yticklabels=ticks, annot=True, square=True,
                cbar_kws={"ticks": list(range(0, 21))})
    plt.title("consGCN")
    plt.xticks(rotation=60)
    plt.yticks(rotation=0)
    plt.savefig('static/consgcn.png')
    plt.close()

    # DepConsGCN
    plt.figure(figsize=(16, 16))
    sns.heatmap(dep_cons_matrix, cmap="cool", linewidths=.5, xticklabels=ticks, yticklabels=ticks, annot=True,
                square=True, cbar_kws={"ticks": list(range(0, 21))})
    plt.title("depconsGCN")
    plt.xticks(rotation=60)
    plt.yticks(rotation=0)
    plt.savefig('static/depconsgcn.png')
    plt.close()


if __name__ == '__main__':
    cons_adj("I charge it at night and skip taking the cord with me because of the good battery life .")
