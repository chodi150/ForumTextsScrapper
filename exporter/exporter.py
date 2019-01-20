import pandas as pd

from config import database_config

from repositories import Repository
from vector_representations.glove_representation import transform_to_glove
from vector_representations.tfidf_representation import transform_to_tfidf


def do_tfidf(forum_id, date_from, date_to, filename, max_df,min_df):
    size_of_dictionary, tfidf = transform_to_tfidf(date_from, date_to, filename, forum_id, max_df, min_df)
    save_tfidf_to_csv(filename, tfidf, size_of_dictionary)


def save_tfidf_to_csv(filename, tfidf, size_of_dictionary):
    filename = "dict_size_" + str(size_of_dictionary) + "_" + filename
    tfidf.to_csv(filename, sep=';', escapechar='\\', encoding='utf-8')


def do_glove(forum_id, date_from,date_to, filename, window_size, vec_dim, max_df,min_df, niter):
    representations, size_of_dictionary = transform_to_glove(date_from, date_to, filename, forum_id, max_df, min_df, vec_dim, window_size, niter)
    save_glove_to_csv(filename, representations, size_of_dictionary)


def save_glove_to_csv(filename, representations, size_of_dictionary):
    filename = "dict_size_" + str(size_of_dictionary) + "_" + filename
    representations.to_csv(filename, sep=';')


def export_posts(forum_id, date_from,date_to, filename):
    repository = Repository.Repository()
    data = repository.get_posts(date_from, date_to, forum_id)
    df = pd.DataFrame(data, columns=['post', 'post_date', 'topic_title', 'category'])
    df.to_csv(filename, sep=';', escapechar='\\')


def show_all_forums():
    print("Forums at DB:" + database_config.HOST)
    print("-------------------------------------")
    print("forum_id | forum_link")
    repository = Repository.Repository()
    forums = repository.get_all_forums()
    for f in forums:
        print(str(f.forum_id) + " | " + f.link)
