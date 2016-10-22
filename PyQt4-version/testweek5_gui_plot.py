# -*- coding: utf-8 -*-
"""
@author: kidyhg1412@sina.com
"""

# Week 5 GUI Plot Data
from matplotlib.finance import quotes_historical_yahoo_ochl
from datetime import date
from datetime import datetime
import pandas as pd

###############################################################################
def PlotData(code, start, end, dlist):
    start_date = start
    end_date = end
    quotes = quotes_historical_yahoo_ochl(code, start_date, end_date)
    fields = ['date', 'open', 'close', 'high', 'low', 'volume']
    list1 = []
    for i in range(0, len(quotes)):
        x = date.fromordinal(int(quotes[i][0]))
        y = datetime.strftime(x, '%Y-%m-%d')
        list1.append(y)
    
    quotesdf = pd.DataFrame(quotes, index = list1, columns = fields)
    quotesdf = quotesdf.drop(['date'], axis = 1)
    quotesdftemp = pd.DataFrame()
 
    for i in range(0, len(dlist)):
        quotesdftemp[dlist[i]] = quotesdf[dlist[i]]

    quotesdftemp.plot(marker = 'o', grid = True, title = code)
