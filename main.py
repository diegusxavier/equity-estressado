from src.choses import *
import warnings

def main():
    # desativa todos os warnings
    warnings.filterwarnings("ignore")

    # inicia o prompt perguntando o que fazer
    while True:
        print('----\nQual operação você deseja realizar?\n  1 - Extrair dados de um site\n  2 - Fazer mapeamento dos imóveis da região\n  3 - Concatenar planilhas\n  4 - Extrair dados da OLX\n')
        input_command = int(input('Escolha o número da operação desejada: '))
        if input_command in list(range(1, 5)):
            break
        else:
            print('----\nDIGITE UM NÚMERO VÁLIDO!')
    if input_command == 1:
        chose_extract_data()
    elif input_command == 2:
        chose_plot_map()
    elif input_command == 3:
        chose_concat_df()
    elif input_command == 4:
        chose_extract_olx()


if __name__ == '__main__':
    while True:
        main()
        answer = input('Deseja fazer mais alguma operação? [y/n] ').upper()
        if answer != 'Y':
            break
