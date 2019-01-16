import datetime

from entities import Entities
import pony.orm as pny
import pandas as pd
from util import sql_queries
from repositories import Repository

def export_posts(forum_id, filterdate, filename):
    repository = Repository.Repository()
    data = repository.get_posts(filterdate, forum_id)
    df = pd.DataFrame(data, columns=['post', 'post_date', 'topic_title', 'category'])
    df.to_csv("output/"+filename, sep=';', escapechar='\\')


