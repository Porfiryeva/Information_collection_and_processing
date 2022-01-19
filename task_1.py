"""
1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
для конкретного пользователя, сохранить JSON-вывод в файле *.json.
"""
import requests
import json

username = 'Porfiryeva'
request = 'repos'
url = f'https://api.github.com/users/{username}/{request}'

response = requests.get(url)
response_j = response.json()

with open('user_repos1.json', 'w') as f:
    json.dump(response_j, f)

print(f'Список публичных репозиториев пользователя {username}: ')
for el in response_j:
    print(el.get('name'))
