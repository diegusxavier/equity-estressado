![Static Badge](https://img.shields.io/badge/Python-yellow?logo=python) ![Static Badge](https://img.shields.io/badge/web%20Scraping-green)  ![Static Badge](https://img.shields.io/badge/automation-red) ![Static Badge](https://img.shields.io/badge/Folium-brown)




# Equity Estressado

Projeto de automação do processo de extração de dados de sites (web scraping) de leilão de imóveis utilizando Python e a biblioteca Selenium. Os dados são salvos em planilhas em formato `.xlsx` e o mapeamento da região dos imóveis é salvo em formato `.html`.

No presente momento, o programa é configurado apenas para realizar a extração de apenas um site [serão adicionados mais sites em breve].

## Como utilizar

1 - Baixe o navegador Firefox e salve-o na pasta padrão de instalação. O Chrome está com um problema de versão.
    (Caso o Firefox esteja em outra localização, modifique a linha 11 de [scraping_leilaoimovel.py](./src/scraping/scraping_leilaoimovel.py) com o caminho desejado)
2 - Execute o arquivo main.exe. Será aberto a janela preta do Terminal. Aguarde até aparecerem as opções de intruções.
    (Caso o antivírus alerte, permita que o programa execute)
3 - Leia as instruções que aparece na tela do Terminal e execute as operações desejadas.
    (Você pode fechar o terminal para cancelar uma instrução dada errada e está em execução)
4 - Você pode minimizar a janela do Firefox e do Terminal enquando roda algum processo
5 - Verifique os arquivos gerados na pasta output e nas subpastas presentes.

### Extração dos dados
- Dependendo da quantidade de dados, o processo pode ser demorado porque não está otimizado para ultilizar o multithreading [ideia de melhorias futuras].
Entretanto, pode minimizar as telas enquanto o programa roda em segundo plano.
- É possível que haja algum erro caso seja alterado a estrutura do site ou o programa tente entrar em um site em que a estrutura do anúncio é diferente.
- O formato para escolher quais cidades vão ser extraídas são as seguintes:
    cidade-uf: tudo em letra minúsculo e sem assento. Caso seja nome composto, separe por hífen.
        -> Exemplo 1: eusebio-ce
        -> Exemplo 2: sao-paulo-sp
- Para extrair de múltiplas cidades, separe-as com espaços. Seja feito uma planilha para cada cidade.
        -> Exemplo 1: fortaleza-ce aquiraz-ce eusebio-ce maracanau-ce

### Mapeamento
- O mapeamento é um processo rápido e vai gerar mapas em arquivos `.html`, que podem ser abertos em quaisquer navegador.
- O mapeamento recebe uma planilha como parâmetro, ou seja, você só vai poder mapear as regiões em que houve extração de dados e a planilha está presente em sua respectiva pasta.
- Basta apenas digitar o número referente a planilha para fazer o mapeamento.
    Diferentemente da extração de dados, nessa função você não pode tentar digitar mais de um número para o mapeamento [ideia de melhorias futuras].
- Para o mapeamento de uma região que englobe mais de um município, deve-se fazer a concatenação/união das planilhas antes.
- Caso o endereço não seja encontrado, será anotado um link no arquivo output\outros\endereco_nao_encontrado.txt. Esse arquivo é resetado a cada mapeamento.

### Concatenação de planilhas
- Basta digitar os números, separados por espaços, referentes as planilhas que você quer concatenar. A nova planilha unificada será nomeada com todas as cidades escolhidas.
- Não digite números repetidos.


## Avisos importantes
- No diretório atual, não modifique o nome nem o endereço de nenhuma das pastas contidas nele.
- Não modifique nenhum dos arquivos com as extensões `.py`, `.txt`, `.exe`, `.md`, `.xlsx`.
- Você pode recortar arquivos das pastas output/planilhas e output.mapas e movê-los para outras pastas (que não seja desse diretório).
- Caso queira o arquivo endereco_nao_encontrado.txt, copie e cole-o onde deseja. Não remova o arquivo da pasta.
- Você pode adicionar novas planilhas à pasta output/planilhas, mas deve tomar a seguinte precaução:
    - As colunas devem ser idênticas e a formatação e a coluna 'Valor do Imóvel' deve corresponder a um tipo int ou float.
