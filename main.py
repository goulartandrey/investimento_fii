import requests
import locale
from tabulate import tabulate
from bs4 import BeautifulSoup
from models import FundoImobiliario, Strategy

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def trata_porcentagem(porcentagem_str):
    return locale.atof(porcentagem_str.split('%')[0])

def trata_decimal(decimal_str):
    return locale.atof(decimal_str)

headers = {'User-Agent': 'Mozilla/5.0'}

resposta = requests.get('https://www.fundamentus.com.br/fii_resultado.php', headers=headers)

soup = BeautifulSoup(resposta.text, 'html.parser')

rows = soup.find(id='tabelaResultado').find('tbody').find_all('tr')

result = []

strategy = Strategy(max_price=40, min_dy=6, max_pvp=1.2, min_liquidity=30000)

for row in rows:
    data_fii = row.find_all('td')
    fii_code = data_fii[0].text
    fii_segment = data_fii[1].text
    fii_price = trata_decimal(data_fii[2].text)
    fii_dy = trata_porcentagem(data_fii[4].text)
    fii_pvp = trata_decimal(data_fii[5].text)
    fii_liquidity = trata_decimal(data_fii[7].text)

    fii = FundoImobiliario(fii_code, fii_segment, fii_price, fii_dy, fii_pvp, fii_liquidity)

    if strategy.aply_strategy(fii):
        result.append(fii)

headers = ['CÓDIGO', 'SEGMENTO', 'COTAÇÃO', 'DY', 'P/VP']

final_table = []

for fund in result:
    final_table.append([fund.code, fund.segment, locale.currency(fund.price), f'{locale.str(fund.dy)} %', fund.pvp])

print(tabulate(final_table, headers=headers, tablefmt='fancy_grid', showindex='always'))