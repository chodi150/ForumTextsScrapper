import argparse
import datetime
import dateutil.parser as dparser
from entities import Forum
import pony.orm as pny
import pandas as pd
from util import sql_queries
from facades import export_representation_facade


parser = argparse.ArgumentParser()
parser.add_argument('-forum', help='Forum link - necessary to start scraping', required=True)
parser.add_argument('-day', help='Day', required=True)
parser.add_argument('-month', help='month', required=True)
parser.add_argument('-year', help='year', required=True)
parser.add_argument('-filename', help='year', required=False)
parser.add_argument('-mode', help='glove or tfidf', required=True)

args = parser.parse_args()
filter_date = datetime.datetime(int(args.year), int(args.month), int(args.day))
forum_id = int(args.forum)
mode = args.mode
filename = "output.csv" if args.filename is None else args.filename


if mode == "glove":
    export_representation_facade.do_glove(forum_id, filter_date, filename)
elif mode == "tfidf":
    export_representation_facade.do_tfidf(forum_id, filter_date, filename)