# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo import errors


class BooksPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.books

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]

        if spider.name == 'book24ru':
            item['_id'] = item['url'].split('-')[-1].rstrip('/')
            item['author'], item['name'] = self.process_title_book24ru(item.get('title'))
            del item['title']
            if item['price']:
                item['price'] = int(item.get('price').replace('\xa0', '').strip(' ').split(' ')[0])
            if item['discount_price']:
                item['discount_price'] = int(item.get('discount_price').replace('\xa0', '').strip(' ').split(' ')[0])
            item['rating'] = float(item.get('rating').replace(',', '.').replace(' ', ''))
        else:
            if item['price']:
                item['price'] = int(item.get('price'))
            if item['discount_price']:
                item['discount_price'] = int(item.get('discount_price'))
            item['rating'] = float(item.get('rating'))

        try:
            collection.insert_one(item)
        except errors.DuplicateKeyError:
            pass

        return item

    def process_title_book24ru(self, auth_name):
        auth_name = auth_name.split(':', maxsplit=1)
        if len(auth_name) == 1:
            author = None
            name = auth_name[0].strip(' ')
        else:
            author = auth_name[0].strip(' ').split(',')
            name = auth_name[1].strip(' ')
        return author, name
