from src.scraping.scraping_leilaoimovel import *
from src.mapping.mapping import *

def main():
    # inicia o prompt perguntando o que fazer
    print('----\nQual operação você deseja realizar?\n  1 - Extrair dados de um site\n  2 - Fazer mapeamento dos imóveis da região')
    input_command = int(input('Escolha o número da operação desejada: '))

    if input_command == 1:
        chose_extract_data()
    elif input_command == 2:
        chose_plot_map()

def chose_extract_data():
    print('----\nQual site você deseja acessar?\n  1 - leilaoimoveis.com.br\n  2 - ')
    input_command = int(input('Escolha o número da operação desejada: '))
    if input_command == 1:
        print('----\nQual o município desejado?\n  1 - Fortaleza (CE)\n  2 - Eusébio (CE)')
        input_command = int(input('Escolha o número referente ao estado desejado: '))
        if input_command == 1:
            create_n_save_df(r'https://www.leilaoimovel.com.br/leilao-de-imovel/fortaleza-ce')
        elif input_command == 2:
            create_n_save_df(r'https://www.leilaoimovel.com.br/leilao-de-imovel/eusebio-ce')

def chose_plot_map():
    print('----\nQual mapa você deseja plotar\n  1 - Fortaleza (CE)\n  2 - Eusébio (CE)')
    input_command = int(input('Escolha o número referente ao mapa escolhido: '))
    if input_command == 1:
        dataframe = pd.read_excel('output\leilaoimoveis_fortaleza-ce.xlsx')
        plot_map(dataframe, 'fortaleza-ce')
    elif input_command == 2:
        dataframe = pd.read_excel('output\leilaoimoveis_eusebio-ce.xlsx')
        plot_map(dataframe, 'eusebio-ce')

if __name__ == '__main__':
    main()
