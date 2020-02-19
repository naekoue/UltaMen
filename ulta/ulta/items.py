# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UltaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
      product = scrapy.Field()
      brand = scrapy.Field()     
      #ingredients = scrapy.Field() 
      #description = scrapy.Field() 
      review_count = scrapy.Field() 
      price = scrapy.Field() 
      review_avg_rating = scrapy.Field() 
      #review_date = scrapy.Field()
      #review_details =scrapy.Field()
      #review_title = scrapy.Field() 
      #review_location = scrapy.Field() 
      #default_size = scrapy.Field() 
      #category = scrapy.Field() 
      url = scrapy.Field()
