import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
import json


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
        

def get_data(page_ad):

    if list(page_ad.keys())[0] == 'subject':

        title = None
        price = None
        location = None
        url = None
        category = None
        real_estate_type = None
        size = None
        rooms = None
        bathrooms = None
        condominio = None
        garage_spaces = None
        iptu = None
        re_types = None
        re_features = None
        re_complex_features = None

        if 'title' in list(page_ad.keys()):
            title = page_ad['title']
            print('Título:', title)
        if 'price' in list(page_ad.keys()):
            price = page_ad['price']
            if price != None:
                price = float(price.replace('R$', '').replace('.', '').replace(',', '.'))
            print('Preço:', price)
        if 'location' in list(page_ad.keys()):
            location = page_ad['location']
            print('Localização:', location)
        if 'url' in list(page_ad.keys()):
            url = page_ad['url']
            print('URL:', url)
        if 'category' in list(page_ad.keys()):
            category = page_ad['category']
            print('Categoria:', category)
        if 'properties' in list(page_ad.keys()):
            for dict in page_ad['properties']:
                if dict['name'] == 'real_estate_type':
                    real_estate_type = dict['value']
                    print('Categoria:', real_estate_type)
                if dict['name'] == 'size':
                    size = float(dict['value'].replace('.', '').replace(',', '.').replace('m²', ''))
                    print('Área Útil:', size)
                if dict['name'] == 'rooms':
                    rooms = dict['value']
                    print('Quartos:', rooms)
                if dict['name'] == 'bathrooms':
                    bathrooms = dict['value']
                    print('Banheiros:', bathrooms)
                if dict['name'] == 'garage_spaces':
                    garage_spaces = dict['value']
                    print('Vagas de garagem:', garage_spaces)
                if dict['name'] == 're_types':
                    re_types = dict['value']
                    print('Tipo:', re_types)
                if dict['name'] == 'condominio':
                    condominio = dict['value']
                    if condominio != None:
                        condominio = float(condominio.replace('R$', '').replace('.', '').replace(',', '.'))
                    print('Valor Condomínio:', condominio)
                if dict['name'] == 'iptu':
                    iptu = dict['value']
                    if iptu != None:
                        iptu = float(iptu.replace('R$', '').replace('.', '').replace(',', '.'))
                    print('Valor IPTU:', iptu) 
                if dict['name'] == 're_features':
                    re_features = dict['value']
                    print('Features do imóvel:', re_features)
                if dict['name'] == 're_complex_features':
                    re_complex_features = dict['value']
                    print('Features do condomínio:', re_complex_features)
        print('\n')
    
        return [title, location, category, real_estate_type, size, price, rooms, bathrooms, condominio, garage_spaces, iptu, re_types, re_features, re_complex_features, url]
    

def create_n_save_df_olx(website, driver):
    df_columns = ['Título', 'Localização', 'Categoria', 'Tipo de Imóvel', 'Área Útil', 'Preço', 'Quartos', 'Banheiros', 'Valor Condomínio', 'Vagas de Garagem', 'Valor IPTU', 'Tipo', 'Features do Imóvel', 'Features do Condomínio', 'URL']
    df = pd.DataFrame(columns=df_columns)
    
    for i in range(1,101):
        new_website = website + f'?o={i}'
        if page_exists(new_website, driver):
            element = driver.find_element(By.ID, '__NEXT_DATA__')
            json_text = driver.execute_script('return arguments[0].innerHTML;', element)
            data = json.loads(json_text)
            page_ads = data['props']['pageProps']['ads']
            for page_ad in page_ads:
                currently_row = get_data(page_ad)
                df.loc[len(df)] = currently_row
        df.to_excel(f'output//planilhas//scraping_olx.xlsx', index=False)
