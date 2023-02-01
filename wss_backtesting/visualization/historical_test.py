import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import mplfinance as mpl
from mpl_finance import candlestick_ohlc




##TODO avaliar mostrar resultado somente em tabelas customizadas
def plt_historical_test(cotacoes:pd.DataFrame, df_operacoes:pd.DataFrame):  
    cotacoes = cotacoes.tail(len(cotacoes.index.values)-60)#dias dias plotado
    cotacoes.index = pd.to_datetime(cotacoes["Date"])   
        
    # Converting date into datetime format
    cotacoes['Date'] = pd.to_datetime(cotacoes['Date'])
    cotacoes['Date'] = cotacoes['Date'].apply(mpl_dates.date2num)
    cotacoes = cotacoes.astype(float)
    
    # Creating Subplots
    fig, ax = plt.subplots()
    fig.set_figwidth(15)
    fig.set_figheight(7)
    candlestick_ohlc(ax, cotacoes.values, width=0.4,
                    colorup='green', colordown='red', alpha=0.8)
    print(df_operacoes)
    fig.suptitle('Daily Candlestick Chart of NIFTY50')
    
    
    # Formatting Date
    date_format = mpl_dates.DateFormatter('%d-%m-%Y')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()
    
    fig.tight_layout()
    
    
    
        
