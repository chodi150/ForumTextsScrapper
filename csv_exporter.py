import argparse
import datetime
import dateutil.parser as dparser
from entities import Entities
import pony.orm as pny
import pandas as pd
from util import sql_queries
from facades import export_facade


parser = argparse.ArgumentParser()
parser.add_argument('-forum', help='Forum link - necessary to start scraping', required=True)
parser.add_argument('-day', help='Day', required=True)
parser.add_argument('-month', help='month', required=True)
parser.add_argument('-year', help='year', required=True)
parser.add_argument('-filename', help='year', required=False)
args = parser.parse_args()
filter_date = datetime.datetime(int(args.year), int(args.month), int(args.day))
forum_id = int(args.forum)
filename = "output.csv" if args.filename is None else args.filename


export_facade.export_posts(forum_id, filter_date, filename)


