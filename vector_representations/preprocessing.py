import re

import hunspell
import nltk
import pandas as pd
from nltk.corpus import stopwords

from repositories import Repository
from text_processing_tools.preprocessing import correct_writing


def preprocess_texts_from_given_forum(forum_id, date_from, date_to, filename):
    data_frame = get_texts_and_prepare_data_frame(date_from, date_to, forum_id)
    data_frame = delete_undesired_elements_from_texts(data_frame)
    tokens = data_frame.post.apply(lambda x: nltk.word_tokenize(x))
    hun = hunspell.Hunspell('pl')
    counter = [0]
    tokens_stemmed = tokens.apply(lambda x: correct_writing(hun, x, counter))
    tokens_stemmed = delete_stop_words(tokens_stemmed)
    data_frame.post = tokens_stemmed
    data_frame.to_csv(filename, sep=';', escapechar='\\') #addidional save after preparing preprocessing
    return data_frame


def get_texts_and_prepare_data_frame(date_from, date_to, forum_id):
    """
    Perform SQL Query to database and turns the result into DataFrame
    """
    repository = Repository.Repository()
    data = repository.get_posts(date_from, date_to, forum_id)
    data_frame = pd.DataFrame(data, columns=['post', 'post_date', 'topic_title', 'category'])
    return data_frame


def delete_stop_words(tokens_stemmed):
    stops = set(stopwords.words('polish'))
    tokens_stemmed = tokens_stemmed.apply(lambda x: [item for item in x if item not in stops])
    return tokens_stemmed


def delete_undesired_elements_from_texts(data_frame):
    data_frame.post = data_frame.post.apply(lambda x: re.sub(' ?(f|ht)tp(s?)://(.*)[0-9][.][a-z]+', '', x)) #delete all links
    data_frame.post = data_frame.post.apply(lambda x: str.lower(x))
    data_frame.post = data_frame.post.apply(lambda x: re.sub(r'[^\w\s]', ' ', x)) # delete all non words and non whitespaces
    data_frame.post = data_frame.post.apply(lambda x: re.sub(r'\d+', ' ', x)) #delete all digits
    return data_frame
