import random

import scrapy
from scrapy import FormRequest


class BlogSpider(scrapy.Spider):
    name = 'wgspider'

    allowed_domains = ["www.wgzimmer.ch"]

    def start_requests(self):
        return [FormRequest("https://www.wgzimmer.ch/wgzimmer/search/mate.html",
                            formdata={
                                'query': '',
                                'priceMin': '700',
                                'priceMax': '1500',
                                'state': 'zurich-stadt',
                                'permanent': 'all',
                                'student': 'none',
                                'country': 'ch',
                                'orderBy': 'MetaData/@mgnl:lastmodified',
                                'orderDir': 'descending',
                                'startSearchMate': 'true',
                                'wgStartSearch': 'true',
                            },
                            callback=self.parse)]

    def parse(self, response):
        links = response.css('div#content ul.list li a::attr(href)').extract()
        cleaned_links = list(filter(lambda a: a != "#", links))
        index = random.randrange(0, len(cleaned_links)-1)
        for clean_link in cleaned_links[index:index+1]:
            yield scrapy.Request(response.urljoin(clean_link), callback=self.parse_room)

    def parse_room(self, response):

        def extract_meta_information(container, name):
            search_string = "//div[contains(@class, '%s')]//p[contains(.//text(), '%s')]//text()" % (container, name)
            address_information = response.xpath(search_string).extract()
            return address_information[1].strip()

        street = extract_meta_information('adress-region', 'Adresse')
        city = extract_meta_information('adress-region', 'Ort')
        from_date = extract_meta_information('date-cost', 'Ab dem')
        to_date = extract_meta_information('date-cost', 'Bis')
        rent = extract_meta_information('date-cost', 'Miete / Monat')

        self.log(rent)
        self.log(to_date)
        self.log(from_date)
        self.log(street)
        self.log(city)


