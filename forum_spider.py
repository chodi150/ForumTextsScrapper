# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.log import configure_logging
import logging
from database import database_handler
from models import forum_elements as felems, scrap_statistics
from w3lib.html import remove_tags
from predictors.categories_predictor import *
from util import rule_provider as rp
from config import mapping as m
import pony.orm as pny
from entities import Forum
from text_processing_tools import post_processing_tool as ppt
from text_processing_tools import data_processing_tool as dpt
from repositories import Repository


class CategoriesSpider(scrapy.Spider):
    name = 'categories'
    categories_predictor = CategoriesPredictor()
    repository = Repository.Repository()
    logging.basicConfig(filename='logs.txt', level=logging.DEBUG)

    def __init__(self, start_url, scrap_mode, db_name="ScrapDB", **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [start_url]
        self.base_domain = start_url
        self.scrap_mode = scrap_mode
        self.db_handler = database_handler.DatabaseHandler(db_name, start_url)
        self.uniqueId = self.db_handler.get_max_id_from_db()
        self.prop = None
        self.rule_provider = rp.RuleProvider()
        self.rule_provider.prepare_model()
        self.mappings = self.rule_provider.mapper.mappings
        with pny.db_session:
            self.forum = Forum.Forum(link=self.base_domain)

    def parse(self, response):
        soup = BeautifulSoup(response.body, features="lxml")
        parent = response.meta.get('parent')
        for tag in self.rule_provider.possible_tags:
            elements_with_tag = soup.body.findAll(tag)
            for html_element in elements_with_tag:
                if self.element_has_css_class(html_element):
                    predicted = self.rule_provider.predict(tag, html_element["class"])

                    if predicted == self.mappings[m.category_whole] or predicted == self.mappings[m.category_title]:
                        yield from self.parse_categories(html_element, predicted, tag, parent)
                    if predicted == self.mappings[m.topic_whole]:
                        yield from self.parse_topics(html_element, parent)
                    if predicted == self.mappings[m.next_page]:
                        yield from self.go_to_next_page(html_element, parent)
                    if predicted == self.mappings[m.post_whole]:
                        self.parse_posts(html_element, parent)

    def element_has_css_class(self, element):
        return 'class' in element.attrs

    def parse_categories(self, html_element, predicted, tag, parent):
        if self.mappings[m.category_title]:

            category = self.repository.save_category(html_element, parent, self.forum)
            yield scrapy.Request(dont_filter=True, url=self.base_domain + category.link, callback=self.parse,
                                 meta={'parent': category})
            logging.info(html_element.contents[0] + " " + self.base_domain + html_element['href'])
        if predicted == self.mappings[m.category_whole]:
            a_html_element = html_element.findAll("a")
            for a_html_element in a_html_element:
                with pny.db_session:
                    Forum.Category(title=html_element.contents[0], link=html_element['href'], forum=self.forum.forum_id)
                logging.info(a_html_element.contents[0] + " " + self.base_domain + a_html_element['href'])

    def parse_topics(self, html_element, parent):
        author = None
        date = None
        for tag in self.rule_provider.possible_tags:
            elements_inside_tag = html_element.findAll(tag)
            for elem in elements_inside_tag:
                if self.element_has_css_class(elem):
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
                if self.element_has_css_class(elem):
                    predicted = self.rule_provider.predict(tag, elem["class"])
                    if predicted == self.mappings[m.post_body]:
                        content = ppt.contents_to_plain_text(elem.contents)
                    if predicted == self.mappings[m.topic_author]:
                        author = elem.contents[0]
                    if predicted == self.mappings[m.post_date]:
                        date = dpt.parse_date(elem.contents)
        self.repository.save_post(author, content, date, parent)



    def go_to_next_page(self, html_element, parent):
        a_html_element = html_element.findAll("a")
        logging.info("Going to next page: " + parent.title + " url: " + a_html_element[0]['href'])
        yield scrapy.Request(url=self.base_domain + a_html_element[0]['href'], callback=self.parse,
                             meta={'parent': parent})

    def assignId(self):
        self.uniqueId += 1
        return self.uniqueId

    def closed(self, reason):
        pass
        # self.db_handler.save_statistics(self.create_scraping_statictics())
        # if self.scrap_mode == scrap_modes.only_categories:
        #     self.db_handler.write_categories_with_structure()

    def create_scraping_statictics(self):
        num_cats = self.db_handler.find_number_of_elements_with_given_type("category")
        num_subcats = self.db_handler.find_number_of_elements_with_given_type("subcategory")
        num_topics = self.db_handler.find_number_of_elements_with_given_type("topic")
        num_posts = self.db_handler.find_number_of_elements_with_given_type("post")
        stat = scrap_statistics.ScrapStatistics(self.base_domain, num_cats, num_subcats, num_topics, num_posts)
        return stat
