# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 11:52:43 2019

@author: philipp.merz
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns

sns.set(context='talk', style='whitegrid', color_codes=True)
# sns.set_palette("Blues")

dirpath = os.getcwd()


#stock_data = dirpath + '\\Stocks\\'

#aapl = pd.read_csv(stock_data+ r'aapl.us.txt', sep=',', index_col='Date', prefix='aapl_')
#aapl.columns = ['aapl_' + i for i in aapl.columns]
# sp500 composition

def read_stocks_txt_to_df(stock_list):
    path = os.getcwd() + '\\Stocks\\'
    close = pd.DataFrame()
    stock_list = list(stock_list)
    for stock in stock_list:
        try:
            df_temp = pd.read_csv(path+ stock.lower() + '.us.txt',
                              sep=',', 
                              index_col='Date',
                              parse_dates = True)
            df_temp.columns = [stock + '_' + i.lower() for i in df_temp.columns]
        except FileNotFoundError:
            df_temp = pd.DataFrame(data= np.zeros(6940,), 
                                   index = pd.date_range(pd.datetime(2000, 1, 1), 
                                                         pd.datetime(2018, 12, 31)),
                                   columns = [stock + '_close'])
        
        close = close.join(df_temp, how='outer')
    return close


sp500_close = pd.read_csv(dirpath + '\\spx.csv', sep=',', index_col ='date', parse_dates=True)
sp500_close
# discrete or percentile change, why not log change?
#aapl['Return'] = aapl['aapl_Close'].pct_change()
# pl.hist(aapl['Return'].dropna(), bins = 75)
#aapl_stats = ( np.mean(aapl['Return']), np.std(aapl.Return) )

sp500_2004_leading_stocks = ["AAPL","XOM","GAS",'BVLAL','EEKEKW','SKKWKW'] # tote stocks haben keine auswirkung
#['acor', 'chscp', 'fslr']    waren die schrott ?? ,"GAS","MIL","MXA"
#["AAPL","XOM","GOOGL"]
#"GHC","MDP","AZO","ASH","SNA","R","RL"
sp500_2004_df = read_stocks_txt_to_df(sp500_2004_leading_stocks
                                      ).filter(regex='.+close', 
                                      axis=1).dropna(
                                              ).pct_change(
                                                      ).mean(axis=1) + 1
apple_vs_tote = read_stocks_txt_to_df(sp500_2004_leading_stocks)
sp500_2004_df[0] = 1                                      
# sp500_2004_df[0] = 1
sp_performance = sp500_close.pct_change().loc['2006':'2017']
sp_performance = sp_performance + 1
sp_performance = sp_performance.cumprod()
portfolio_performance = sp500_2004_df.loc['2006':'2017'].cumprod()
# cummultiplication
y = portfolio_performance#.join(sp_performance, how='left')
# plt.plot(y.index, y,sp_performance,  label = sp500_2004_leading_stocks )

fig, ax = plt.subplots()
ax.plot(y.index, y, label="portfolio")
ax.plot(sp_performance.index, sp_performance, label="sp500")
ax.set_xlabel(r"$time$")
ax.legend(loc="best") 
plt.show()


