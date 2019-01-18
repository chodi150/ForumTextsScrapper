import pandas as pd
import numpy as np
import logging
from anytree import Node, RenderTree
from collections import Counter
from util import logging_util

diacrits = dict([("a", "ą"), ("e", "ę"), ("c", "ć"), ("z", "ź"), ("z", "ź"), ("l", "ł"), ("s", "ś"), ("o", "ó")])

logger_dbg = logging_util.get_logger("logs/correcting")


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

        n1 = Node(word1, parent=parent)
        n2 = Node(word2, parent=parent)
        diacritize_recursively(n1, i + 1)
        diacritize_recursively(n2, i + 1)
        n3 = execute_special_action_if_z_available(parent, i)
        if n3 is not None:
            diacritize_recursively(n3, i + 1)


def execute_special_action_if_z_available(parent, i):
    word3=""
    for j in range(0, len(parent.name)):
        word3 += parent.name[j] if j != i else get_diacrits_wrapped(parent.name[j])
    return Node(word3, parent=parent)


def get_diacrits_wrapped(letter):
    return diacrits[letter] if letter != "z" else "ż"


def diacritize_fully(word):
    """
    str -> set(str)

    Return sets of all possiblities of replacing letters with diacrit signs
    """
    words = set()
    root = Node(word)
    diacritize_recursively(root, 0)
    for pre, fill, node in RenderTree(root):
        words.add( node.name)
    return words
