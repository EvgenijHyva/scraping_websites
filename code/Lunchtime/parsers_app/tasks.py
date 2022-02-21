import os
import sys
import django
import collections

PROJECT_PATH = os.path.dirname(os.path.abspath("manage.py"))
sys.path.append(PROJECT_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Lunchtime.Lunchtime.settings")
django.setup()

from multiprocessing import Process
from celery import shared_task
from menu_scrapers.crawl_runner import Scraper
from .models import Restaurants

"""Here you can add your new spider names"""
created_spiders = ["obelix", "kaksipuuta", ]

def run_scrapy_spiders():
    _spiders = collections.defaultdict(lambda: True)
    [_spiders[name] for name in created_spiders]
    active_spiders = ((restaurant.name.lower(), restaurant.is_active) for restaurant in Restaurants.objects.all())
    _spiders.update(active_spiders)
    all_spiders = list(filter(lambda name: _spiders[name] == True, _spiders))
    menu = Scraper(all_spiders)
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