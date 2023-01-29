from contabil.tradebook import Trade,TradeBook
from scripts.consecutivas import ConsecutivasAltas, ConsecutivasQuedas
import pandas as pd
import yfinance as yf
from datetime import date
from scripts.IEstrategia import IEstrategia

yf.pdr_override()
class Backtest():
    def __init__(self, ativos:list, estrategia:IEstrategia):
        self.ativos = ativos    
        self.estrategia:IEstrategia = estrategia
        self.screen_cols=["ativo", "rentab", "n_operacoes" , "n_gain", "n_loss", "maior_gain", "maior_loss"]
        self.df_screen = pd.DataFrame(columns=self.screen_cols)

    def historical_test(self) -> pd.DataFrame:
        estrate:IEstrategia = self.estrategia
        for id, ativo in enumerate(self.ativos, start=0):            
            cotacoes:pd.DataFrame = yf.download(ativo, start=date(2000,1,1),  auto_adjust=True, interval="1d")
            cotacoes['Data'] = cotacoes.index
            cotacoes.index = range(0, len(cotacoes.index))

            df_operacoes:pd.DataFrame = estrate.execute(ativo, cotacoes)

            positive_cont = 0
            negative_cont = 0
            for index in df_operacoes.index.values:
                if df_operacoes.loc[index].Lucro > 0: 
                    positive_cont+=1 
                    
                if df_operacoes.loc[index].Lucro < 0: 
                    negative_cont+=1

            ##linha gerada
            infos = {
                    self.screen_cols[0]:ativo, 
                    self.screen_cols[1]:df_operacoes['Lucro'].sum(),
                    self.screen_cols[2]:sum([positive_cont,negative_cont]), 
                    self.screen_cols[3]:positive_cont, 
                    self.screen_cols[4]:negative_cont,
                    self.screen_cols[5]:df_operacoes['Lucro'].max(),
                    self.screen_cols[6]:df_operacoes['Lucro'].min()
                    }
            
            self.df_screen.loc[id] = pd.Series(data=infos, index=infos.keys())
            list.clear(estrate.tradeBook.trades)
        return self.df_screen
        
        

        
    
    

