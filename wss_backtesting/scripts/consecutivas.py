import pandas as pd
from math_helper import MathHelper
from contabil.tradebook import TradeBook,Trade
from scripts.IEstrategia import IEstrategia

"""A estratégia efetua uma venda após n dias consecutivos de alta no papel, zerando a posição
    no fechamento do mesmo dia
"""
class ConsecutivasAltas(IEstrategia):
    def __init__(self) -> None:
        self.tradeBook:TradeBook = TradeBook()

    def execute(self, eq:str, df:pd.DataFrame, dias_consec = 7):
        helper = MathHelper()
        dias_consecutivos_alta = dias_consec
        count_altas = 0
        tradeNextDay = False
        for index in range(1,len(df.index)):
            if tradeNextDay:
                self.tradeBook.add_trade(Trade(df.loc[index].Data, tipo="VENDA",ativo=eq, valor=df.loc[index].Open))                                
                self.tradeBook.add_trade(Trade(df.loc[index].Data, tipo="COMPRA",ativo=eq, valor=df.loc[index].Close))
                count_altas=0

            var = helper.variation(df.loc[index-1].Close, df.loc[index].Close)##variaçao do fechamento de D-1 ao fechamento corrente(index)
            count_altas = count_altas+1 if var > 0 else  0
            tradeNextDay =  count_altas == dias_consecutivos_alta
        return self.tradeBook.gerar_operacoes()



"""A estratégia efetua uma compra após n dias consecutivos de baixa no papel, zerando a posição no 
    fechamento do mesmo dia 
"""
class ConsecutivasQuedas(IEstrategia):
    def __init__(self) -> None:
        self.tradeBook:TradeBook = TradeBook()

    def execute(self, eq:str, df:pd.DataFrame, dias_consec = 7):
        helper = MathHelper()
        dias_consecutivos_queda = dias_consec
        count_quedas = 0
        tradeNextDay = False
        for index in range(1,len(df.index)):
            if tradeNextDay:
                self.tradeBook.add_trade(Trade(df.loc[index].Data, tipo="COMPRA",ativo=eq, valor=df.loc[index].Open))                                
                self.tradeBook.add_trade(Trade(df.loc[index].Data, tipo="VENDA",ativo=eq, valor=df.loc[index].Close))
                count_quedas=0

            var = helper.variation(df.loc[index-1].Close, df.loc[index].Close)##variaçao do fechamento de D-1 ao fechamento corrente(index)
            count_quedas = count_quedas+1 if var < 0 else  0
            tradeNextDay =  count_quedas == dias_consecutivos_queda
        return self.tradeBook.gerar_operacoes()

   
    