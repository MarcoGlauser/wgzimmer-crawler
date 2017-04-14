# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import dateparser
import re

import geocoder
from django.contrib.gis.geos import GEOSGeometry


class WgzimmerPipeline(object):
    def process_item(self, item, spider):
        item['room_identifier'] = hashlib.sha256(item['url'].encode()).hexdigest()
        item['from_date'] = dateparser.parse(item['from_date'])
        if item['to_date'] == 'Unbefristet':
            item['to_date'] = None
            item['to_text'] = None
        else:
            item['to_text'] = item['to_date']
            try:
                item['to_date'] = dateparser.parse(item['to_date'])
            except ValueError:
                item['to_date'] = None

        item['rent'] = "".join(re.findall(r'\d+', item['rent']))

        try:
            item.django_model.objects.get(room_identifier=item['room_identifier'])
        except item.django_model.DoesNotExist:
            geometry_string = geocoder.google(", ".join([item['street'], item['city']])).wkt
            print(geometry_string)
            item['location'] = GEOSGeometry(geometry_string)
            item.save()

        return item
