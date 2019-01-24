import datetime

# These are default parameters for the exporter
# Can be overwritten by specifying respective values at the input of export_starter.py

glove_window_size = 5
glove_vector_dimension = 100
niter = 100
date_from = datetime.datetime(year=1970, month=1, day=1)
date_to = datetime.datetime(year=2040, month=1, day=1)
min_df = 0.0025
max_df = 0.5
