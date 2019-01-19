import re

import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

from vector_representations.preprocessing import preprocess_texts_from_given_forum


def transform_to_tfidf(date_from, date_to, filename, forum_id, max_df, min_df):
    data_frame = preprocess_texts_from_given_forum(forum_id, date_from, date_to, "prepare_" + filename)
    data_frame = preprocess_for_tfidf(data_frame)
    tfidf, vectorizer = prepare_tfidf(data_frame, max_df, min_df)
    tfidf = drop_null_values(tfidf)
    size_of_dictionary = len(vectorizer.get_feature_names())
    return size_of_dictionary, tfidf


def preprocess_for_tfidf(data_frame):
    data_frame.post = data_frame.post.apply(lambda x: " ".join(x))
    data_frame.post = data_frame.post.apply(lambda x: re.sub(r'[^\w\s]', '', x))
    return data_frame


def prepare_tfidf(data_frame, max_df, min_df):
    stops = set(stopwords.words('polish'))
    vectorizer = TfidfVectorizer(stop_words=stops, min_df=min_df, max_df=max_df)
    vectorizer.fit(data_frame.post)
    tfidf = pd.DataFrame(vectorizer.transform(data_frame.post).toarray(), columns=vectorizer.get_feature_names())
    tfidf['category'] = data_frame.category
    return tfidf, vectorizer


def drop_null_values(tfidf):
    only_nulls = list(map(lambda x: np.all(x[0:len(x) - 1] == 0), tfidf.values))
    tfidf['only_nulls'] = np.array(only_nulls)
    tfidf = tfidf[tfidf['only_nulls'] == False]
    tfidf = tfidf.drop('only_nulls', axis=1)
    return tfidf