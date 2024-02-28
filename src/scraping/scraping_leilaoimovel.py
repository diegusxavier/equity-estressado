import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup

# get url of actual website and append to the links_list, the https://www.leilaoimovel.com.br/imoveis-springfield isn't added to the list
def get_page_links(links_list):
    properties = driver.find_elements(By.XPATH, "//div[@class='place-box']")
    for property in properties:
        if property.find_element(By.CLASS_NAME, 'Link_Redirecter').get_property('href') != 'https://www.leilaoimovel.com.br/imoveis-springfield':
            links_list.append(property.find_element(By.CLASS_NAME, 'Link_Redirecter').get_property('href'))

def get_all_ad_links(links_list, website):
    for num_page in range(len_pages(website)):
        currently_site = website + '?pag=' + str(num_page)
        driver.get(currently_site)
        get_page_links(links_list)


def extract_data(link):
    driver.get(link)

    # VERIFY THE AUCTION TYPE
    type = auction_type(link)

    # 1 - SPATIAL INFO
    total_area = None #
    util_area = None #
    bedrooms = None #
    car_vacancies = None #

    # UNFORMATED INFOS - infos that aren't common to each other
    auction_price = None #
    evaluation_price = None 
    discount = None 
    first_price = None #
    second_price = None #
    start_date = None 
    end_date = None
    first_date = None
    second_date = None
    auctioneer = None


    localization = driver.find_element(By.XPATH, r'/html/body/div/main/div[9]/section[3]/div/div[2]/div[1]/div/div[1]/div[2]/div/div/p').text
    ad_link = link
    
    # 1 - SPATIAL INFO
    spatial_info = driver.find_element(By.XPATH, r'/html/body/div/main/div[9]/section[3]/div/div[2]/div[1]/div/div[2]')
    for element in spatial_info.find_elements(By.CLASS_NAME, 'detail'):
        if element.find_element(By.CLASS_NAME, 'mb-1').text == 'Área Útil:':
            util_area = element.find_element(By.CLASS_NAME, 'icon').find_element(By.TAG_NAME, 'span').text
        elif element.find_element(By.CLASS_NAME, 'mb-1').text == 'Área Terreno:':
            total_area = element.find_element(By.CLASS_NAME, 'icon').find_element(By.TAG_NAME, 'span').text
        elif element.find_element(By.CLASS_NAME, 'mb-1').text == 'Quartos:':
            bedrooms = element.find_element(By.CLASS_NAME, 'icon').find_element(By.TAG_NAME, 'span').text
        elif element.find_element(By.CLASS_NAME, 'mb-1').text == 'Vagas:':
            car_vacancies = element.find_element(By.CLASS_NAME, 'icon').find_element(By.TAG_NAME, 'span').text
    

    # MONEY INFO
    if type == 0:
        auction_price = driver.find_element(By.XPATH, r'/html/body/div/main/div[9]/section[3]/div/div[2]/div[2]/div/div/div/div[1]/div/div/h2').text
        first_price = driver.find_element(By.XPATH, r'/html/body/div/main/div[9]/section[3]/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[2]/h3').text
        second_price = driver.find_element(By.XPATH, r'/html/body/div/main/div[9]/section[3]/div/div[2]/div[2]/div/div/div/div[4]/div[2]/div[2]/h3').text
        first_date = driver.find_element(By.XPATH, r'/html/body/div/main/div[9]/section[3]/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[1]/p').text.split()[0]
        second_date = driver.find_element(By.XPATH, r'/html/body/div/main/div[9]/section[3]/div/div[2]/div[2]/div/div/div/div[4]/div[2]/div[1]/p').text.split()[0]
        start_date = driver.find_element(By.XPATH, r'/html/body/div/main/div[9]/section[3]/div/div[2]/div[1]/div/div[4]/div[6]').text.split()[3]
    elif type == 1 or type == 2:
        if type == 2:
            auction_price = driver.find_element(By.XPATH, r'/html/body/div/main/div[9]/section[3]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/h2').text
            evaluation_price = driver.find_element(By.XPATH, r'/html/body/div/main/div[9]/section[3]/div/div[2]/div[2]/div/div/div/div[1]/div/div/h2').text

        more_infos = driver.find_element(By.XPATH, r'/html/body/div/main/div[9]/section[3]/div/div[2]/div[1]/div/div[4]')
        for div in more_infos.find_elements(By.TAG_NAME, 'div'):
            if 'Data' in div.text:
                end_date = div.text.split()[-1]


        if 'Encerra' in BeautifulSoup(requests.get(link).content, 'html.parser').prettify():
            end_date = driver.find_element(By.XPATH, r'/html/body/div/main/div[9]/section[3]/div/div[2]/div[2]/div/div/div/div[4]/p').text.split()[3]
    

# verify if 'Praça' is in the web page
def auction_type(link): 
    content = requests.get(link).content
    site = BeautifulSoup(content, 'html.parser')
    if 'Praça' in site.prettify():
        return 0
    elif 'consultar'in site.prettify():
        return 1
    else:
        return 2

# return the number of pages in website
def len_pages(website):
    driver.get(website)
    a = driver.find_element(By.XPATH, r'/html/body/div/main/section[3]/div/div/div[2]/div/a[5]').get_property('href').split('=')[1]
    return int(a)


# SETUP THE FIREFOX WEBDRIVER
options = webdriver.FirefoxOptions()
options.headless = True
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
links_list = []

get_all_ad_links(links_list, website)

for i in range(len(links_list)):
    print(f'{i} |', links_list[i], '\n')
    extract_data(links_list[i])

