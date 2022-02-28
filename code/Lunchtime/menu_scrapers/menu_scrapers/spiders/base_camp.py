from statistics import median

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
        self.address = response.xpath(u'normalize-space(//li[@class="footer-sprite address"]/a/text())').get()
        self.map_url = response.xpath('//li[@class="footer-sprite address"]/a/@href').get()
        week_menu = response.xpath("//ul/div[@class='row']/div/li/a/div/div")
        days = get_week_tuple(1, 5)
        if week_menu:
            for day_num, day in enumerate(days):
                position_start = day_num * 8  # positions on menu
                position_end = position_start + 8  # every day 8 lines of menu
                # raw data extract data in format (price,dish)
                _raw_data = [(line.xpath("./div/b/span/text()").get(), line.xpath("./h4/text()").get()) for line in
                             week_menu[position_start:position_end]]
                # separate values by [(prices),(dishes)],where prices=0 & dishes=1
                price_dish_unzipped = list(zip(*_raw_data))
                prices = list(map(float, price_dish_unzipped[0]))
                scraped_menu = {
                    "day": "%s" % days[day_num][1],
                    "date": days[day_num][0],
                    "dishes": price_dish_unzipped[1],
                    "price": f"around {median(prices)}€",
                    "additional_price": f"{min(prices)}€ - {max(prices)}€"
                }
                yield scraped_menu
