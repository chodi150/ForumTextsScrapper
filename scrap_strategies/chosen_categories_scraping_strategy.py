import scrapy

from scrap_strategies.scraping_strategy import ScrapingStrategy
from repositories import Repository as r
import pandas as pd
from config import mapping as m


class ChosenCategoriesScrapingStrategy(ScrapingStrategy):

    def __init__(self):
        self.repository = r.Repository()
        self.strategy_initialized = False
        self.forum = None

    def init_strategy(self, forum_link):
        self.forum = self.repository.find_forum(forum_link)
        return self.forum

    def execute_strategy(self, html_element, parent, predicted, tag, mappings, spider):
        if not self.strategy_initialized:
            yield from self.prepare_strategy(spider)
        else:
            if predicted == mappings[m.topic_whole]:
                yield from spider.parse_topics(html_element, parent)
            if predicted == mappings[m.next_page] or predicted == mappings[m.next_page_link]:
                yield from spider.go_to_next_page(html_element, parent, predicted)
            if predicted == mappings[m.post_whole]:
                spider.parse_posts(html_element, parent)

    def prepare_strategy(self, spider):
        config_file = pd.read_csv("config/categories.csv", sep=';')
        category_ids = set(config_file['category_id'])
        categories = self.repository.get_categories(category_ids)
        base_link = self.repository.get_forum_of_category(categories[0]).link

        for category in categories:
            yield scrapy.Request(dont_filter=True, url=base_link + category.link, callback=spider.parse,
                                 meta={'parent': category})


