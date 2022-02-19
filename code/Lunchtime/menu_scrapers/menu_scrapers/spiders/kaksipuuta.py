import scrapy
from random import choice
from core.custom_headers import CUSTOM_HEADERS as HEADERS
from core.custom_weekdays import get_week_tuple
import re


class KaksipuutaSpider(scrapy.Spider):
    name = 'kaksipuuta'
    allowed_domains = ['www.2puuta.fi']
    start_urls = ['http://www.2puuta.fi/lounas.html']
    map_url = ""
    address = ""

    def start_requests(self):
        url = self.start_urls[0]
        headers = choice(HEADERS)
        yield scrapy.Request(url, headers=headers)

    def parse(self, response):
        week_days = get_week_tuple(1, 5)
        self.address = response.xpath("//div[@class='custom']/p/strong/text()").get()
        menu = response.xpath("//div[@itemprop='articleBody']")
        _main_info = [x.split(" ") for x in menu.xpath("./h3/strong/text()").getall()[2:]]
        price = menu.xpath("./h3/strong/text()").getall()[2].split(" ")[-1]
        all_prices = ("".join(["".join(filter(lambda x: re.match("\d+", x), line)) for line in _main_info +
                        [line.split(" ") for line in menu.xpath("./p/text()").getall()]])).split("€")
        _additional_info = [" ".join(list(line)) for line in _main_info]
        additional_info = ",\n".join([_additional_info.pop(1) + " " + menu.xpath("./h4/text()").getall()[-1]] + \
                    [line.replace("\xa0", "") for line in menu.xpath("./p/text()").getall()[-5:-2]] + _additional_info)
        all_prices = list(map(float, filter(lambda x: len(x), map(lambda x: x.replace(",", "."), all_prices))))
        for index, line in enumerate(menu.xpath("./p/text()").getall()[1:6]):
            scraped_menu = {
                "day": "%s" % week_days[index][1],
                "date": week_days[index][0],
                "dishes": line,
                "price": f"around {price}",
                "additional_price": f"{min(all_prices)}€ - {max(all_prices)}€",
                "additional_info": additional_info
            }
            yield scraped_menu