from src.scraping.json_to_xlsx import *
from src.scraping.scraping_leilaoimovel import *
from src.mapping import *
from src.scraping.scraping_olx import *
import os
import time

def chose_extract_data():
    while True:
        print('----\nQual site você deseja acessar?\n  1 - leilaoimoveis.com.br\n  2 - ')
        input_command = int(input('Escolha o número da operação desejada: '))
        if input_command in [1]:
            break
        else:
            print('----\nDIGITE UM NÚMERO VÁLIDO!')
    if input_command == 1:
        print('----\nQual o município desejado? Escreva no formato do exemplo: Exemplo: fortaleza-ce')
        cidades = input('Nome do município: ')
        cidades = cidades.split()
        driver = setup_webdriver()
        for cidade in cidades:
            website = 'https://www.leilaoimovel.com.br/leilao-de-imovel/' + cidade
            start_time = time.time()
            create_n_save_df_leilaoimoveis(website, driver)
            end_time = time.time()
            print(f'A extração dos dados demorou {(end_time-start_time)/60:2f} minutos.')
        

def chose_plot_map():
    print('----\nQual mapa você deseja plotar?')
    sheets = os.listdir(r'output\planilhas')
    for i in range(len(sheets)):
        print(i+1, '-', sheets[i])
    while True:
        input_command = int(input('Digite o número da tabela que deseja mapear: '))
        print('\n')
        if input_command in range(len(sheets) + 1):
            break
        else:
            print('----\nDIGITE UM NÚMERO VÁLIDO!')
    sheet_path = 'output\\planilhas\\' + sheets[input_command - 1] # plota uma unidade de mapa
    df = pd.read_excel(sheet_path)
    name = sheets[input_command - 1].split('_')[-1].split('.')[0]
    start_time = time.time()
    plot_map(df, name)
    end_time = time.time()
    print(f'A extração dos dados demorou {(end_time-start_time)/60:2f} minutos.')

def chose_concat_df():
    sheets = os.listdir(r'output\planilhas')
    for i in range(len(sheets)): # imprime as planilhas disponíveis
        print(i+1, '-', sheets[i])
    while True: # while para digitar o número correto
        invalid_index = 0 # para verificar se todos os dígitos são corretos
        sheets_index = input('Digite os número da planilhas que deseja concatenar: ').split()
        for i in range(len(sheets_index)): # transformar em inteiro
            sheets_index[i] = int(sheets_index[i])
        for index in sheets_index: # for para manter ou sair do laço que verifica se os índices escritos são corretos
            if index not in list(range(len(sheets) + 1)):
                print('----\nDIGITE UM NÚMERO VÁLIDO!')
                invalid_index = 1
                break
        if invalid_index == 0:
            break

    sheet_name = []
    new_sheet_name = ''
    sheet_name.append(sheets[sheets_index[0]-1])
    df = pd.read_excel('output\\planilhas\\' + sheets[sheets_index[0]-1]) # define primeira planilha
    if len(sheets_index) > 1: # verifica se não foi apenas uma planilha selecionada
        for i in range(1, len(sheets_index)):
            df_new =  pd.read_excel('output\\planilhas\\' + sheets[sheets_index[i]-1])
            sheet_name.append(sheets[sheets_index[i]-1])
            df = pd.concat([df, df_new])
        for name in sheet_name:
            new_sheet_name += '-' + name.split('_')[1].split('.')[0][0:-3]
        new_sheet_name = new_sheet_name[1:]
        df.to_excel(f'output//planilhas//{new_sheet_name}.xlsx', index=False)
    else:
        print('----\nNão é possível concatenar apenas uma planilha')


def chose_extract_olx():
    url = input('Cole aqui a URL da página da OLX que deseja extrair os dados: ')
    file_name = input('\nComo você  deseja nomear a planilha? Digite o nome do arquivo sem a extensão: ')
    driver = setup_webdriver()
    create_n_save_df_olx(url, driver, file_name)
    # while True:
    #     print('----\nQual operação você deseja realizar?\n  1 - extrair dados da OLX\n  2 - extrair nome dos anunciantes\n  3 - extrair dados da OLX e nome dos anunciantes (é mais recomendado fazer as outras duas operações separadas.)\n')
    #     input_command = int(input('Escolha o número da operação desejada: '))
    #     if input_command in list(range(1, 4)):
    #         break
    #     else:
    #         print('----\nDIGITE UM NÚMERO VÁLIDO!')
    # if input_command == 1:
    #     driver = setup_webdriver()
    #     url = input('Cole aqui a URL da página da OLX que deseja extrair os dados: ')
    #     file_name = input('Como você  deseja nomear a planilha? Digite o nome do arquivo sem a extensão: ')
    #     create_n_save_df_olx(url, driver, file_name)
    # elif input_command == 2:
    #     driver = setup_webdriver()
    #     extract_seller_n_date(driver)
    # elif input_command == 3:
    #     driver = setup_webdriver()
    #     url = input('Cole aqui a URL da página da OLX que deseja extrair os dados: ')
    #     file_name = input('Como você  deseja nomear a planilha? Digite o nome do arquivo sem a extensão: ')
    #     create_n_save_df_olx(url, driver, file_name, True)

