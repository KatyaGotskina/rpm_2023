from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import monotonic
from config import DATA, SURVIVAL_BUTTON_XPATH, NO_AUTH_BUTTON


working_time = int(input('Сколько программе работать : '))
driver = webdriver.Chrome()
driver.get("https://www.invokergame.com/")

search_button = driver.find_element(By.XPATH, value=SURVIVAL_BUTTON_XPATH).click()
steam_enter = driver.find_element(By.XPATH, value=NO_AUTH_BUTTON).click()

start_time = monotonic()
BODY = driver.find_element(By.TAG_NAME, 'body')
BODY.send_keys(Keys.ENTER)
prelast = ''
last = ''
while monotonic() - start_time < working_time:
    page = driver.page_source
    soup = BeautifulSoup(page, "lxml")
    conteiners = soup.find_all("td", class_="ActiveSpell")

    for conteiner in conteiners:
        spell = conteiner.find("span").text
        if spell == prelast:
            BODY.send_keys('F')
        elif spell == last:
            BODY.send_keys('D')

        buttons = DATA[spell]
        BODY.send_keys(buttons[0])
        BODY.send_keys(buttons[1])
        BODY.send_keys(buttons[2])
        BODY.send_keys('R')
        BODY.send_keys('D')
        prelast = last 
        last = spell