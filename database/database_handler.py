from pymongo import MongoClient
from models import forum_elements as felem, scrap_statistics
from . import database_config
import os
import re



class DatabaseHandler:
    client = MongoClient('mongodb://myUserAdmin:abc123@'+database_config.server_ip+':'+str(database_config.port))
    db = client['ScrapDB']
    collection_forum = db['haszysz']
    db_results = client['ResultsScrapDB']
    collection_results = db['haszysz']

    def __init__(self, db_name, collection_name):
        self.client = MongoClient('mongodb://myUserAdmin:abc123@'+database_config.server_ip+':'+str(database_config.port))
        self.db = self.client[db_name]
        self.db_results = self.client[db_name + "_statistics"]
        self.collection_forum = self.db[collection_name]
        self.collection_results = self.db_results["statistics"]

    def insert_topic_to_db(self, topic, parent):
        self.collection_forum.insert(
            {"_id": topic.id,
             "content": topic.content,
             "link": topic.link,
             "type": "topic",
             "author": topic.author,
             "date": topic.date,
             "number_of_posts": topic.number_of_posts,
             "children": [],
             "parent": parent.id
             })
        self.collection_forum.update({"_id": parent.id},
                                     {"$addToSet": {"topics": topic.id}})

    def insert_category_to_db(self, forum_element):
        self.collection_forum.insert(
            {"_id": forum_element.id,
             "content": forum_element.content,
             "link": forum_element.link,
             "type": "category",
             "subcategories": [],
             "topics": []
             })

    def insert_subcategory_to_db(self, forum_element, parent):
        self.collection_forum.insert(
            {"_id": forum_element.id,
             "content": forum_element.content,
             "link": forum_element.link,
             "type": "subcategory",
             "subcategories": [],
             "topics": [],
             "parent": parent.id
             })
        self.collection_forum.update({"_id": parent.id}, {"$addToSet": {"subcategories": forum_element.id}})

    def insert_post_to_db(self, post, parent):
        self.collection_forum.insert(
            {"_id": post.id,
             "content": post.content,
             "type": "post",
             "author": post.author,
             "date": post.date,
             "parent": parent.id,
             })
        self.collection_forum.update({"_id": parent.id},
                                     {"$addToSet": {"children": post.id}})

    def get_max_id_from_db(self):
        try:
            return self.collection_forum.find().sort("_id", -1)[0]['_id']
        except:
            return 0

    # section selecting
    def select_all_categories(self):
        cats = []
        categories = self.collection_forum.find({"type": "category"})
        for cat in categories:
            cats.append(
                felem.ForumElement(cat['_id'], cat['content'], cat['link'], cat['subcategories'], cat['topics']))
        return cats

    def select_one_category(self, name):
        category = self.collection_forum.find_one({"content": name})
        if category == None:
            raise Exception("Couldn't find specified category")
        return category

    def select_categories_by_ids(self, categories_ids):
        categories = []
        for id in categories_ids:
            cat = self.collection_forum.find({"_id": id})[0]
            categories.append(felem.ForumElement(cat['_id'], cat['content'], cat['link']))
        return categories

    def get_subcategory_by_id(self, id):
        cat = self.collection_forum.find({"_id": id})[0]
        return felem.ForumElement(cat['_id'], cat['content'], cat['link'], cat['subcategories'], cat['topics'])

    def get_topic_by_id(self, id):
        topic = self.collection_forum.find({"_id": id})[0]
        topic_object = felem.Topic(topic["_id"], topic["content"], topic["link"], topic["date"], topic["author"],
                                   topic["number_of_posts"])
        return topic_object

    # exploring
    def write_categories_with_structure(self):
        file = open("config/categories.db", 'w', encoding='utf-8')
        categories = self.collection_forum.find({"type": "category"})
        for cat in categories:
            file.write(cat['content'] + "id==" + str(cat['_id']) + "\n")
            self.write_structure_of_category(cat, file, "\t")

    def write_structure_of_category(self, category, file, tabs):
        for child_id in category['subcategories']:
            child_cat = self.collection_forum.find({"_id": child_id})[0]
            file.write(tabs + child_cat['content'] + " | id==" + str(child_cat['_id']) + "\n")
            self.write_structure_of_category(child_cat, file, tabs + "\t")

    def get_all_posts_of_topic(self, topic):
        posts = [ self.collection_forum.find_one({"_id": id}) for id in topic["children"]]
        return posts


    def get_max_id_in_db(self):
        return self.db.collection_forum.find().sort("_id", -1).limit(1)

    def save_statistics(self, statistics: scrap_statistics.ScrapStatistics):
        self.collection_results.update(
            {"_id": statistics.link},
            {"number_of_categories": statistics.number_of_categories,
             "number_of_subcategories": statistics.number_of_subcategories,
             "number_of_topics": statistics.number_of_topics,
             "number_of_posts": statistics.number_of_posts,
             }, upsert=True)

    def find_number_of_elements_with_given_type(self, type):
        return self.collection_forum.find({"type": type}).count()
