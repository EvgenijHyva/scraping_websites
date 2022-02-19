import os
import sys
import django

PROJECT_PATH = os.path.dirname(os.path.abspath("manage.py"))
sys.path.append(PROJECT_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Lunchtime.Lunchtime.settings")
django.setup()

from multiprocessing import Process
from celery import shared_task
from menu_scrapers.crawl_runner import Scraper


def run_scrapy_spiders():
    existing_spiders = ["obelix", "kaksipuuta", ]
    menu = Scraper(existing_spiders)
    menu.run_spiders()


@shared_task
def run_scrapy_task():
    proc = Process(target=run_scrapy_spiders)
    proc.start()
    proc.join()
    return "Spider process from menu_scrapers task"


if __name__ == "__main__":
    run_scrapy_task()

#docker-compose up --build