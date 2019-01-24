from config import filtering_config
from filtering.filtering_helpers import date_after_ref, date_before_ref, is_keyword_in_string


def post_meets_criterions(content, author, date):
    return is_post_author_valid(author) and is_post_date_in_range(date) and has_post_keywords(content)


def topic_meets_criterion(content, author, date):
    return is_topic_author_valid(author) and is_topic_date_in_range(date) and has_topic_keywords(content)


def is_topic_author_valid(author):
    return is_author_valid(author, filtering_config.topic_authors)


def is_post_author_valid(author):
    return is_author_valid(author, filtering_config.post_authors)


def is_author_valid(author, ref_authors):
    if ref_authors is None:
        return True
    if author is None:
        return False
    return author in ref_authors


def has_topic_keywords(content):
    return is_keyword_in_string(filtering_config.topic_keywords, content)


def has_post_keywords(content):
    return is_keyword_in_string(filtering_config.post_keywords, content)


def is_post_date_in_range(date):
    if date is None:
        return False
    return date_after_ref(filtering_config.posts_date_from, date) and date_before_ref(filtering_config.posts_date_to,
                                                                                      date)


def is_topic_date_in_range(date):
    return date_after_ref(filtering_config.topics_date_from, date) and date_before_ref(filtering_config.topics_date_to,
                                                                                       date)


def assign_new_value_if_changed_and_not_null(old_value: str, new_value: str):
    if old_value is None or (new_value != old_value and new_value != ""):
        return new_value
    else:
        return old_value
