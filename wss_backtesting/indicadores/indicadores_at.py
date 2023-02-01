import pandas as pd
import numpy as np

def rsi(cotacoes:pd.DataFrame, periodo=20) -> pd.DataFrame:
    cotacoes['Variation'] = cotacoes['Close'].diff()        
    cotacoes = cotacoes[1:]
    
    cotacoes.loc[cotacoes['Variation'] > 0, 'positive'] =  cotacoes['Variation']
    cotacoes.loc[cotacoes['Variation'] < 0, 'positive'] =  0
    
    cotacoes.loc[cotacoes['Variation'] < 0, 'negative'] =  cotacoes['Variation']
    cotacoes.loc[cotacoes['Variation'] > 0, 'negative'] =  0
    
    simple_avg_gain = cotacoes['positive'].rolling(periodo).mean()
    simple_avg_loss = cotacoes['negative'].abs().rolling(periodo).mean()
    cotacoes['RS'] = simple_avg_gain / simple_avg_loss
    cotacoes['RSI'] = 100 - (100 / (1 + cotacoes['RS']))
        
    cotacoes = cotacoes.drop(columns=['positive', 'negative', 'RS'])
    cotacoes.dropna(inplace=True)
    return cotacoes

def boiller_bands(cotacoes:pd.DataFrame, periodo=20) -> pd.DataFrame:
    column_mm = 'MM'+str(periodo)
    cotacoes[column_mm] = cotacoes["Close"].rolling(periodo).mean()
    desvio_padrao = np.std(cotacoes["Close"].tail(periodo))    
    cotacoes["BB_sup"] = cotacoes[column_mm] + (2*desvio_padrao)
    cotacoes["BB_inf"] = cotacoes[column_mm] - (2*desvio_padrao)
    cotacoes.drop(columns=[column_mm])
    cotacoes.dropna(inplace=True)        
    return cotacoes

def estocastico_rapido(cotacoes:pd.DataFrame, periodo = 8) -> pd.DataFrame:
    n_highest_high = cotacoes["High"].rolling(periodo).max()
    n_lowest_low = cotacoes["Low"].rolling(periodo).min()
    cotacoes['estoc_rapido'] = ((cotacoes['Close'] - n_lowest_low) /(n_highest_high - n_lowest_low))*100
    cotacoes.dropna(inplace=True)
    return cotacoes

def estocastico_lento(cotacoes:pd.DataFrame, periodo = 8) -> pd.DataFrame:
    import matplotlib.pyplot as plt
    cotacoes = estocastico_rapido(cotacoes)
    cotacoes["%D"] = cotacoes['estoc_rapido'].rolling(3).mean()
    cotacoes["estoc_rapido"] = cotacoes["%D"]
    cotacoes["estoc_lento"] = cotacoes["estoc_rapido"].rolling(3).mean()
    cotacoes.dropna(inplace=True)
    return cotacoes
