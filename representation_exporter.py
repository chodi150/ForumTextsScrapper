import argparse
import datetime
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
filename = "output" if args.filename is None else args.filename

current_date = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M")
filename = filename + current_date + ".csv"

window_size = 5
vec_dim = 100

if mode == "glove":
    filename = "window_size_" + str(window_size) + "_vec_dim_" + str(vec_dim) + "_" + filename
    filename = "glove_" + filename
    export_representation_facade.do_glove(forum_id, filter_date, filename, window_size = window_size, vec_dim=vec_dim)
elif mode == "tfidf":
    filename = "tfidf_" + filename
    export_representation_facade.do_tfidf(forum_id, filter_date, filename)
elif mode == "prepare":
    filename = "prepare_" + filename
    export_representation_facade.prepare(forum_id, filter_date, filename)