import argparse
import os
from datetime import datetime
from urllib.parse import urlparse
import re
from entities import Entities
import pony.orm as pny
import dateutil.parser as dparser


def find_forum( forum_id, filter_date):
    with pny.db_session:
        forum = Entities.Forum[forum_id]
        base_directory = "../output/"+urlparse(forum.link)[1]
        if not os.path.isdir(base_directory):
            os.makedirs(base_directory)
        for category in filter(lambda p: p.parent_category is None, forum.categories):
            path = base_directory + "/" + re.sub('[^\w\-_\. ]', '_', category.title)
            if not os.path.isdir(path):
                os.makedirs(path)
                write_posts(category, path, filter_date)
            for subcat in category.subcategories:
                sub_path = path + "/" + re.sub('[^\w\-_\. ]', '_', subcat.title)
                if not os.path.isdir(sub_path):
                    os.makedirs(sub_path)
                    write_posts(subcat, sub_path, filter_date)

def write_posts(category, path, filter_date):
    i = 0
    print("Exporting category: " + category.title+ "..." + " Number of topics: " + str(len(category.topics)))
    for topic in category.topics:
        if(topic.date< filter_date):
            continue
        for post in topic.topics:
            file = open(path + "/" + str(i), 'w', encoding='utf-8')
            file.write(post.content)
            file.close()
            i = i +1

parser = argparse.ArgumentParser()
parser.add_argument('-forum', help='Forum link - necessary to start scraping', required=True)
args = parser.parse_args()

filter_date = dparser.parse('2015-01-01 00:00:00.000000')
forum_id = int(args.forum)
find_forum(forum_id, filter_date)


#'2005-09-06 00:00:00.000000