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
import json

sns.set(context='talk', style='whitegrid', color_codes=True)
# sns.set_palette("Blues")

dirpath = os.getcwd()


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
            close = close.join(df_temp, how='outer', rsuffix= '_double')
        except FileNotFoundError:
            print('ticker not found: ' + stock)
#            df_temp = pd.DataFrame(data= np.zeros(6940,), 
#                                   index = pd.date_range(pd.datetime(2000, 1, 1), 
#                                                         pd.datetime(2018, 12, 31)),
#                                   columns = [stock + '_close'])
    return close

with open('sp500-historical-components_no_weighting.json') as data:
    data = json.load(data)
    time_stamps = []
    symbols = []
    for sp_comp in data:
        time_stamps.append(sp_comp['Date'])
        symbols.append(sp_comp['Symbols'])        
    
sp500_comp_df = pd.DataFrame(index = pd.to_datetime(time_stamps),
                             data = symbols)
sp500_comp_df.sort_index()

stocks_2017_04_28 = read_stocks_txt_to_df(sp500_comp_df.loc['2017-04-28'].dropna(1).values[0][:50])    

sp500_close = pd.read_csv(dirpath + '\\spx.csv', sep=',', index_col ='date', parse_dates=True)

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
stocks_2017_04_28_portfolio = stocks_2017_04_28.filter(regex='.+close', 
                                      axis=1).pct_change()

start_date = '2011-01-31'
end_date = '2012-01-30'

stocks_2011_01_31 = read_stocks_txt_to_df(sp500_comp_df.loc['2011/01/31'].dropna(1).values[0])
stocks_2011_01_31_return = stocks_2011_01_31.loc['2011-01-31':'2013-01-30'].dropna(1).filter(regex='(.+close)', 
                                      axis=1).pct_change()
stocks_2011_01_31_performance = (stocks_2011_01_31_return +1).cumprod() 

benchmark = (sp500_close.loc['2011-01-31':'2013-01-30'].pct_change()+1).cumprod()
stocks_2011_01_31_performance = (stocks_2011_01_31_return +1).cumprod()

vs_benchmark_date = benchmark.index[-1]
stocks_vs_bench = stocks_2011_01_31_performance.loc[\
        vs_benchmark_date, :] > benchmark.loc[vs_benchmark_date][0]
stocks_vs_bench.to_csv('returns_with_benchmark\\VSbench.csv')

(stocks_2011_01_31.loc['2011-01-31':'2012-01-31'].dropna(1).filter(regex='(.+close)', 
      axis=1).pct_change() +1).cumprod().to_csv('returns_with_benchmark\\returns.csv')

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
#
#import os
#if not os.path.exists(directory):
#    os.makedirs(directory)


