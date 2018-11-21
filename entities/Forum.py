from pony.orm import *
import datetime

db = Database()
db.bind(provider='postgres', user='postgres', password='postgres', host='localhost', database='scrap_db')

class Forum(db.Entity):
    forum_id = PrimaryKey(int, auto=True)
    link = Required(str)
    categories = Set('Category')


class Category(db.Entity):
    category_id = PrimaryKey(int, auto=True)
    link = Required(str)
    title = Required(str)
    parent_category = Optional('Category')
    subcategories = Set('Category')
    forum = Required(Forum)
    topics = Set('Topic')


class Topic(db.Entity):
    topic_id = PrimaryKey(int, auto=True)
    title = Required(str)
    date = Optional(datetime.datetime)
    author = Optional(str)
    link = Required(str)
    topics = Set('Post')
    category = Required(Category)


class Post(db.Entity):
    post_id = PrimaryKey(int, auto=True)
    content = Required(str)
    date = Optional(datetime.datetime)
    author = Optional(str)
    topic = Required(Topic)


db.generate_mapping(create_tables=True)