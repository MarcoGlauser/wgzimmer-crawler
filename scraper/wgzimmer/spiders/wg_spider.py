import hashlib
import random

import scrapy
from scrapy import FormRequest

from scraper.wgzimmer.items import WgzimmerItem


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
        for clean_link in cleaned_links:
            yield scrapy.Request(response.urljoin(clean_link), callback=self.parse_room)

    def parse_room(self, response):

        def extract_meta_information(container, name):
            search_string = "//div[contains(@class, '%s')]//p[contains(.//text(), '%s')]//text()" % (container, name)
            address_information = response.xpath(search_string).extract()
            return address_information[1].strip()

        def extract_description(css_class):
            search_string = ".%s p::text" % css_class
            return response.css(search_string).extract_first()

        data = {
            'url': response.url,
            'rent': extract_meta_information('date-cost', 'Miete / Monat'),
            'from_date': extract_meta_information('date-cost', 'Ab dem'),
            'to_date': extract_meta_information('date-cost', 'Bis'),
            'street': extract_meta_information('adress-region', 'Adresse'),
            'city': extract_meta_information('adress-region', 'Ort'),
            'room_description': extract_description("mate-content"),
            'profile_description': extract_description('room-content'),
            'mates_description': extract_description("person-content")
        }

        return WgzimmerItem(**data)
