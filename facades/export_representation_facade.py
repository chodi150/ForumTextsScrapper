import pandas as pd
import nltk
import re


from nltk.corpus import stopwords
import hunspell
from sklearn.feature_extraction.text import TfidfVectorizer
from glove import Corpus, Glove
from preprocessing_text_data.preprocessing import correct_writing, build_post_repr
import itertools
import csv

from repositories import Repository


def swap(word, swap_rule):
    return word.replace(swap_rule[0], swap_rule[1])

def prepare(forum_id, filterdate, filename):
    repository = Repository.Repository()
    data = repository.get_posts(filterdate, forum_id)
    data_frame = pd.DataFrame(data, columns=['post', 'post_date', 'topic_title', 'category'])
    data_frame.post = data_frame.post.apply(lambda x: re.sub(' ?(f|ht)tp(s?)://(.*)[0-9][.][a-z]+', '', x))
    data_frame.post = data_frame.post.apply(lambda x: str.lower(x))
    data_frame.post = data_frame.post.apply(lambda x: re.sub(r'[^\w\s]', ' ', x))
    data_frame.post = data_frame.post.apply(lambda x: re.sub(r'\d+', ' ', x))
    tokens = data_frame.post.apply(lambda x: nltk.word_tokenize(x))
    hun = hunspell.Hunspell('pl')
    counter = [0]
    tokens_stemmed = tokens.apply(lambda x: correct_writing(hun, x, counter))
    stops = set(stopwords.words('polish'))
    tokens_stemmed = tokens_stemmed.apply(lambda x: [item for item in x if item not in stops])
    data_frame.post = tokens_stemmed
    data_frame.to_csv(filename)
    return data_frame


def do_tfidf(forum_id, filterdate, filename):
    data_frame  = pd.read_csv("C:/Users/Piotr/Desktop/Inz/thesisData/thesisData/Tokens_Subaru.csv", sep=',')
    data_frame.post = data_frame.post.apply(lambda x: re.sub(r'[^\w\s]', '', x))
    stops = set(stopwords.words('polish'))
    vectorizer = TfidfVectorizer(stop_words=stops, min_df=10)
    vectorizer.fit(data_frame.post)
    tfidf_transformed = vectorizer.transform(data_frame.post)
    tfidf = pd.SparseDataFrame(tfidf_transformed)
    tfidf.to_csv(filename, sep=';', escapechar='\\')
    # tfidf = pd.DataFrame(, columns=vectorizer.get_feature_names())
    # tfidf['belongs_to'] = data_frame.category
    # tfidf.to_csv(filename, sep=';', escapechar='\\')


def do_glove(forum_id, filterdate, filename):
    # data_frame = prepare(forum_id, filterdate)
    data_frame  = pd.read_csv("C:/Users/Piotr/Desktop/Inz/thesisData/thesisData/Tokens_Subaru.csv", sep=',')
    data_frame.post = data_frame.post.apply(lambda x: re.sub(r'[^\w\s]', '', x))
    data_frame.post = data_frame.post.apply(lambda x: x.split(" "))
    corpus = Corpus()
    corpus.fit(data_frame.post, window=5)
    glove = Glove(no_components=100, learning_rate=0.01)
    glove.fit(corpus.matrix, epochs=300, no_threads=4, verbose=True)
    glove.add_dictionary(corpus.dictionary)
    pd.DataFrame(glove.word_vectors).to_csv("word_Vectors.csv", sep=';')

    representations = pd.DataFrame()
    for post in data_frame.post:
        representations = representations.append(build_post_repr(post, glove))
    representations['belongs_to'] = data_frame.category
    representations.to_csv(filename, sep=';')


