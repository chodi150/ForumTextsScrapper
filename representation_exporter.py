import argparse
import datetime
from datetime import datetime
from facades import export_representation_facade
from properties.default_values import *


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

parser = argparse.ArgumentParser(description="Help of export module")

parser.add_argument('-f', '--forum', help='Id of forum to export', required=True)
parser.add_argument('-m', '--mode', help='Vector representation: glove or tfidf', required=True)
parser.add_argument('-df', '--datefrom',
                    help='Posts written from the date, use format: y-m-d, default value: 1970-1-1',
                    type=valid_date)
parser.add_argument('-dt', '--dateto',
                    help='Posts written from the date, use format: y-m-d, default value: 2020-1-1',
                    type=valid_date)
parser.add_argument('-fn', '--filename', help='Filename for exportedfile, default value: output')

parser.add_argument('-gw', '--glovewindow', help='Size of context window in GloVe, default value: 5', type=int)
parser.add_argument('-gv', '--glovevector', help='Used vector dimension in GloVe, default value: 100', type=int)
parser.add_argument('-mindf', '--mindf',
                    help='Min document frequency when creating dictionary for vector representation, default: 0.0025',
                    type=float)
parser.add_argument('-maxdf', '--maxdf',
                    help='Min document frequency when creating dictionary for vector representation, default: 0.5',
                    required=False, type=float)
args = parser.parse_args()


current_date = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M")
forum_id = int(args.forum)
mode = args.mode
filename = "output" if args.filename is None else args.filename
filename = filename + current_date + ".csv"

date_from = date_from if args.datefrom is None else args.datefrom
date_to = date_to if args.dateto is None else args.dateto
glove_window_size = glove_window_size if args.glovewindow is None else args.glovewindow
glove_vector_dimension = glove_vector_dimension if args.glovevector is None else args.glovevector
max_df = max_df if args.maxdf is None else args.maxdf
min_df = min_df if args.mindf is None else args.mindf



if mode == "glove":
    filename = "window_size_" + str(glove_window_size) + "_vec_dim_" + str(glove_vector_dimension) + "_" + filename
    filename = "glove_" + filename
    export_representation_facade.do_glove(forum_id, date_from, date_to, filename, glove_window_size, glove_vector_dimension, max_df, min_df)
elif mode == "tfidf":
    filename = "tfidf_" + filename
    export_representation_facade.do_tfidf(forum_id, date_from, date_to, filename, max_df, min_df)
elif mode == "prepare":
    filename = "prepare_" + filename
    export_representation_facade.prepare(forum_id, date_from, date_to, filename)
else:
    print("No such mode - choose glove or tfidf")
