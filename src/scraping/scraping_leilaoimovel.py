import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import time

inicio = time.time()


# get url of actual website and append to the links_list, the https://www.leilaoimovel.com.br/imoveis-springfield isn't added to the list
def get_page_links(links_list):
    properties = driver.find_elements(By.XPATH, "//div[@class='place-box']")
    for property in properties:
        if property.find_element(By.CLASS_NAME, 'Link_Redirecter').get_property('href') != 'https://www.leilaoimovel.com.br/imoveis-springfield':
            links_list.append(property.find_element(By.CLASS_NAME, 'Link_Redirecter').get_property('href'))

def get_all_ad_links(links_list, website):
    for num_page in range(1, len_pages(website)+1):
        currently_site = website + '?pag=' + str(num_page)
        driver.get(currently_site)
        get_page_links(links_list)


def extract_data(link):
    driver.get(link)

    # VERIFY THE AUCTION TYPE
    type = auction_type(link)

    # 1 - SPATIAL INFO
    total_area = None 
    util_area = None 
    bedrooms = None 
    car_vacancies = None 

    # UNFORMATED INFOS - infos that aren't common to each other
    auction_price = None 
    evaluation_price = None 
    discount = None 
    first_price = None 
    second_price = None 
    start_date = None 
    end_date = None
    first_date = None
    second_date = None
    auctioneer = None
    real_estate_registration = None
    registration = None

    localization = driver.find_element(By.XPATH, r'/html/body/div/main/div[9]/section[3]/div/div[2]/div[1]/div/div[1]/div[2]/div/div/p').text
    ad_link = link

    # MORE INFOS (corretly)
    more_infos = driver.find_element(By.CLASS_NAME, r'sobre-imovel')
    for div in more_infos.find_elements(By.TAG_NAME, 'div'):
        if 'Data' in div.text and len(div.text.split()) < 15:
            start_date = div.text.split()[-1]
        if 'Leiloeiro' in div.text and len(div.text.split()) < 20:
            auctioneer = div.text.split('(')[0].split(':')[1]
        if 'Matrícula' in div.text and len(div.text.split()) < 20:
            registration = div.text.split()[-1]
        if 'Inscrição' in div.text and len(div.text.split()) < 20:
            real_estate_registration = div.text.split()[-1]
    if 'Encerra' in BeautifulSoup(requests.get(link).content, 'html.parser').prettify(): # pode ter erro
        end_date = driver.find_element(By.XPATH, r'/html/body/div/main/div[9]/section[3]/div/div[2]/div[2]/div/div/div/div[4]/p').text.split()[2]

    # SPATIAL INFO (correctly)
    spatial_info = driver.find_element(By.XPATH, r'/html/body/div/main/div[9]/section[3]/div/div[2]/div[1]/div/div[2]')
    for element in spatial_info.find_elements(By.CLASS_NAME, 'detail'):
        if element.find_element(By.CLASS_NAME, 'mb-1').text == 'Área Útil:':
            util_area = element.find_element(By.CLASS_NAME, 'icon').find_element(By.TAG_NAME, 'span').text
        elif element.find_element(By.CLASS_NAME, 'mb-1').text == 'Área Terreno:':
            total_area = element.find_element(By.CLASS_NAME, 'icon').find_element(By.TAG_NAME, 'span').text
        elif element.find_element(By.CLASS_NAME, 'mb-1').text == 'Quartos:':
            bedrooms = int(element.find_element(By.CLASS_NAME, 'icon').find_element(By.TAG_NAME, 'span').text)
        elif element.find_element(By.CLASS_NAME, 'mb-1').text == 'Vagas:':
            car_vacancies = int(element.find_element(By.CLASS_NAME, 'icon').find_element(By.TAG_NAME, 'span').text)
    

    # OTHERS INFOS
    price_infos = driver.find_element(By.XPATH, r'/html/body/div/main/div[9]/section[3]/div/div[2]/div[2]/div/div/div')
    for div in price_infos.find_elements(By.TAG_NAME, 'div'):
        # print(div.text.split(), '\n')
        if '1°' in div.text:
            if first_date == None:
                first_div = list(div.text.split())
                first_date = first_div[2]
                first_price = first_div[6]
                auction_price = first_price
            
        elif '2°' in div.text:
            if second_date == None:
                second_div = list(div.text.split())
                second_date = second_div[2]
                second_price = second_div[6]
        elif 'avaliado' in div.text:
            evaluation_price = div.text.split()[-1]
        elif 'Imóvel' in div.text:
            auction_price = div.text.split()[4]
        elif 'Corretor' in div.text:
            auctioneer = div.text.split(':')[1]
            if 'CRECI' in div.text:
                auctioneer = auctioneer.split('CRECI')[0]

        # if 'Encerra' in BeautifulSoup(requests.get(link).content, 'html.parser').prettify():
        #     end_date = driver.find_element(By.XPATH, r'/html/body/div/main/div[9]/section[3]/div/div[2]/div[2]/div/div/div/div[4]/p').text.split()[2]

    if auction_price != None:
        if 'consultar' in auction_price:
            auction_price = None
        else:
            auction_price = float(auction_price.replace('.', '').replace(',', '.'))
    if total_area != None:
        total_area = float(total_area.replace('.', '').replace(',', '.').replace('m²', ''))
    if util_area != None:
        util_area = float(util_area.replace('.', '').replace(',', '.').replace('m²', ''))
    if first_price != None:
        first_price = float(first_price.replace('.', '').replace(',', '.'))
    if second_price != None:
        second_price = float(second_price.replace('.', '').replace(',', '.'))
    if evaluation_price != None:
        evaluation_price = float(evaluation_price.replace('.', '').replace(',', '.'))
    if registration != None and registration.isnumeric():
        int(registration)
    if real_estate_registration != None and real_estate_registration.isnumeric():
        int(real_estate_registration)
    else:
        real_estate_registration = 0
    return [auction_price, total_area, util_area, bedrooms, car_vacancies, first_price, second_price, evaluation_price, start_date, end_date, first_date, second_date, auctioneer, registration, real_estate_registration, localization, ad_link]

# verify if 'Praça' is in the web page
def auction_type(link): 
    content = requests.get(link).content
    site = BeautifulSoup(content, 'html.parser')
    if 'Praça' in site.prettify() and 'única' not in site.prettify():
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
df_columns = ['Valor do Leilão', 'Área Total [m²]', 'Área Útil [m²]', 'Quartos', 'Vagas', 'R$ 1a Praça', 'R$ 2a Praça', 'Valor Avaliado', 'Data de Início', 'Data de Encerramento', 'Data 1a Praça', 'Data 2a Praça', 'Leiloeiro', 'Matrícula', 'Inscrição Imobiliária', 'Localização', 'Link']
df = pd.DataFrame(columns=df_columns)
# df.to_excel(r'output/leilaoimoveis.xlsx', index=False)

get_all_ad_links(links_list, website)

for i in range(len(links_list)):
    # print(f'{i} |', links_list[i], '\n')
    currently_row = extract_data(links_list[i])
    df.loc[len(df)] = currently_row
    # df.to_excel(r'output/leilaoimoveis.xlsx', index=False)

fim = time.time()
tempo_execucao = fim - inicio
df.to_excel(r'output/leilaoimoveis.xlsx', index=False)

print(f"Tempo de execução: {tempo_execucao:.2f} segundos ({tempo_execucao/60}) minutos")

