import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By

def get_page_links(links_list):
    properties = driver.find_elements(By.XPATH, "//div[@class='place-box']")
    for property in properties:
        links_list.append(property.find_element(By.CLASS_NAME, 'Link_Redirecter').get_property('href'))
        # remove https://www.leilaoimovel.com.br/imoveis-springfield



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


