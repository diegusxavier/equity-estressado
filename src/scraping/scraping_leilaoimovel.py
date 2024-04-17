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

# return the number of pages in website
def len_pages(website, driver):
    driver.get(website)
    id = driver.find_element(By.ID, 'pagination')
    a = id.find_elements(By.TAG_NAME, 'a')
    if len(a) > 1:
        a = int(a[-2].text)
    else:
        a = 1
    return a

# get url of actual website and append to the links_list; the https://www.leilaoimovel.com.br/imoveis-springfield isn't added to the list
def get_page_links(links_list, driver):
    properties = driver.find_elements(By.XPATH, "//div[@class='place-box']")
    for property in properties:
        if property.find_element(By.CLASS_NAME, 'Link_Redirecter').get_property('href') != 'https://www.leilaoimovel.com.br/imoveis-springfield':
            links_list.append(property.find_element(By.CLASS_NAME, 'Link_Redirecter').get_property('href'))

# get all links of all pages of website
def get_all_ad_links(website, driver):
    links_list = []
    for num_page in range(1, len_pages(website, driver)+1):
        currently_site = website + '?pag=' + str(num_page)
        driver.get(currently_site)
        get_page_links(links_list, driver)
    return links_list


# web scraping algorithm for extract the important data of the link
def extract_data(link, driver):
    driver.get(link)

    # VERIFY THE AUCTION TYPE
    # type = auction_type(link)

    # 1 - SPATIAL INFO
    total_area = None 
    util_area = None 
    bedrooms = None 
    car_vacancies = None 

    # UNFORMATED INFOS - infos that aren't common to each other
    auction_price = None 
    evaluation_price = None 
    cash_price = None
    discount = 0.0 
    first_price = None 
    second_price = None 
    start_date = None 
    end_date = None
    first_date = None
    second_date = None
    auctioneer = None
    real_estate_registration = None
    registration = None
    property_type = None
    type_of_sale = None

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
        if 'Tipo' in div.text and len(div.text.split()) < 20:
            type_of_sale = div.text.split('/')[-1]
            property_type = div.text.split('/')[0].split(':')[-1]
            if property_type[-1] == ' ':
                property_type = property_type[0:-1]
            if property_type[0] == ' ':
                property_type = property_type[1:]
    if 'Encerra' in driver.find_element(By.XPATH, r'/html/body/div/main/div[9]/section[3]/div/div[2]/div[2]/div/div/div').text: # pode ter erro
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
        elif 'vista' in div.text:
            if first_price != None:
                cash_price = (div.text.split()[4])
            else:
                cash_price = first_price

                
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
    if cash_price != None:
        cash_price = float(cash_price.replace('.', '').replace(',', '.'))
    if registration != None and registration.isnumeric():
        int(registration)
    if real_estate_registration != None and real_estate_registration.isnumeric():
        int(real_estate_registration)
    else:
        real_estate_registration = 0

    # discount calc
    if first_price != None and second_price != None:
        if first_price > second_price:
            discount = (first_price - second_price)/first_price
    elif evaluation_price != None and cash_price != None:
        discount = (evaluation_price - cash_price)/evaluation_price
    elif evaluation_price != None:
        discount = (evaluation_price - auction_price)/evaluation_price

    discount = discount*100    

    return [property_type, auction_price, total_area, util_area, bedrooms, car_vacancies, first_price, second_price, evaluation_price, cash_price, discount, start_date, end_date, first_date, second_date, type_of_sale, auctioneer, registration, real_estate_registration, localization, ad_link]



def get_website():
    with open(r"src\utils\websites.txt", "r") as websites:
        website_list = []
        for website in websites:
            website_list.append(website) 
        websites.close()
    return website_list

def page_exists(website):
    content = requests.get(website).content
    site = BeautifulSoup(content, 'html.parser')
    if 'A página que você está procurando não existe' in site.prettify():
        cidade_errada = website.split('/')[-1]
        print(f'A cidade {cidade_errada} não existe ou foi digitada errada.')
        return 0
    else: 
        return 1

def create_n_save_df_leilaoimoveis(website, driver):
    if page_exists(website) == 1:
        df_columns = ['Tipo de Imóvel','Valor do Leilão', 'Área Total [m²]', 'Área Útil [m²]', 'Quartos', 'Vagas', 'R$ 1a Praça', 'R$ 2a Praça', 'Valor Avaliado', 'Valor à Vista', 'Desconto','Data de Início', 'Data de Encerramento', 'Data 1a Praça', 'Data 2a Praça', 'Tipo de Venda', 'Leiloeiro', 'Matrícula', 'Inscrição Imobiliária', 'Localização', 'Link']
        df = pd.DataFrame(columns=df_columns)

        cidade = website.split('/')[-1]
        
        links_list = get_all_ad_links(website, driver)
        
        for i in range(len(links_list)):
            print(f'{i} |', links_list[i], '\n')
            currently_row = extract_data(links_list[i], driver)
            df.loc[len(df)] = currently_row
            # df.to_excel(f'output//leilaoimoveis_{cidade}.xlsx', index=False)
        df.to_excel(f'output//planilhas//leilaoimoveis_{cidade}.xlsx', index=False)
