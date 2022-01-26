"""
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной
платой больше введённой суммы (необходимо анализировать оба поля зарплаты). То есть цифра
вводится одна, а запрос проверяет оба поля
"""
from pprint import pprint
from pymongo import MongoClient

req = 500000

client = MongoClient('127.0.0.1', 27017)
db = client['hh_vacancy']

for doc in db.py_vacancy.find({'salary.currency': 'руб.',
                               '$or': [{'salary.min': {'$gt': req}},
                                       {'salary.max': {'$gt': req}}]}):
    pprint(doc)
