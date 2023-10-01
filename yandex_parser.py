import requests
from bs4 import BeautifulSoup
import lxml
import json


response = requests.get('https://music.yandex.ru/chart')
bs = BeautifulSoup(response.text, "lxml")
containers = bs.find_all('div', class_='d-track typo-track d-track_selectable d-track_with-cover d-track_with-chart')
number = 1
result = {}
for container in containers:
    name = container.find('div', class_='d-track__name')
    meta_information = container.find('div', class_='d-track__meta')
    author = meta_information.find('span', class_='d-track__artists')
    authorName = (str(author.text), str(name.text[3:-2]))
    result[number] = authorName
    number += 1
print(result)
with open('jsonChart.json', 'w', encoding='UTF-8') as f:
    json.dump(result, f, indent=4, ensure_ascii=False)