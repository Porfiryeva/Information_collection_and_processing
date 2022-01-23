"""
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через
аргументы получаем должность) с сайтов HH(обязательно) и/или Superjob(по желанию).
Приложение должно анализировать несколько страниц сайта (также вводим через input или
аргументы). Получившийся список должен содержать в себе минимум:
    Наименование вакансии.
    Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры
преобразуем к цифрам).
    Ссылку на саму вакансию.
    Сайт, откуда собрана вакансия (можно указать статично для hh - hh.ru, для superjob -
superjob.ru)
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно
вывести с помощью dataFrame через pandas. Сохраните в json либо csv.
"""
import requests
import pandas
from bs4 import BeautifulSoup

names = []
min_salaries = []
max_salaries = []
currencies = []
text_salaries = []
links = []
from_sites = []


def scan_pages(page, subj):
    url = 'https://hh.ru/search/vacancy'
    params = {'text': subj,
              'page': page
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

        name = vacancy.find('a').getText().replace('\xa0', ' ')
        names.append(name)

        link = vacancy.find('a').get('href')
        if link.find('hh.ru') != -1:
            link = link.partition('?')[0].partition('.')[2]
            links.append('https://' + link)
        else:
            links.append(link)

        try:
            salary_txt = vacancy.find_all('span', {
                'class': 'bloko-header-section-3'})[1].getText().replace('\u202f', '')
            text_salaries.append(salary_txt)
            salary_lst = salary_txt.split(' ')
            currencies.append(salary_lst[-1])

            if len(salary_lst) == 4:
                min_salaries.append(int(salary_lst[0]))
                max_salaries.append(int(salary_lst[2]))
            elif len(salary_lst) == 3:

                if salary_lst[0] == 'от':
                    min_salaries.append(int(salary_lst[1]))
                    max_salaries.append(None)
                elif salary_lst[0] == 'до':
                    min_salaries.append(None)
                    max_salaries.append(int(salary_lst[1]))
                else:
                    min_salaries.append(None)
                    max_salaries.append(None)

            else:
                min_salaries.append(None)
                max_salaries.append(None)

        except IndexError:
            min_salaries.append(None)
            max_salaries.append(None)
            currencies.append(None)
            text_salaries.append(None)

        from_sites.append('hh.ru')


pages = 3
subj = 'Python'

is_accomplish = []
for i in range(pages):
    scan_pages(i, subj)
    if len(is_accomplish) > 0:
        print('Вакансии закончились')
        break


vacancies_df = pandas.DataFrame({
    'name': names,
    'min_salary': min_salaries,
    'max_salary': max_salaries,
    'currency': currencies,
    'text_salary': text_salaries,
    'link': links,
    'from_site': from_sites
})

# vacancies_df.to_csv('hh_vacancies.csv', index=False)
