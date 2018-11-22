# -*- coding: utf-8 -*-
import scrapy
import logging
from predictors.categories_predictor import *
from util import rule_provider as rp, html_util
from config import mapping as m
import pony.orm as pny
from entities import Forum
from text_processing_tools import post_processing_tool as ppt
from text_processing_tools import data_processing_tool as dpt
from repositories import Repository
from scrap_strategies import scraping_strategy_builder


class CategoriesSpider(scrapy.Spider):
    name = 'categories'
    categories_predictor = CategoriesPredictor()
    repository = Repository.Repository()
    logging.basicConfig(filename='logs.txt', level=logging.DEBUG)

    def __init__(self, start_url, scrap_mode, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [start_url]
        self.base_domain = start_url
        self.scrap_mode = scrap_mode
        self.rule_provider = rp.RuleProvider()
        self.rule_provider.prepare_model()
        self.mappings = self.rule_provider.mapper.mappings
        self.scraping_strategy = scraping_strategy_builder.get_strategy(scrap_mode)
        with pny.db_session:
            self.forum = Forum.Forum(link=self.base_domain)

    def parse(self, response):
        soup = BeautifulSoup(response.body, features="lxml")
        parent = response.meta.get('parent')
        for tag in self.rule_provider.possible_tags:
            elements_with_tag = soup.body.findAll(tag)
            for html_element in elements_with_tag:
                if html_util.element_has_css_class(html_element):
                    predicted = self.rule_provider.predict(tag, html_element["class"])

                    if predicted == self.mappings[m.category_whole] or predicted == self.mappings[m.category_title]:
                        yield from self.parse_categories(html_element, predicted, tag, parent)
                    if predicted == self.mappings[m.topic_whole]:
                        yield from self.parse_topics(html_element, parent)
                    if predicted == self.mappings[m.next_page] or predicted == self.mappings[m.next_page_link]:
                        yield from self.go_to_next_page(html_element, parent, predicted)
                    if predicted == self.mappings[m.post_whole]:
                        self.parse_posts(html_element, parent)



    def parse_categories(self, html_element, predicted, tag, parent):
        category = None
        if predicted == self.mappings[m.category_title]:
            category = self.repository.save_category(html_element, parent, self.forum)
            logging.info(html_element.contents[0] + " " + self.base_domain + html_element['href'])

        if predicted == self.mappings[m.category_whole]:
            a_html_element = html_element.findAll("a")
            category = self.repository.save_category(a_html_element[0], parent, self.forum)
            logging.info(str(a_html_element[0].contents[0]) + " " + self.base_domain + a_html_element[0]['href'])

        if category is not None and html_util.url_not_from_other_domain(category.link):
            yield scrapy.Request(url=self.base_domain + category.link, callback=self.parse, meta={'parent': category})


    def parse_topics(self, html_element, parent):
        author = None
        date = None
        for tag in self.rule_provider.possible_tags:
            elements_inside_tag = html_element.findAll(tag)
            for elem in elements_inside_tag:
                if html_util.element_has_css_class(elem):
                    predicted = self.rule_provider.predict(tag, elem["class"])
                    if predicted == self.mappings[m.topic_title]:
                        logging.info("Parsed topic: " + elem.contents[0] + elem['href'])
                        title = elem.contents[0]
                        link = elem['href']
                    if predicted == self.mappings[m.topic_author]:
                        author = elem.contents[0]
                    if predicted == self.mappings[m.topic_date]:
                        date = dpt.parse_date(elem.contents)

        topic = self.repository.save_topic(author, date, link, parent, title)
        yield scrapy.Request(dont_filter=True, url=self.base_domain + topic.link, callback=self.parse,
                             meta={'parent': topic})

    def parse_posts(self, html_element, parent):
        logging.info("Parsing post of topic: " + parent.title)
        author = None
        date = None
        for tag in self.rule_provider.possible_tags:
            elements_with_tag = html_element.findAll(tag)
            for elem in elements_with_tag:
                if html_util.element_has_css_class(elem):
                    predicted = self.rule_provider.predict(tag, elem["class"])
                    if predicted == self.mappings[m.post_body]:
                        content = ppt.contents_to_plain_text(elem.contents)
                    if predicted == self.mappings[m.topic_author]:
                        author = elem.contents[0]
                    if predicted == self.mappings[m.post_date]:
                        date = dpt.parse_date(elem.contents)
        self.repository.save_post(author, content, date, parent)

    def go_to_next_page(self, html_element, parent, predicted):
        if predicted == predicted == self.mappings[m.next_page]:
            a_html_element = html_element.findAll("a")
            logging.info("Going to next page: " + parent.title + " unwrapped url: " + a_html_element[0]['href'])
            yield scrapy.Request(url=self.base_domain + a_html_element[0]['href'], callback=self.parse,
                                 meta={'parent': parent})
        elif predicted == self.mappings[m.next_page_link]:
            logging.info("Going to next page: " + parent.title + " url: " + html_element['href'])
            yield scrapy.Request(url=self.base_domain + html_element['href'], callback=self.parse,
                                 meta={'parent': parent})