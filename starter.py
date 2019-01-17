from scrapy.crawler import CrawlerProcess
import argparse
from properties.scrap_modes import *
import forum_spider
from urllib.parse import urlparse

def start_scraping(start_url, scrap_mode):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(forum_spider.CategoriesSpider, start_url, scrap_mode)
    process.start()


parser = argparse.ArgumentParser()
parser.add_argument('-f','--forum', help='Forum link - necessary to start scraping', required=True)
parser.add_argument('-m', '--mode', help='Mode of scraping: full, only_categories, chosen_categories', required=True)
args = parser.parse_args()
mode = args.mode

if mode != full_scraping and mode != only_categories and mode != chosen_categories:
    print("Not found such mode. Available are following modes: full, only_categories, chosen_categories")
    exit(1)

forum_link = args.forum



start_scraping(forum_link, mode)
