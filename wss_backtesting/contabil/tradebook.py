from datetime import datetime
import inspect
import numpy as np 
import pandas as pd 
from math_helper import MathHelper

class Trade():
    def __init__(self,data:datetime , tipo:str, ativo:str, valor:float, qntd=1000, isStop=False) -> None:                
        self.data = data
        self.tipo = tipo
        self.ativo =  ativo
        self.valor = valor
        self.quantidade = qntd if tipo == "COMPRA" else qntd*-1
        self.isStop = isStop
    
    def __repr__(self):
        return "{}, {}, {}, {}, {}".format(self.tipo, self.ativo, self.valor, self.quantidade, self.data)
    
    def toSeries(self):
        return pd.Series(data=self.__dict__.values(), index=self.__dict__.keys())

class TradeBook():
    def __init__(self) -> None:
        self.trades = []          

    #sera ignorado sinais de compra ou vendas repetidos(mesmo tipo)
    def add_trade(self, trade:Trade): 
        if 0 != len(self.trades):
            if self.trades[len(self.trades)-1].tipo == trade.tipo:
                pass
            else:
                self.trades.append(trade)
        else:
            self.trades.append(trade)                                

    ##agrupar por ativo
    #Verifica se existe operacoes abertas retornando n < 0 para posição vendida e n > 0 para posição comprada
    def posicao(self):                        
        qntds = []
        for t in self.trades:
            qntds.append(t.quantidade)        
        return sum(qntds)

    #considera como tipo de operação, a operação do primeiro trade incluido                    
    def gerar_operacoes(self):        
        trades = self.trades           
        cols=["Start", "End", "Tipo","Entrada","Saida","Lucro"]
        mh = MathHelper()     
        df = pd.DataFrame(columns=cols)        
        for index in range(0, len(trades)-1, 2):                       
            var = mh.variation(trades[index].valor, trades[index+1].valor)
            if trades[index].tipo == "VENDA": var = var*-1            
            
            df.loc[index] = pd.Series( 
                data=[trades[index].data, 
                      trades[index+1].data, 
                      trades[index].tipo,
                      trades[index].valor,
                      trades[index+1].valor,
                      var],
                index=cols)  
        df.index = range(0, len(df.index))
        return df

    def clean(self):
        list.clear(self.trades)

    def isComprado(self) -> bool:
        if not self.trades: return False
        return self.trades[len(self.trades)-1].tipo == "COMPRA"
    
    def lst_value(self) -> float:
        
        return self.trades[len(self.trades)-1].valor
    
    def get_dataframe_trades(self):
        df = pd.DataFrame(columns=list(self.trades[0].__dict__.keys()))
        for index,t in enumerate(self.trades):
            df.loc[index] = t.toSeries()
        return df
        
    
            
            