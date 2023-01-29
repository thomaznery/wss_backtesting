from backtesting import Backtest
from scripts.consecutivas import ConsecutivasAltas, ConsecutivasQuedas
from dados.ibov import ibov_composicao, ibov_composicao_random



#rodar para varios ativos
ativos = ibov_composicao_random(3)
screening = Backtest(ativos, ConsecutivasQuedas())
screen = screening.historical_test()
print(screen)


