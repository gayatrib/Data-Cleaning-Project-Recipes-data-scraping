# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkItem(scrapy.Item):
	link = scrapy.Field()
	
class RecipeItem(scrapy.Item):
	link = scrapy.Field()
	name = scrapy.Field()
	description = scrapy.Field()
	author = scrapy.Field()
	ingredients = scrapy.Field()
	method = scrapy.Field()
