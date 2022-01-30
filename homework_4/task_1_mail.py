"""
1. Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru,
lenta.ru, yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:
название источника;
наименование новости;
ссылку на новость;
дата публикации.
2. Сложить собранные новости в БД
"""
import requests
import re
from lxml import html
from pymongo import MongoClient
from pymongo import errors

client = MongoClient('127.0.0.1', 27017)
db = client['news']
mail_news = db.mail_news


url = 'https://yandex.ru/news'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)

links = dom.xpath("//a[contains(@class, 'js-topnews__item')]/@href | //li[@class='list__item']/a/@href")
for news_link in links:
    news_response = requests.get(news_link, headers=headers)
    news_dom = html.fromstring(news_response.text)

    _id = re.search(r'(\d+)', news_link).group()
    name = news_dom.xpath("//h1/text()")
    date = news_dom.xpath("//span[@datetime]/@datetime")
    source = news_dom.xpath("//span[@class='note']//span[@class='link__text']/text()")

    try:
        mail_news.insert_one({'_id': _id,
                              'link': news_link,
                              'name': name[0],
                              'date': date[0],
                              'source': source[0]
                              })
    except errors.DuplicateKeyError:
        continue
