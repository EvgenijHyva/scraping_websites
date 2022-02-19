import scrapy
from scrapy_selenium import SeleniumRequest
from random import choice
from core.custom_headers import CUSTOM_HEADERS as HEADERS
from core.custom_weekdays import get_week_tuple


class BaseCampSpider(scrapy.Spider):

    """Note that, this scrapper require a chromedriver and chrome browser for scraping JavaScript websites"""

    name = 'base_camp'
    start_urls = ['https://www.base-camp.fi/lunchmenu.php']
    map_url = ""
    address = ""


    def start_requests(self):
        headers = choice(HEADERS)
        yield SeleniumRequest(
            url='https://www.base-camp.fi/lunchmenu.php', wait_time=3, callback=self.parse,
            screenshot=True, headers=headers
        )

    def parse(self, response):
        week_days = get_week_tuple(1, 5)
        week_menu = response.xpath("//ul/div[@class='row']/div/li/a/div/div")
        day_counter = 0
        scraped_menu = {}
        dishes = []
        for line in week_menu:
            article = line.xpath("./h4/text()").get()
            price = line.xpath("./div/b/span/text()").get() + "€"
            dishes.append({"article": article, "price": price})
            try:
                num = int(article[1:2])
            except ValueError:
                print("not a number")
                break
            if num == 8 and day_counter < len(week_days):
                scraped_menu.update({week_days[day_counter][1]: dishes})
                dishes = []
                day_counter += 1
        yield scraped_menu
