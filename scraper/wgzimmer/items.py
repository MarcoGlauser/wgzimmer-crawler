# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem

# noinspection PyUnresolvedReferences
from room.models import Room


class WgzimmerItem(DjangoItem):
    django_model = Room
