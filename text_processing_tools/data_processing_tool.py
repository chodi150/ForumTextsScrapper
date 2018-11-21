from text_processing_tools import polish_month_parser
import dateutil.parser as dparser
import bs4
import logging

helper = polish_month_parser.PolishMonthHelper()

def substitute_polish_month(expression):
    for abb in helper.all_months_abbreviations:
        if abb in expression:
            expression = expression.replace(abb, helper.get_month(abb))
    return expression


def parse_date(contents):
    without_tags = list(filter(lambda x: type(x) is bs4.element.NavigableString, contents))
    without_tags = list(map(lambda x: str(x), without_tags))
    for expression in without_tags:
        expression = substitute_polish_month(expression)
        try:
            date = dparser.parse(expression, fuzzy=True, dayfirst=True)
            return date
        except:
            logging.error("No date in:" + expression)