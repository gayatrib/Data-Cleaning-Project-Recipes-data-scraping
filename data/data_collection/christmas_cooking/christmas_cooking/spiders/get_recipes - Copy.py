# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
#from urllib.parse import urljoin
from urlparse import urljoin
from christmas_cooking import items
import json

#docker run --memory=6GB --restart unless-stopped -d -p 8050:8050 scrapinghub/splash --max-timeout 600 --slots 20 --disable-private-mode

class GetRecipes(scrapy.Spider):
	name = 'get_recipes'
  	
	def start_requests(self):
		pages=pd.read_csv("../../data/links.csv")['link'].dropna(axis=0)
		pages=[page for page in pages if page != 'link']
		for page in pages:
			self.log("Requesting: " + page)
			yield SplashRequest(url=page, callback=self.parse,args={'wait': 1})

	def parse(self, response):
		print(response.url)
		print(response.css('h1.recipe-header__title::text').extract_first())
		description=response.xpath('//div[@class = "field-item even"]/p/text()').extract_first()
		if not description:
			description=response.xpath('//div[@class = "field-item even"]/text()').extract_first()
		print(description)
		print(response.xpath('//meta[@itemprop="datePublished"]/@content').extract_first())		
		print(response.xpath('//span[@class = "author"]/a/text()').extract_first())
		print(response.xpath('//span[contains(@class, "rate-button") and contains(@class, "rate-fivestar-btn-filled")]/text()')[-1].extract())
		print(response.xpath('//div[@class = "rate-info"]/text()').extract())
		print(response.xpath('//span[@class = "recipe-details__cooking-time-prep"]/span[contains(@class,"mins") or contains(@class,"hrs")]/text()').extract())
		print(response.xpath('//span[@class = "recipe-details__cooking-time-cook"]/span[contains(@class,"mins") or contains(@class,"hrs")]/text()').extract())
		print(response.xpath('//section[contains(@class, "recipe-details__item") and  contains(@class,"recipe-details__item--skill-level")]/span[@class = "recipe-details__text"]/text()').extract())
		print(response.xpath('//section[contains(@class, "recipe-details__item") and  contains(@class,"recipe-details__item--servings")]/span[@class = "recipe-details__text"]/text()').extract())
		additional_info=response.xpath('//ul[@class = "additional-info"]/li/text()').extract()
		print(additional_info)
		
		nutrition = []
		nutrition_label = response.xpath('//ul[@class="nutrition"]/li/span[@class="nutrition__label"]/text()').extract()
		nutrition_value = response.xpath('//ul[@class="nutrition"]/li/span[@class="nutrition__value"]/text()').extract()
		nutrition=[" ".join(entry) for entry in zip(nutrition_label, nutrition_value)]
		
		
		#for li in response.xpath('//ul[@class="nutrition"]/li'):
		#	nutrient = " ".join(li.xpath('string(.)').get())
		#	nutrition.append(nutrient)
		print(nutrition)
		ingredients_content=response.xpath('//li[@class = "ingredients-list__item"]/@content').extract()
		print(ingredients_content)
		method_list=response.xpath('//li[@class = "method__item"]/p/text()').extract()
		print(method_list)
		
		recipe = {"Name": response.css('h1.recipe-header__title::text').extract_first(), 
						 "url": response.url, 
						 "Description": description, 
						 "Author": response.xpath('//span[@class = "author"]/a/text()').extract_first(),
						 "Publication Date": response.xpath('//meta[@itemprop="datePublished"]/@content').extract_first(),
						 "Rating": response.xpath('//span[contains(@class, "rate-button") and contains(@class, "rate-fivestar-btn-filled")]/text()')[-1].extract(),
						 "Number of Ratings": response.xpath('//div[@class = "rate-info"]/text()').extract(),
						 "Prep Time": response.xpath('//span[@class = "recipe-details__cooking-time-prep"]/span[contains(@class,"mins") or contains(@class,"hrs")]/text()').extract(),
						 "Cook Time": response.xpath('//span[@class = "recipe-details__cooking-time-cook"]/span[contains(@class,"mins") or contains(@class,"hrs")]/text()').extract(),
						 "Skill Level": response.xpath('//section[contains(@class, "recipe-details__item") and  contains(@class,"recipe-details__item--skill-level")]/span[@class = "recipe-details__text"]/text()').extract(),
						 "Servings": response.xpath('//section[contains(@class, "recipe-details__item") and  contains(@class,"recipe-details__item--servings")]/span[@class = "recipe-details__text"]/text()').extract(),
						 "Additional Info": response.xpath('//ul[@class="additional-info"]/li/text()').extract(),
						 "Nutrition": nutrition,
						 "Ingredients": response.xpath('//li[@class = "ingredients-list__item"]/@content').extract(),
						 "Method": response.xpath('//li[@class = "method__item"]/p/text()').extract()}
		with open("../../data/recipes.json", "a") as fc: 
			json.dump(recipe, fc)
			fc.write('\n')