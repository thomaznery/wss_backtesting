import pandas as pd
import numpy as np
import random

def ibov_composicao() -> list:
    ##fonte https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-ibovespa-ibovespa-composicao-da-carteira.htm
    f = open('./dados/IBOVDia_30-01-23.csv', 'r', encoding='latin-1')
    ativos = []
    for line in f:
        ativos.append(line.split(";")[0])
    del ativos[0]
    del ativos[0]
    del ativos[-1]
    del ativos[-1]
    
    for index,a in enumerate(ativos):
        ativos[index] = ativos[index]+".SA"
    return ativos

def ibov_composicao_random(n:int) -> list:
    ativos = ibov_composicao()
    randoms = []
    for eq in range(0,n):
        randoms.append(ativos[random.randint(0,len(ativos))])
    return randoms