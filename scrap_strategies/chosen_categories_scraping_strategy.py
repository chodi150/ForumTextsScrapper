import scrapy

from scrap_strategies.scraping_strategy import ScrapingStrategy
from repositories import Repository as r
import pandas as pd
from properties import mapping as m
from util.html_util import build_link

class ChosenCategoriesScrapingStrategy(ScrapingStrategy):

    def finish_strategy(self):
        pass

    def __init__(self):
        self.repository = r.Repository()
        self.strategy_initialized = False
        self.forum = None

    def init_strategy(self, forum_link):
        self.forum = self.repository.find_forum(forum_link)
        return self.forum

    def execute_strategy(self, html_element, parent, predicted, tag, mappings, spider):
        """
        Look for all the forum elements apart from categories
        """
        if not self.strategy_initialized:
            yield from self.prepare_strategy(spider)
        else:
            if predicted == mappings.get_mapping(m.topic_whole):
                yield from spider.parse_topics(html_element, parent)
            if predicted == mappings.get_mapping(m.next_page) or predicted == mappings.get_mapping(m.next_page_link):
                yield from spider.go_to_next_page(html_element, parent, predicted)
            if predicted == mappings.get_mapping(m.post_whole):
                spider.parse_posts(html_element, parent)

    def prepare_strategy(self, spider):
        """
        Read all the categories to scrap from config file
        """
        config_file = pd.read_csv("config/categories.csv", sep=';')
        category_ids = set(config_file['category_id'])
        categories = self.repository.get_categories(category_ids)
        base_link = self.forum.link
        self.strategy_initialized = True
        for category in categories:
            yield scrapy.Request(url=build_link(base_link, category.link), callback=spider.parse,
                                 meta={'parent': category})


