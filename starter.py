import sys, getopt
from scrapy import cmdline
import datetime
from scrapy.crawler import CrawlerProcess
import argparse
from properties.scrap_modes import *
import forum_spider

parser = argparse.ArgumentParser()
parser.add_argument('-forum', help='Forum link - necessary to start scraping', required=True)
parser.add_argument('-mode', help='Mode of scraping: full, only_categories, chosen_categories')
args = parser.parse_args()
mode = args.mode

if mode != full_scraping and mode != only_categories and mode != chosen_categories:
    print("Not found such mode. Available are following modes: full, only_categories, chosen_categories")
    exit(1)


def start_scraping(start_url, scrap_mode):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(forum_spider.CategoriesSpider, start_url, scrap_mode)
    process.start()


start_scraping(args.forum, mode)
