from stocksymbol import StockSymbol
import pandas as pd
import numpy as np

api_key = '33b2a486-0d39-4c66-a28f-bebca5a151d6'
ss = StockSymbol(api_key)
##https://pypi.org/project/stocksymbol/
brazil_equitys = pd.DataFrame(ss.get_symbol_list(market="BR"))

np.savetxt("./equitys.txt", brazil_equitys.values, fmt='%s %s %s %s %s %s', delimiter=";")



