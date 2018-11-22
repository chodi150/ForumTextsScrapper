from abc import abstractmethod


class ScrapingStrategy:
    @abstractmethod
    def execute_strategy(self): raise NotImplementedError