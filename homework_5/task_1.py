"""
Написать программу, которая собирает входящие письма из своего или тестового почтового
ящика и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма,
текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172#
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import time


def authorization(login, password):
    driver.get('https://mail.ru/')

    element = driver.find_element(By.NAME, 'login')
    element.send_keys(login)
    element.send_keys(Keys.RETURN)
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.NAME, 'password')))
    element.send_keys(password)
    element.send_keys(Keys.ENTER)


def get_links():
    # не знаю, какое здесь событие: что-то подсчитывается для title?
    driver.implicitly_wait(10)
    element = driver.find_element(By.XPATH, '//a[contains(@title, "Входящие")]')
    total_inc = int(element.get_attribute("title").split(' ')[1])  # число входящих
    # print(total_inc)

    # при первом сборе - от 27 до 29 (неясно, отчего), далее - 30, при каждом скролле добавляется 11 новых
    while len(links) < total_inc:
        element = driver.find_elements(By.XPATH, "//a[contains(@href, '/inbox/0')]")

        for el in element:
            link = el.get_attribute('href')
            links.add(link)

        actions = ActionChains(driver)
        actions.move_to_element(element[-1])
        actions.perform()
        time.sleep(3)


def get_letters(links):
    for link in links:
        time.sleep(3)  # не знаю чего, но чего-то ждём
        driver.get(link)

        _id = link.split(':')[2]

        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='letter__author']/span")))
        sender = element.get_attribute('title')

        element = driver.find_element(By.CLASS_NAME, 'letter__date')
        date = element.text

        element = driver.find_element(By.CLASS_NAME, 'thread-subject')
        subject = element.text

        element = driver.find_element(By.CLASS_NAME, 'letter-body__body-content')
        text = element.text
        if not text:
            element = element.find_elements(By.TAG_NAME, 'img')
            for el in element:
                text += el.get_attribute('alt') + ' '

        mails.insert_one({'_id': _id,
                          'sender': sender,
                          'date': date,  # Сегодня или Вчера надо обработать отдельно!
                          'subject': subject,
                          'text': text})


chrome_options = Options()
chrome_options.add_argument("start-maximized")
driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)

client = MongoClient('127.0.0.1', 27017)
db = client['mail_ru']
mails = db.mails

login = 'study.ai_172@mail.ru'
password = 'NextPassword172#'
authorization(login, password)

links = set()
get_links()
get_letters(links)
