import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class Scraper:
    def __init__(self, names):
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'menu_scrapers.menu_scrapers.settings'
        self.process = CrawlerProcess(settings=get_project_settings())
        self.spiders = [*names]


    def run_spiders(self):
        if len(self.spiders):
            for spider in self.spiders:
                self.process.crawl(spider)
            self.process.start()


