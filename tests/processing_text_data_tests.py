from unittest import TestCase
from text_processing_tools import data_processing_tool as dpt


class TestTextProcessingTools(TestCase):

    def test_given_string_with_polish_month_when_substituting_then_proper_returned(self):
        strin_with_date = "15 kwiecień 1996"
        res = dpt.substitute_polish_month(strin_with_date)
        self.assertEquals("15 4 1996", res)

    def test_given_string_with_polish_month_when_substituting_then_proper_returned(self):
        strin_with_date = "1996 kwiecien 15"
        res = dpt.substitute_polish_month(strin_with_date)
        self.assertEquals("1996 4 15", res)

    def test_given_string_with_polish_month_when_substituting_then_proper_returned(self):
        strin_with_date = "1 sie 2000"
        res = dpt.substitute_polish_month(strin_with_date)
        self.assertEquals("1 8 2000", res)