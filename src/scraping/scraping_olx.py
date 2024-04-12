import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
import json
import requests
from bs4 import BeautifulSoup

# setup webdriver
def setup_webdriver():
    options = webdriver.FirefoxOptions()
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    options.headless = True
    service = FirefoxService(executable_path=r"drivers/geckodriver.exe")
    driver = webdriver.Firefox(service=service, options=options)
    return driver

# verify if page exists
def page_exists(website, driver):
    driver.get(website)
    if 'Nenhum anúncio' in driver.find_element(By.XPATH, r'/html/body/div[1]/div[1]/main/div/div[2]/main/div[4]').text:
        print('Page not found')
        return False
    return True

def get_page_json(website, driver, list_ads):
    for i in range(1,101):
        new_website = website + f'?o={i}'
        if page_exists(new_website, driver):
            element = driver.find_element(By.ID, '__NEXT_DATA__')
            json_text = driver.execute_script('return arguments[0].innerHTML;', element)
            data = json.loads(json_text)
            page_ads = data['props']['pageProps']['ads']
            for page_ad in page_ads:
                list_ads.append(page_ad)
            print(len(list_ads))
    save_list(list_ads)

def save_list(list):
    with open("file.txt", 'w', encoding='utf-8') as f:
        for item in list:
            f.write(str(item) + '\n')


driver = setup_webdriver()
list_ads = []
get_page_json('https://www.olx.com.br/imoveis/venda/estado-ce/fortaleza-e-regiao', driver, list_ads)
