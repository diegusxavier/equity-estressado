from src.scraping.scraping_leilaoimovel import *
from src.mapping.mapping import *
import os

def main():
    # inicia o prompt perguntando o que fazer
    while True:
        print('----\nQual operação você deseja realizar?\n  1 - Extrair dados de um site\n  2 - Fazer mapeamento dos imóveis da região')
        input_command = int(input('Escolha o número da operação desejada: '))
        if input_command in [1, 2]:
            break
        else:
            print('----\nDIGITE UM NÚMERO VÁLIDO!')
    if input_command == 1:
        chose_extract_data()
    elif input_command == 2:
        chose_plot_map()

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
            create_n_save_df(website, driver)
        

def chose_plot_map():
    print('----\nQual mapa você deseja plotar?')
    sheets = os.listdir(r'output\planilhas')
    for i in range(len(sheets)):
        print(i+1, sheets[i])
    while True:
        input_command = int(input('Digite o número da tabela que deseja mapear: '))
        if input_command in range(len(sheets) + 1):
            break
        else:
            print('----\nDIGITE UM NÚMERO VÁLIDO!')
    sheet_path = 'output\\planilhas\\' + sheets[input_command - 1]
    df = pd.read_excel(sheet_path)
    name = sheets[input_command - 1].split('_')[-1].split('.')[0]
    plot_map(df, name)

if __name__ == '__main__':
    main()
