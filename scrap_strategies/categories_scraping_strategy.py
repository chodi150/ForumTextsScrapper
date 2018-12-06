from scrap_strategies.scraping_strategy import ScrapingStrategy
from properties import mapping as m
from repositories import Repository as r
import pandas as pd


class CategoriesScrapingStrategy(ScrapingStrategy):

    def __init__(self):
        self.repository = r.Repository()
        self.forum = None

    def init_strategy(self, link):
        self.forum = self.repository.save_forum(link)
        return self.forum

    def execute_strategy(self, html_element, parent, predicted, tag, mappings, spider):
        if predicted in (mappings[m.category_whole], mappings[m.category_title]):
            yield from spider.parse_categories(html_element, predicted, parent)

    def finish_strategy(self):
        repository = r.Repository()
        all_categories = repository.get_all_categories(self.forum)
        categories_data_frame = pd.DataFrame.from_records([category.to_dict() for category in all_categories])
        categories_data_frame.to_csv("config/categories.csv", sep=";")
