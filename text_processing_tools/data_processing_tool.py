import argparse
import datetime

from text_processing_tools import polish_month_parser
import dateutil.parser as dparser
import bs4
import logging

helper = polish_month_parser.PolishMonthHelper()


def substitute_polish_month(expression):
    matching_abbreviations = []
    for abb in helper.all_months_abbreviations:
        if abb in expression:
            matching_abbreviations.append(abb)
    if len(matching_abbreviations) ==0:
        return expression
    longest_matching = max(matching_abbreviations, key=len)
    expression = expression.replace(longest_matching, helper.get_month(longest_matching))
    return expression


def parse_date(contents):
    without_tags = list(filter(lambda x: type(x) is bs4.element.NavigableString, contents))
    without_tags = list(map(lambda x: str(x), without_tags))
    for expression in without_tags:
        try:
            expression = substitute_polish_month(expression)
            date = dparser.parse(expression, fuzzy=True, dayfirst=True)
            return date
        except BaseException as e:
            pass
    logging.error("[NODATE] Not found date in expression:" + "".join(without_tags))
    return None


def parse_english_date(date):
    date_string = ''.join(date)
    date = dparser.parse(date_string, fuzzy=True)
    return date


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)