# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()  # Автор, Автор: название, если нет : автор - None
    _id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()  # если обе None - нет в наличии
    discount_price = scrapy.Field()
    rating = scrapy.Field()
