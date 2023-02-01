import pandas as pd
import yfinance as yf
from scripts.IEstrategia import IEstrategia
from visualization.historical_test import plt_historical_test
from statistics import mean


yf.pdr_override()
class Backtest():
    def __init__(self, ativos:list, estrategia:IEstrategia):
        self.ativos = ativos    
        self.estrategia:IEstrategia = estrategia
        self.screen_cols=["ativo", "rentab", "n_operacoes" , "n_gain", "n_loss", "maior_gain", "maior_loss"]
        self.df_screen = pd.DataFrame(columns=self.screen_cols)

    def historical_test(self, verbose=False) -> pd.DataFrame:
        estrate:IEstrategia = self.estrategia
        for id, ativo in enumerate(self.ativos, start=0):                        
            cotacoes:pd.DataFrame = yf.download(ativo, period="3y",  auto_adjust=True, interval="1d")
            
            cotacoes.reset_index(inplace=True)  
            
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
            if verbose:
                
                df_infos = pd.DataFrame(columns=['sumary', str(id)])
                
                rent_acumulada_axies = self.get_rent_acumulada_historico(df_operacoes)                
                self.backtest_info_add(df_infos, "Stat Period", cotacoes.loc[cotacoes.index[0]].Date.strftime('%d/%m/%Y'))
                self.backtest_info_add(df_infos, "End Period", cotacoes.loc[cotacoes.index[len(cotacoes.index.values)-1]].Date.strftime('%d/%m/%Y'))
                self.backtest_info_add(df_infos, "Rentab Acumul.", rent_acumulada_axies[len(rent_acumulada_axies)-1])
                self.backtest_info_add(df_infos, "Max Drawdown", min(rent_acumulada_axies))
                self.backtest_info_add(df_infos, "Max Rent", max(rent_acumulada_axies))
                self.backtest_info_add(df_infos, "Volatility Mean", mean(rent_acumulada_axies))
                self.backtest_info_add(df_infos, "Best Day", max(df_operacoes["Lucro"]))
                self.backtest_info_add(df_infos, "Worst Day", min(df_operacoes["Lucro"]))
                self.backtest_info_add(df_infos, "Gains Count", df_operacoes.query("Lucro > 0")['Lucro'].count())
                self.backtest_info_add(df_infos, "Losses Count", df_operacoes.query("Lucro < 0")['Lucro'].count())
                
                print(df_infos)
                            
            self.df_screen.loc[id] = pd.Series(data=infos, index=infos.keys())
            list.clear(estrate.tradeBook.trades)
            
        return self.df_screen
        
    def get_rent_acumulada_historico(self, operacoes:pd.DataFrame) ->list:
        acum = [0]
        for index, item in enumerate(operacoes['Lucro'].values):
            acum.append(acum[index]+item)                
        return acum

    def backtest_info_add(self, *kwargs): 
        ##adiciona uma linha no data frame, considerando as colunas de df_infos
         kwargs[0].loc[len(kwargs[0].index.values)] \
                    = (pd.Series(
                        data=[kwargs[1], kwargs[2]], 
                        index=kwargs[0].columns.values))
        

        
    
    

