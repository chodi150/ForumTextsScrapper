from scrap_strategies.scraping_strategy import ScrapingStrategy
from properties import mapping as m
from repositories import Repository as r


class FullScrapingStrategy(ScrapingStrategy):

    def __init__(self):
        self.repository = r.Repository()
        self.forum = None

    def finish_strategy(self):
        pass

    def init_strategy(self, link):
        self.forum = self.repository.save_forum(link)
        return self.forum

    def execute_strategy(self, html_element, parent, predicted, tag, mappings, spider):
        if predicted in (mappings.get_mapping(m.category_whole), mappings.get_mapping(m.category_title)):
            yield from spider.parse_categories(html_element, predicted, parent)
        if predicted == mappings.get_mapping(m.topic_whole):
            yield from spider.parse_topics(html_element, parent)
        if predicted in (mappings.get_mapping(m.next_page), predicted == mappings.get_mapping(m.next_page_link)):
            yield from spider.go_to_next_page(html_element, parent, predicted)
        if predicted == mappings.get_mapping(m.post_whole):
            spider.parse_posts(html_element, parent)

