import argparse
import os
from urllib.parse import urlparse
import re

from entities import Forum
import logging
import pony.orm as pny



def find_forum( forum_id):
    with pny.db_session:
        forum = Forum.Forum[forum_id]
        base_directory = "../output/"+urlparse(forum.link)[1]
        if not os.path.isdir(base_directory):
            os.makedirs(base_directory)
        for category in filter(lambda p: p.parent_category is None, forum.categories):
            path = base_directory + "/" + re.sub('[^\w\-_\. ]', '_', category.title)
            if not os.path.isdir(path):
                os.makedirs(path)
                write_posts(category, path)
            for subcat in category.subcategories:
                sub_path = path + "/" + re.sub('[^\w\-_\. ]', '_', subcat.title)
                if not os.path.isdir(sub_path):
                    os.makedirs(sub_path)
                    write_posts(subcat, sub_path)

def write_posts(category, path):
    i = 0
    for topic in category.topics:
        for post in topic.topics:
            file = open(path + "/" + str(i), 'w', encoding='utf-8')
            file.write(post.content)
            file.close()
            i = i +1


parser = argparse.ArgumentParser()
parser.add_argument('-forum', help='Forum link - necessary to start scraping', required=True)
args = parser.parse_args()


forum_id = int(args.forum)
find_forum(forum_id)

