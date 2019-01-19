import pandas as pd
from glove import Corpus, Glove
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

from text_processing_tools.preprocessing import build_post_repr
from vector_representations.preprocessing import preprocess_texts_from_given_forum


def transform_to_glove(date_from, date_to, filename, forum_id, max_df, min_df, vec_dim, window_size):
    data_frame = preprocess_texts_from_given_forum(forum_id, date_from, date_to, "prepare_" + filename)
    vectorizer = build_dictionary_for_glove(data_frame, max_df, min_df)
    data_frame.post = data_frame.post.apply(lambda x: x.split(" "))
    glove = build_glove_word_vectors(data_frame, vec_dim, vectorizer, window_size)
    pd.DataFrame(glove.word_vectors).to_csv("word_vectors" + filename, sep=';')
    representations = build_document_representations(data_frame, glove)
    size_of_dictionary = len(vectorizer.get_feature_names())
    return representations, size_of_dictionary


def build_glove_word_vectors(data_frame, vec_dim, vectorizer, window_size):
    corpus = Corpus(vectorizer.vocabulary_)
    corpus.fit(data_frame.post, window=window_size, ignore_missing=True)
    glove = Glove(no_components=vec_dim, learning_rate=0.01)
    glove.fit(corpus.matrix, epochs=1, no_threads=4, verbose=True)
    glove.add_dictionary(corpus.dictionary)
    return glove


def build_dictionary_for_glove(data_frame, max_df, min_df):
    data_frame.post = data_frame.post.apply(lambda x: " ".join(x))
    stops = set(stopwords.words('polish'))
    vectorizer = TfidfVectorizer(stop_words=stops, min_df=min_df, max_df=max_df, use_idf=False)
    vectorizer.fit(data_frame.post)
    return vectorizer


def build_document_representations(data_frame, glove):
    representations = pd.DataFrame()
    for post in data_frame.post:
        representations = representations.append(build_post_repr(post, glove))
    representations['belongs_to'] = data_frame.category.values
    representations = representations[representations['delete'] == False]
    representations = representations.drop('delete', axis=1)
    return representations