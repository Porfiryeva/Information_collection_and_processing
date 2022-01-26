"""
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать
функцию, которая будет добавлять только новые вакансии в вашу базу.
"""
import requests
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo import errors

client = MongoClient('127.0.0.1', 27017)
db = client['hh_vacancy']
py_vacancy = db.py_vacancy


def scan_pages(page, subj, update=True):  # update=True если заполняется не с нуля
    url = 'https://hh.ru/search/vacancy'
    params = {'text': subj,
              'page': page,
              'items_on_page': 20
              }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

    response = requests.get(url, params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')

    vacancy_list = dom.find_all('div', {'class': 'vacancy-serp-item'})
    if not vacancy_list:
        is_accomplish.append(True)
        return

    for vacancy in vacancy_list:
        link = vacancy.find('a').get('href')
        if link.find('hh.ru') != -1:
            link = re.search(r'hh.ru\S([^?#]*)', link).group()
            _id = re.search(r'(\d*)$', link).group()
        else:
            _id = link  # для странных ссылок (_id соотв параметру utm_vacancy, но он не всегда отобр)

        if update and py_vacancy.find_one({'_id': _id}):
            continue

        name = vacancy.find('a').getText().replace('\xa0', ' ')

        salary = {'min': None, 'max': None, 'currency': None}

        salary_lst = vacancy.find_all('span', {'class': 'bloko-header-section-3'})
        if len(salary_lst) > 1:
            salary_lst = salary_lst[1].getText().replace('\u202f', '').replace('\xa0', '').split(' ')
            salary['currency'] = salary_lst[-1]

            if len(salary_lst) == 4:
                salary['min'] = int(salary_lst[0])
                salary['maxn'] = int(salary_lst[2])
            elif len(salary_lst) == 3:

                if salary_lst[0] == 'от':
                    salary['min'] = int(salary_lst[1])
                elif salary_lst[0] == 'до':
                    salary['max'] = int(salary_lst[1])

        # тк при анализе в pandas после одного прохождения выдаёт дубли
        try:
            py_vacancy.insert_one({'_id': _id,
                                   'name': name,
                                   'link': link,
                                   'salary': salary,
                                   'from_sites': 'hh.ru'
                                   })
        except errors.DuplicateKeyError:
            continue


subj = 'Python'

i = 0
is_accomplish = []
while not is_accomplish:
    scan_pages(i, subj)
    print(i)
    i += 1
