from src.scraping.scraping_leilaoimovel import *
from src.mapping.mapping import *

def main():
    # inicia o prompt perguntando o que fazer
    print('Qual operação você deseja realizar?\n  1 - pegar dados do site leilaoimoveis.com.br\n  2 - fazer mapeamento das areas')
    input_command = int(input('Escolha o número da operação desejada: '))

    if input_command == 1:
        website = r'https://www.leilaoimovel.com.br/leilao-de-imovel/eusebio-ce'
        create_n_save_df(website)
    elif input_command == 2:
        dataframe = pd.read_excel('output\leilaoimoveis.xlsx')
        plot_map(dataframe, 'fortaleza-ce')



if __name__ == '__main__':
    main()
