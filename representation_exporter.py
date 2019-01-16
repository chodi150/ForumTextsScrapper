import argparse
import datetime
from facades import export_representation_facade
from properties.default_values import glove_window_size, glove_vector_dimension

parser = argparse.ArgumentParser(description="Help of export module")
parser.add_argument('-forum', help='Forum link - necessary to start scraping', required=True)
parser.add_argument('-day', help='Day', required=True)
parser.add_argument('-month', help='month', required=True)
parser.add_argument('-year', help='year', required=True)
parser.add_argument('-filename', help='year', required=True)
parser.add_argument('-mode', help='glove or tfidf', required=True)
parser.add_argument('-glove_window', help='Size of context window in GloVe, default value: 100', required=False)
parser.add_argument('-glove_vec_dim', help='Used vector dimension in GloVe', required=False)

args = parser.parse_args()
filter_date = datetime.datetime(int(args.year), int(args.month), int(args.day))
forum_id = int(args.forum)
mode = args.mode
filename =  args.filename

current_date = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M")
filename = filename + current_date + ".csv"

if mode == "glove":
    filename = "window_size_" + str(glove_window_size) + "_vec_dim_" + str(glove_vector_dimension) + "_" + filename
    filename = "glove_" + filename
    export_representation_facade.do_glove(forum_id, filter_date, filename, window_size =glove_window_size, vec_dim=glove_vector_dimension)
elif mode == "tfidf":
    filename = "tfidf_" + filename
    export_representation_facade.do_tfidf(forum_id, filter_date, filename)
elif mode == "prepare":
    filename = "prepare_" + filename
    export_representation_facade.prepare(forum_id, filter_date, filename)