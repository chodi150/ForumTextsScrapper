from scrap_strategies.scraping_strategy import ScrapingStrategy
from config import mapping as m


class CategoriesScrapingStrategy(ScrapingStrategy):
    def execute_strategy(self, html_element, parent, predicted, tag, mappings):
        if predicted == mappings[m.category_whole] or predicted == mappings[m.category_title]:
            yield from self.parse_categories(html_element, predicted, tag, parent)
