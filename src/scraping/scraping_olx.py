import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
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

def extract_data(link, driver):
    driver.get(link)

    # details
    area = None
    bathdrooms = None
    bedrooms = None
    car_vacancies = None

    condominium_features = []
    property_features = []
