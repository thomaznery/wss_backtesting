from backtesting import Backtest
from scripts.consecutivas import ConsecutivasAltas, ConsecutivasQuedas
from scripts.boillerbands import BoillerB
from dados.ibov import ibov_composicao, ibov_composicao_random
import pandas as pd
import yfinance as yf
from datetime import date
from indicadores.indicadores_at import *


#rodar para varios ativos
#ativos = ibov_composicao_random(5)
ativos = ['vale3.sa']
screening = Backtest(ativos, BoillerB())
screen = screening.historical_test(verbose=True)



"""cotacoes:pd.DataFrame = yf.download('vale3.sa', start=date(2022,1,1),  auto_adjust=True, interval="1d")
cotacoes['Data'] = cotacoes.index
cotacoes.index = range(0, len(cotacoes.index))

print(estocastico_rapido(cotacoes))"""







