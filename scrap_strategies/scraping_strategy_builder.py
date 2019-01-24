from properties import scrap_modes
from scrap_strategies.categories_scraping_strategy import CategoriesScrapingStrategy
from scrap_strategies.chosen_categories_scraping_strategy import ChosenCategoriesScrapingStrategy
from scrap_strategies.full_scraping_strategy import FullScrapingStrategy
from scrap_strategies.scraping_strategy import ScrapingStrategy


def get_strategy(abbreviation) -> ScrapingStrategy:
    """
        Produce scraping strategy based on abbreviations
    """
    if abbreviation == scrap_modes.chosen_categories:
        return ChosenCategoriesScrapingStrategy()
    elif abbreviation == scrap_modes.full_scraping:
        return FullScrapingStrategy()
    elif abbreviation == scrap_modes.only_categories:
        return CategoriesScrapingStrategy()
