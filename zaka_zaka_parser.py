import json
import time
import requests
from bs4 import BeautifulSoup


games_prices = {}
zaka_url = 'https://zaka-zaka.com/game/new'
for page_num in range(1, 16):
    response = requests.get(zaka_url + "/page{id}".format(id=page_num))
    print('Собираю данные со страницы {}..'.format(page_num))
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        containers = soup.find_all(class_='game-block')
        for container in containers:
            if "game-block-more" in container.get("class"):
                continue
            name = container.find(class_="game-block-name")
            price = container.find(class_="game-block-price")
            games_prices[name.text] = {"price": float(price.text[:-1])}

    else:
        print('Возникла ошибка:', response.status_code)
time.sleep(0.5)

with open("zaka.json", "w") as json_file:
    json.dump(games_prices, json_file,  indent=4)
