"""
2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти
среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя
авторизацию. Ответ сервера записать в файл.
Если нет желания заморачиваться с поиском, возьмите API вконтакте
(https://vk.com/dev/first_guide). Сделайте запрос, чтобы получить список всех сообществ
на которые вы подписаны.
"""
import requests
import json

access_token = ''
user_id = '664002'
url = 'https://api.vk.com/method/groups.get'

params = {'v': '5.131',
          'access_token': access_token,
          'user_id': user_id,
          'extended': 1
}

response = requests.get(url, params=params)
response_j = response.json()

# with open('vk_groups.json', 'w') as f:
#     json.dump(response_j, f)

print(f'Список сообществ пользователя {user_id}: ')
for el in response_j.get('response').get('items'):
    print(f"\t{el.get('name')} c id={el.get('id')}")
