from unittest import TestCase
import hunspell
from text_processing_tools import data_processing_tool as dpt
from text_processing_tools import preprocessing as prp


class TestTextProcessingTools(TestCase):

    def test_given_string_with_polish_month_when_substituting_then_proper_returned(self):
        strin_with_date = "15 kwiecień 1996"
        res = dpt.substitute_polish_month(strin_with_date)
        self.assertEqual("15 4 1996", res)

    def test_given_string_with_polish_month_april_when_substituting_then_proper_returned(self):
        strin_with_date = "1996 kwiecien 15"
        res = dpt.substitute_polish_month(strin_with_date)
        self.assertEqual("1996 4 15", res)

    def test_given_string_with_polish_month__august_when_substituting_then_proper_returned(self):
        strin_with_date = "1 sie 2000"
        res = dpt.substitute_polish_month(strin_with_date)
        self.assertEquals=("1 8 2000", res)

    def test_given_word_without_diacritics_when_diacritizing_then_proper_options_done(self):
        word = "isc"
        res = prp.diacritize_fully(word)
        self.assertEqual(4, len(res))
        self.assertTrue("iść" in res)
        self.assertTrue("isć" in res)
        self.assertTrue("iśc" in res)
        self.assertTrue("isc" in res)

    def test_given_long_word_without_diacritics_when_diacritizing_then_proper_options_done(self):
        word = "poszlyscie"
        res = prp.diacritize_fully(word)
        self.assertTrue("poszłyście" in res)

    def test_given_long_word_with_z_without_diacritics_when_diacritizing_then_proper_options_done(self):
        word = "zrebie"
        res = prp.diacritize_fully(word)
        self.assertTrue("źrebię" in res)

    def test_given_long_word_with_z_without_diacritics2_when_diacritizing_then_proper_options_done(self):
        word = "zebrak"
        res = prp.diacritize_fully(word)
        print(res)
        self.assertTrue("żebrak" in res)


    def test_given_long_word_with_z_without_diacritics3_when_diacritizing_then_proper_options_done(self):
        word = "wiez"
        res = prp.diacritize_fully(word)
        self.assertTrue("więż" in res)

    def test_given_long_word_with_z_without_diacritics4_when_diacritizing_then_proper_options_done(self):
        word = "wieza"
        res = prp.diacritize_fully(word)
        self.assertTrue("wieża" in res)

    def test_given_incorrect_word_when_testing_then_false(self):
        word="karkoweczka"
        res = prp.is_correct(word,  hun = hunspell.Hunspell('pl'))
        self.assertFalse(res)

    def test_given_correct_word_when_testing_then_true(self):
        word="konstytucja"
        res = prp.is_correct(word,  hun = hunspell.Hunspell('pl'))
        self.assertTrue(res)