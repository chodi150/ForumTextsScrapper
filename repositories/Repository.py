from entities import Forum
import logging
import pony.orm as pny

logging.basicConfig(filename='logs.txt', level=logging.DEBUG)


class Repository:

    def save_category(self, title,link, parent, forum):
        try:
            with pny.db_session:
                return Forum.Category(title=title, link=link,
                                      forum=forum.forum_id,
                                      parent_category=None if parent is None else parent.category_id)
        except KeyError as e:
            logging.error(str(e))
            logging.error("For element: " + str(title))

    def save_topic(self, author, date, link, parent, title):
        try:
            with pny.db_session:
                return Forum.Topic(title=title, link=link,
                                   author='' if author is None else author,
                                   date=date,
                                   category=parent.category_id)
        except BaseException as e:
            logging.error(str(e))
            logging.error("Title: " + title + " link: " + link + " author: " + author)

    def save_post(self, author, content, date, parent):
        try:
            with pny.db_session:
                Forum.Post(content=content, topic=parent.topic_id,
                           author='' if author is None else author,
                           date=date)
        except BaseException as e:
            logging.error("Save post: " + str(e))
            logging.error("Content: " + content + " author: " + author)
