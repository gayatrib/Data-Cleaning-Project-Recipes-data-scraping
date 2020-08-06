# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
#from urllib.parse import urljoin
from urlparse import urljoin
from christmas_cooking import items
from scrapy.crawler import CrawlerProcess

#docker run --memory=6GB --restart unless-stopped -d -p 8050:8050 scrapinghub/splash --max-timeout 600 --slots 20 --disable-private-mode

class GetLinks(scrapy.Spider):
	name = 'get_links'
  
	def start_requests(self):
		page='https://www.bbcgoodfood.com/search?query=christmas/'	
		#page='https://www.bbcgoodfood.com/search/recipes?query=dosa/'	
		self.log("Requesting: " + page)
		yield SplashRequest(url=page, callback=self.parse)

	def parse(self, response):
		for url in Selector(response).xpath("//div[@class='teaser-item__image']/a/@href").extract():
			linkitem=items.LinkItem()
			url=urljoin(response.url,url)
			linkitem['link']=url
			yield(linkitem)
			
		next_page_url = response.xpath("//li[@class = 'pager-next bg-turquoise-safe last']/a/@href").extract_first()
		#print(next_page_url)
		if next_page_url:
			next_page_url = response.urljoin(next_page_url)
			yield scrapy.Request(url=next_page_url, callback=self.parse)