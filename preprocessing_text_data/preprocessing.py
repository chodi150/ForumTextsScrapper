import pandas as pd
import numpy as np
import logging
from anytree import Node, RenderTree
from collections import Counter


diacrits = dict([("a", "ą"), ("e", "ę"), ("c", "ć"), ("z", "ź"), ("z", "ź"), ("l", "ł"), ("s", "ś"), ("o", "ó")])

logger_dbg = logging.getLogger("dbg")
logger_dbg.setLevel(logging.DEBUG)
fh_dbg_log = logging.FileHandler('correctingwriting.log', mode='w', encoding='utf-8')
fh_dbg_log.setLevel(logging.DEBUG)

# Print time, logger-level and the call's location in a source file.
formatter = logging.Formatter(
    '%(asctime)s-%(levelname)s(%(module)s:%(lineno)d)  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
fh_dbg_log.setFormatter(formatter)

logger_dbg.addHandler(fh_dbg_log)
logger_dbg.propagate = False


def is_correct(word, hun):
    try:
        suggested = hun.suggest(word)
        return word in suggested
    except BaseException as e:
        print(str(e))
        return False


def report_progress(counter):
    counter[0] = counter[0] + 1
    if counter[0] % 100 ==0:
        print("Preprocessed " + str(counter[0]) + " tokens")


def correct_writing(hun, tokens, counter):
    tokens_stemmed = []
    report_progress(counter)
    for i in range(0,len(tokens)):
        if not is_correct(tokens[i], hun):
            try:
                suggested = hun.suggest(tokens[i])
                if len(suggested) != 0:
                    common = set(suggested).intersection(diacritize_fully(tokens[i]))
                    chosen_suggestion = suggested[0] if len(common) == 0 else list(common)[0]
                    if len(common) !=0:
                        logger_dbg.info("Word was: " + tokens[i] + " diacritic check; " + str(common) + " chosen first: " + chosen_suggestion)
                    words =chosen_suggestion.split(' ')
                    for w in words:
                        tokens_stemmed.append(str.lower(hun.stem(w)[0]))
            except BaseException as e:
                print(str(e))
        else:
            tokens_stemmed.append(hun.stem(tokens[i])[0])
    return tokens_stemmed


def build_post_repr(tokens, glove):
    representation = np.zeros(glove.no_components)
    counter = Counter(tokens)
    for tok in tokens:
        if tok in glove.dictionary:
            representation = representation + counter[tok]*glove.word_vectors[glove.dictionary[tok]]

    data_frame =  pd.DataFrame(item for item in representation).transpose()
    data_frame['delete'] = True if np.all(representation == 0) else False
    return data_frame


def diacritize_recursively(parent, i):
    if i >= len(parent.name):
        return
    if parent.name[i] not in diacrits.keys():
        diacritize_recursively(parent, i + 1)
    else:
        word1 = parent.name
        word2 = ""
        for j in range(0, len(parent.name)):
            word2 += parent.name[j] if j != i else diacrits[parent.name[j]]
        n1 = Node(word1, parent = parent)
        n2 = Node(word2, parent = parent)
        diacritize_recursively(n1, i + 1)
        diacritize_recursively(n2, i + 1)


def diacritize_fully(word):
    words = set()
    root = Node(word)
    diacritize_recursively(root, 0)
    for pre, fill, node in RenderTree(root):
        words.add( node.name)
    return words
