from pony.orm import *
import datetime

db = Database()
db.bind(provider='postgres', user='postgres', password='postgres', host='localhost', database='scrap2')


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

    def __str__(self):
        return "["+str(self.category_id)+"] " + self.title


class Topic(db.Entity):
    topic_id = PrimaryKey(int, auto=True)
    title = Required(str)
    date = Optional(datetime.datetime)
    author = Optional(str)
    link = Required(str)
    topics = Set('Post')
    category = Required(Category)

    def __str__(self):
        return "[" + str(self.topic_id) + "] " + self.title


class Post(db.Entity):
    post_id = PrimaryKey(int, auto=True)
    content = Required(str)
    date = Optional(datetime.datetime)
    author = Optional(str)
    topic = Required(Topic)

    def __str__(self):
        return "[" + str(self.post_id) + "] " + self.content

db.generate_mapping(create_tables=True)