import scrapy
from random import choice
from core.custom_headers import CUSTOM_HEADERS as HEADERS
from core.custom_weekdays import get_week_tuple
import re
from statistics import median


class ObelixSpider(scrapy.Spider):
    name = 'obelix'
    allowed_domains = ['obelix.fi']
    start_urls = ['https://obelix.fi/hyvinkaa/lounas/']
    map_url = ""
    address = ""

    def start_requests(self):
        url = self.start_urls[0]
        headers = choice(HEADERS)
        yield scrapy.Request(url, headers=headers)

    def parse(self, response):
        print(response.request.headers)
        menu_per_day = response.xpath('//div[@class="fw-text-inner"]')
        week_days = get_week_tuple(1, 5)
        self.address = ",".join([line.strip("\n") for line in
                                response.xpath(".//div[@class='textwidget']/p/text()").getall()[0: 2]])
        for index, day in enumerate(menu_per_day[1:6]):
            scraped_menu = {
                "day": "%s" % week_days[index][1],
                "date": week_days[index][0],
            }
            if day.xpath("./p/text()").get() == "SULJETTU":
                scraped_menu.update(
                    {
                        "info": day.xpath("./p/text()").getall()[0],
                        "additional_info": day.xpath("./p/text()").getall()[1]
                    })
            else:
                lst = [x.replace(u'\xa0', u'') for x in day.xpath("./ul/li/strong/text()").getall() + day.xpath("./p/strong/text()").getall() +
                      day.xpath("./p[@class='Oletus']/b/span/text()").getall() + day.xpath("./p/b/text()").getall() + day.xpath("./ul/li/p/strong/text()").getall()]
                lst = [lst[0] + lst[1]] + lst[2:]
                prices = list(map(float, map(lambda x: x.replace(",", "."), filter(lambda x: len(x),
                                    " ".join(map("".join, (re.findall("\d+,?\d+", x) for x in lst))).split(" ")))))
                scraped_menu.update({
                    "dishes": ",\n".join(lst),
                    "price": "around {:.2f}€".format(median(prices)),
                    "additional_price": "%s€ - %s€" % (min(prices), max(prices))
                })
            yield scraped_menu
