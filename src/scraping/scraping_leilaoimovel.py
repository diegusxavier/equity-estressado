import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup

def get_page_links(links_list):
    properties = driver.find_elements(By.XPATH, "//div[@class='place-box']")
    for property in properties:
        links_list.append(property.find_element(By.CLASS_NAME, 'Link_Redirecter').get_property('href'))
        # remove https://www.leilaoimovel.com.br/imoveis-springfield

def extract_data(link):
    driver.get(link)

    # 1 - SPATIAL DATA
    total_area = None
    util_area = None
    bedrooms = None
    car_vacancies = None

    auction_price = None
    evaluation = None
    discount = None
    
    start_date = None
    end_date = None
    localization = None
    auctioneer = None

    ad_link = link
    
    # 1 - SPATIAL DATA
    spatial_data = driver.find_element(By.XPATH, r'/html/body/div/main/div[9]/section[3]/div/div[2]/div[1]/div/div[2]')
    for element in spatial_data.find_elements(By.CLASS_NAME, 'detail'):
        if element.find_element(By.CLASS_NAME, 'mb-1').text == 'Área Útil:':
            util_area = element.find_element(By.CLASS_NAME, 'icon').find_element(By.TAG_NAME, 'span').text
        elif element.find_element(By.CLASS_NAME, 'mb-1').text == 'Área Terreno:':
            total_area = element.find_element(By.CLASS_NAME, 'icon').find_element(By.TAG_NAME, 'span').text
        elif element.find_element(By.CLASS_NAME, 'mb-1').text == 'Quartos:':
            bedrooms = element.find_element(By.CLASS_NAME, 'icon').find_element(By.TAG_NAME, 'span').text
        elif element.find_element(By.CLASS_NAME, 'mb-1').text == 'Vagas:':
            car_vacancies = element.find_element(By.CLASS_NAME, 'icon').find_element(By.TAG_NAME, 'span').text
    print(util_area, total_area, bedrooms, car_vacancies)

# SETUP THE FIREFOX WEBDRIVER
options = webdriver.FirefoxOptions()
service = FirefoxService(executable_path=r"drivers/geckodriver.exe")
driver = webdriver.Firefox(service=service, options=options)

# DEFINE THE WEBSITES THAT WE WILL ACESS
with open(r"src\utils\websites.txt", "r") as websites:
    website_list = []
    for website in websites:
        website_list.append(website) 
    websites.close()
website = website_list[0]

# ACESS THE WEBSITE
driver.get(website)


links_list = []
get_page_links(links_list)
extract_data(links_list[4])

