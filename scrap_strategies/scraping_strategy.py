from abc import abstractmethod


class ScrapingStrategy:
    @abstractmethod
    def execute_strategy(self, html_element, parent, predicted, tag, mappings, spider): raise NotImplementedError

    @abstractmethod
    def finish_strategy(self): raise NotImplementedError

    @abstractmethod
    def init_strategy(self, link): raise NotImplementedError
