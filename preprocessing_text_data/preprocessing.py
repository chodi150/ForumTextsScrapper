import pandas as pd
import nltk
import numpy as np
import re
from nltk.corpus import stopwords
import hunspell
from sklearn.feature_extraction.text import TfidfVectorizer
from glove import Corpus, Glove


def is_correct(word, hun):
    suggested = hun.suggest(word)
    if len(suggested)== 0:
        return False
    return suggested[0] == word



def correct_writing(hun, tokens):
    tokens_stemmed = []

    for i in range(0,len(tokens)):
        if not is_correct(tokens[i], hun):
            suggested = hun.suggest(tokens[i])
            if len(suggested) != 0:
                try:
                    chosen_suggestion = suggested[0]
                    words =chosen_suggestion.split(' ')
                    for w in words:
                        tokens_stemmed.append(str.lower(hun.stem(w)[0]))
                except BaseException as e:
                    print(tokens[i] + " stemmed to: " + suggested[0])
        else:
            tokens_stemmed.append(hun.stem(tokens[i])[0])

    return tokens_stemmed

def build_post_repr(tokens, glove):
    representation = np.zeros(glove.no_components)
    for tok in tokens:
        if tok in glove.dictionary:
            representation = representation + glove.word_vectors[glove.dictionary[tok]]

    mean_vect = representation/len(representation)

    return pd.DataFrame(item for item in mean_vect).transpose()