import requests
import re
import datetime
from lxml import html
from pymongo import MongoClient
from pymongo import errors

client = MongoClient('127.0.0.1', 27017)
db = client['news']
yandex_news = db.yandex_news

url = 'https://yandex.ru/news'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)

items = dom.xpath("//h1[@id='top-heading']/..//div[contains(@class, 'mg-grid__col')]")

for item in items:
    link = item.xpath(".//h2/a/@href")

    _id = re.search(r'(\d+)$', link[0]).group()
    link = link[0].split('?')[0]
    name = item.xpath(".//h2/a/text()")
    date = item.xpath(".//span[@class='mg-card-source__time']/text()")
    source = item.xpath(".//a[@class='mg-card__source-link']/text()")

    try:
        yandex_news.insert_one({'_id': _id,
                                'link': link,
                                'name': name[0].replace('\xa0', ' '),
                                'date': f'{datetime.date.today()} {date[0]}',
                                'source': source[0]
                                })
    except errors.DuplicateKeyError:
        continue
