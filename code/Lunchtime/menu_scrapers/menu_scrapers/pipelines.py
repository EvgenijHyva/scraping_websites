# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
from django.db import IntegrityError
from itemadapter import ItemAdapter
from parsers_app.models import RestaurantMenu, Restaurants, Errors

class MenuScrapersPipeline(object):

    def open_spider(self, spider):
        logging.warning(self)

    def process_item(self, item, spider):
        _restaurant = {
            "name": spider.name.title(),
            "url": spider.start_urls[0],
            "address": spider.address,
            "map_url": spider.map_url
        }
        try:
            restaurant, restaurant_created = Restaurants.objects.get_or_create(**_restaurant)
            #print("pipelines info", restaurant, restaurant_created)
        except IntegrityError as e:
            restaurant = Restaurants.objects.get(name=_restaurant["name"])
            Errors.objects.create(target=restaurant, error_text=e)

        menu, menu_created = RestaurantMenu.objects.get_or_create(restaurant=restaurant, **item)
        logging.info(f"created instance - {menu}")
        return item

    def close_spider(self, spider):
        logging.warning("Items recorded to database by pipeline")

