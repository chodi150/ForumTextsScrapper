from config import filtering_config
from filtering.filtering import *
from unittest import TestCase
from datetime import datetime


class TestTextProcessingTools(TestCase):

    def test_all_properties_none_when_given_post_then_meets_criterions(self):
        filtering_config.posts_date_to = None
        filtering_config.posts_date_from = None
        filtering_config.post_keywords = None
        filtering_config.post_authors = None

        res = post_meets_criterions("Mein Auto ist leider kaputt", "Friderik", datetime(2000, 1, 1))

        self.assertTrue(res)

    def test_all_properties_none_when_given_topic_then_meets_criterions(self):
        filtering_config.topics_date_to = None
        filtering_config.topics_date_from = None
        filtering_config.topic_keywords = None
        filtering_config.topic_authors = None

        res = topic_meets_criterions("Mein Auto ist leider kaputt", "Friderik", datetime(2000, 1, 1))

        self.assertTrue(res)

    def test_given_date_scope_when_topic_within_then_meets_criterion(self):
        filtering_config.topics_date_to = datetime(2005, 1, 1)
        filtering_config.topics_date_from = datetime(2003, 1, 1)
        filtering_config.topic_keywords = None
        filtering_config.topic_authors = None

        res = topic_meets_criterions("Mein Auto ist leider kaputt", "Friderik", datetime(2004, 10, 1))

        self.assertTrue(res)

    def test_given_date_scope_when_topic_before_then_doesnt_meet_criterion(self):
        filtering_config.topics_date_to = datetime(2005, 1, 1)
        filtering_config.topics_date_from = datetime(2003, 1, 1)
        filtering_config.topic_keywords = None
        filtering_config.topic_authors = None

        res = topic_meets_criterions("Mein Auto ist leider kaputt", "Friderik", datetime(2002, 10, 1))

        self.assertFalse(res)

    def test_given_date_scope_when_topic_after_then_doesnt_meet_criterion(self):
        filtering_config.topics_date_to = datetime(2005, 1, 1)
        filtering_config.topics_date_from = datetime(2003, 1, 1)
        filtering_config.topic_keywords = None
        filtering_config.topic_authors = None

        res = topic_meets_criterions("Mein Auto ist leider kaputt", "Friderik", datetime(2007, 10, 1))

        self.assertFalse(res)

    def test_given_date_in_scope_but_author_not_when_topic_checked_then_doesnt_meet_criterion(self):
        filtering_config.topics_date_to = datetime(2009, 1, 1)
        filtering_config.topics_date_from = datetime(2000, 1, 1)
        filtering_config.topic_keywords = None
        filtering_config.topic_authors = ["Johannes", "Moritz"]

        res = topic_meets_criterions("Mein Auto ist leider kaputt", "Friderik", datetime(2004, 10, 1))

        self.assertFalse(res)

    def test_given_date_in_scope_and_author_in_list_when_topic_checked_then_doesnt_meet_criterion(self):
        filtering_config.topics_date_to = datetime(2009, 1, 1)
        filtering_config.topics_date_from = datetime(2000, 1, 1)
        filtering_config.topic_keywords = None
        filtering_config.topic_authors = ["Johannes", "Moritz", "Friderik"]

        res = topic_meets_criterions("Mein Auto ist leider kaputt", "Friderik", datetime(2004, 10, 1))

        self.assertTrue(res)

    def test_given_date_in_scope_and_author_but_keywords_differ_when_topic_checked_then_doesnt_meet_criterion(self):
        filtering_config.topics_date_to = datetime(2009, 1, 1)
        filtering_config.topics_date_from = datetime(2000, 1, 1)
        filtering_config.topic_keywords = ["Drogen", "Unfall"]
        filtering_config.topic_authors = ["Johannes", "Moritz", "Friderik"]

        res = topic_meets_criterions("Mein Auto ist leider kaputt", "Friderik", datetime(2004, 10, 1))

        self.assertFalse(res)

    def test_given_date_in_scope_and_author_and_keywords_when_topic_checked_then_doesnt_meet_criterion(self):
        filtering_config.topics_date_to = datetime(2009, 1, 1)
        filtering_config.topics_date_from = datetime(2000, 1, 1)
        filtering_config.topic_keywords = ["Drogen", "Unfall", "kaputt"]
        filtering_config.topic_authors = ["Johannes", "Moritz", "Friderik"]

        res = topic_meets_criterions("Mein Auto ist leider kaputt", "Friderik", datetime(2004, 10, 1))

        self.assertTrue(res)

    def test_given_date_scope_when_post_within_then_meets_criterion(self):
        filtering_config.posts_date_to = datetime(2005, 1, 1)
        filtering_config.posts_date_from = datetime(2003, 1, 1)
        filtering_config.post_keywords = None
        filtering_config.post_authors = None

        res = post_meets_criterions("Mein Auto ist leider kaputt", "Friderik", datetime(2004, 10, 1))

        self.assertTrue(res)

    def test_given_date_scope_when_post_before_then_doesnt_meet_criterion(self):
        filtering_config.posts_date_to = datetime(2005, 1, 1)
        filtering_config.posts_date_from = datetime(2003, 1, 1)
        filtering_config.post_keywords = None
        filtering_config.post_authors = None

        res = post_meets_criterions("Mein Auto ist leider kaputt", "Friderik", datetime(2002, 10, 1))

        self.assertFalse(res)

    def test_given_date_scope_when_post_after_then_doesnt_meet_criterion(self):
        filtering_config.posts_date_to = datetime(2005, 1, 1)
        filtering_config.posts_date_from = datetime(2003, 1, 1)
        filtering_config.post_keywords = None
        filtering_config.post_authors = None

        res = post_meets_criterions("Mein Auto ist leider kaputt", "Friderik", datetime(2007, 10, 1))

        self.assertFalse(res)

    def test_given_date_in_scope_but_author_not_when_post_checked_then_doesnt_meet_criterion(self):
        filtering_config.posts_date_to = datetime(2009, 1, 1)
        filtering_config.posts_date_from = datetime(2000, 1, 1)
        filtering_config.post_keywords = None
        filtering_config.post_authors = ["Johannes", "Moritz"]

        res = post_meets_criterions("Mein Auto ist leider kaputt", "Friderik", datetime(2004, 10, 1))

        self.assertFalse(res)

    def test_given_date_in_scope_and_author_in_list_when_post_checked_then_meet_criterion(self):
        filtering_config.posts_date_to = datetime(2009, 1, 1)
        filtering_config.posts_date_from = datetime(2000, 1, 1)
        filtering_config.post_keywords = None
        filtering_config.post_authors = ["Johannes", "Moritz", "Friderik"]

        res = post_meets_criterions("Mein Auto ist leider kaputt", "Friderik", datetime(2004, 10, 1))

        self.assertTrue(res)

    def test_given_date_in_scope_and_author_but_keywords_differ_when_post_checked_then_doesnt_meet_criterion(self):
        filtering_config.posts_date_to = datetime(2009, 1, 1)
        filtering_config.posts_date_from = datetime(2000, 1, 1)
        filtering_config.post_keywords = ["Drogen", "Unfall"]
        filtering_config.post_authors = ["Johannes", "Moritz", "Friderik"]

        res = post_meets_criterions("Mein Auto ist leider kaputt", "Friderik", datetime(2004, 10, 1))

        self.assertFalse(res)

    def test_given_date_in_scope_and_author_and_keywords_when_post_checked_then_meet_criterion(self):
        filtering_config.posts_date_to = datetime(2009, 1, 1)
        filtering_config.posts_date_from = datetime(2000, 1, 1)
        filtering_config.post_keywords = ["Drogen", "Unfall", "kaputt"]
        filtering_config.post_authors = ["Johannes", "Moritz", "Friderik"]

        res = post_meets_criterions("Mein Auto ist leider kaputt", "Friderik", datetime(2004, 10, 1))

        self.assertTrue(res)

    def test_given_proper_author_and_keywords_but_date_wrong_when_post_checked_then_doesnt_meet_criterion(self):
        filtering_config.posts_date_to = datetime(2009, 1, 1)
        filtering_config.posts_date_from = datetime(2000, 1, 1)
        filtering_config.post_keywords = ["Drogen", "Unfall", "kaputt"]
        filtering_config.post_authors = ["Johannes", "Moritz", "Friderik"]

        res = post_meets_criterions("Mein Auto ist leider kaputt", "Friderik", datetime(2012, 10, 1))

        self.assertFalse(res)


    def test_given_proper_author_and_keywords_but_topic_author_unknown_when_post_checked_then_not_meet_criterion(self):
        filtering_config.posts_date_to = datetime(2009, 1, 1)
        filtering_config.posts_date_from = datetime(2000, 1, 1)
        filtering_config.post_keywords = ["Drogen", "Unfall", "kaputt"]
        filtering_config.post_authors = ["Johannes", "Moritz", "Friderik"]

        res = post_meets_criterions("Mein Auto ist leider kaputt", None, datetime(2005, 10, 1))

        self.assertFalse(res)


    def test_given_proper_author_and_keywords_but_date_unknown_when_post_checked_then_not_meet_criterion(self):
        filtering_config.posts_date_to = datetime(2009, 1, 1)
        filtering_config.posts_date_from = datetime(2000, 1, 1)
        filtering_config.post_keywords = ["Drogen", "Unfall", "kaputt"]
        filtering_config.post_authors = ["Johannes", "Moritz", "Friderik"]

        res = post_meets_criterions("Mein Auto ist leider kaputt", "Friderik", None)

        self.assertFalse(res)

    def test_only_from_date_specified_when_post_written_after_checked_then_meet_criterion(self):
        filtering_config.posts_date_to = None
        filtering_config.posts_date_from = datetime(2004, 1, 1)
        filtering_config.post_keywords = ["Drogen", "Unfall", "kaputt"]
        filtering_config.post_authors = ["Johannes", "Moritz", "Friderik"]

        res = post_meets_criterions("Mein Auto ist leider kaputt", "Friderik", datetime(2005, 10, 1))

        self.assertTrue(res)

    def test_given_different_new_and_old_values_when_testing_then_new_returned(self):
        old = "Unfall"
        new = "Drogen"
        res = assign_new_value_if_changed_and_not_null(old, new)
        self.assertEqual(res, new)

    def test_given_same_new_and_old_values_when_testing_then_old_returned(self):
        old = "Unfall"
        new = "Unfall"
        res = assign_new_value_if_changed_and_not_null(old, new)
        self.assertEqual(res, old)

    def test_given_differen_new_and_old_values_new_is_empty_when_testing_then_new_returned(self):
        old = "Unfall"
        new = ""
        res = assign_new_value_if_changed_and_not_null(old, new)
        self.assertEqual(res, old)