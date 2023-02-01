from scripts.IEstrategia import IEstrategia
from contabil.tradebook import TradeBook,Trade
import pandas as pd
from indicadores.indicadores_at import boiller_bands
from math_helper import MathHelper

class BoillerB(IEstrategia):
    def __init__(self) -> None:
        self.tradeBook:TradeBook = TradeBook()

    ##gerar os trades
    def execute(self,ativo:str, cotacoes:pd.DataFrame, verbose:bool=False):
        mh = MathHelper()
        cotacoes = boiller_bands(cotacoes=cotacoes, periodo=40)
        cotacoes['Variation'] = cotacoes['Close'].diff()

        #media exponencias de 20 periodos usada no stop
        cotacoes['EMA20'] = cotacoes["Close"].ewm(span=20).mean()

        for index,row in cotacoes.iterrows():            
                
            #violinada nas bandas inferiores, compra no preco das bandas
            if cotacoes.loc[index].Low < cotacoes.loc[index].BB_inf and cotacoes.loc[index].Close > cotacoes.loc[index].BB_inf:
                self.tradeBook.add_trade(Trade(cotacoes.loc[index].Date, "COMPRA", ativo, cotacoes.loc[index].Close))
                continue                

            if cotacoes.loc[index].High > cotacoes.loc[index].EMA20:
                if len(self.tradeBook.trades) > 0:
                    self.tradeBook.add_trade(Trade(cotacoes.loc[index].Date, "VENDA", ativo, cotacoes.loc[index].EMA20))
                    continue

            if self.tradeBook.isComprado(): 
                stop = self.tradeBook.lst_value() - (self.tradeBook.lst_value()*0.03)
                if (cotacoes.loc[index].Open < stop or cotacoes.loc[index].Close < stop):
                    if mh.inRange(cotacoes.loc[index].Open, cotacoes.loc[index].Close, stop):
                        self.tradeBook.add_trade(Trade(cotacoes.loc[index].Date, "VENDA", ativo, stop, isStop=True))                        
                    elif cotacoes.loc[index].Open < stop:
                        ##estopar na abertura se abrir com gap abaixo do stop
                        self.tradeBook.add_trade(Trade(cotacoes.loc[index].Date, "VENDA", ativo, cotacoes.loc[index].Open, isStop=True))

        return self.tradeBook.gerar_operacoes()
    