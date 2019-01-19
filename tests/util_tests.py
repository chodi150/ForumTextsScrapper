from unittest import TestCase
from util import html_util
from repositories import sql_queries
import datetime
import sqlparse


class TestTextProcessingTools(TestCase):

    def test_given_domain_and_link_when_building_link_proper_build_invision(self):
        domain = 'http://www.uk420.com/boards/'
        link = 'http://www.uk420.com/boards/index.php?/forum/103-outdoor-growing/'

        res = html_util.build_link(domain,link)

        self.assertEqual(res,link)

    def test_given_domain_and_link_when_building_link_proper_build_phpbb(self):
        domain = 'https://forum.vwgolf.pl/'
        link = './viewforum.php?f=157&sid=339596b98a9c27072f8ed07d68be22cd'

        res = html_util.build_link(domain,link)

        self.assertEqual(res,domain+link)

    def test_given_domain_and_link_when_building_link_proper_build_vbulletin(self):
        domain = 'https://www.forum.haszysz.com/'
        link = 'forumdisplay.php?97-Hodowla'

        res = html_util.build_link(domain,link)

        self.assertEqual(res,domain+link)

    def test_given_url_from_same_domain_when_checking_true(self):
        domain = 'http://www.uk420.com/boards/'
        link = 'http://www.uk420.com/boards/index.php?/forum/103-outdoor-growing/'

        res = html_util.url_not_from_other_domain(link, domain)

        self.assertTrue(res)

    def test_given_url_from_other_domain_when_checking_false(self):
        domain = 'https://www.forum.haszysz.com/'
        link = 'https://www.vapefully.com/'

        res = html_util.url_not_from_other_domain(link, domain)

        self.assertFalse(res)

    def test_given_url_from_without_domain_when_checking_true(self):
        domain = 'https://www.forum.haszysz.com/'
        link = 'forumdisplay.php?97-Hodowla'

        res = html_util.build_link(domain, link)

        self.assertTrue(res)

    def test_given_dates_when_getting_sql_query_all_posts_then_query_is_valid_sql(self):
        query = sql_queries.query_all_posts(1, datetime.datetime(2016, 1, 1), datetime.datetime(2018, 1, 1))

        res = sqlparse.parse(query)

        self.assertTrue(res is not None)

    def test_given_valid_url_when_checking_true(self):
        domain = 'https://www.forum.haszysz.com/'

        res = html_util.is_url_valid(domain)

        self.assertTrue(res)

    def test_given_malformed_url_when_checking_false(self):
        domain = 'forum.haszysz.com'

        res = html_util.is_url_valid(domain)

        self.assertFalse(res)