#Runs ADF and Hurst test on a single stock to test for mean reversion properties

import statsmodels.tsa.stattools as ts

from datetime import datetime
from pandas.io.data import DataReader

from numpy import cumsum, log, polyfit, sqrt, std, subtract
from numpy.random import randn

def ADF(ticker,start,end):
    print('ADF')
    
    stock = DataReader(ticker, "yahoo", start, end)
    
    result = ts.adfuller(stock['Adj Close'], 1)
    print(result)
    print('')
    
    test = result[0]
    crit = result[4]
    one = crit['1%']
    five = crit['5%']
    ten = crit['10%']
    
    if test<one:
        print('Lesser than 1%')
        print('-----------------------------------------')
        return stock
        
    if test<five:
        print('Lesser than 5%')
        print('-----------------------------------------')
        return stock
        
    if test<ten:
        print('Lesser than 10%')
        print('-----------------------------------------')
        return stock
        
    print('Cannot reject Null Hypothesis')
    print('-----------------------------------------')
    return stock
    
def hurst_calc(ts):

    lags = range(2, 100)
    
    tau = [sqrt(std(subtract(ts[lag:], ts[:-lag]))) for lag in lags]
    
    poly = polyfit(log(lags), log(tau), 1)
    
    return poly[0]*2.0
    
def hurst(ts):
    print('Hurst')
    
    gbm = log(cumsum(randn(100000))+1000)
    mr = log(randn(100000)+1000)
    tr = log(cumsum(randn(100000)+1)+1000)
    
    print "Hurst(GBM(Random)): %s" % hurst_calc(gbm)
    print "Hurst(MeanReverting): %s" % hurst_calc(mr)
    print "Hurst(Trending): %s" % hurst_calc(tr)
    
    print "Hurst: %s" % hurst_calc(ts['Adj Close'])
    print('-----------------------------------------')
    
def runtests(stock):
    price = ADF(stock,datetime(2000,1,1), datetime(2013,1,1))
    hurst(price)
    
if __name__ == "__main__":
    price = ADF('JPM',datetime(2000,1,1), datetime(2013,1,1))
    hurst(price)
    
    
    
    

    