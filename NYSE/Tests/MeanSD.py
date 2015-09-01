#Tests a pair with CADF and Hurst and outputs key data for the time period selected

# -*- coding: utf-8 -*-
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pandas.io.data as web
import statsmodels.tsa.stattools as ts
from pandas.stats.api import ols
import math

def plot_price_series(df, ts1, ts2,start,end):
    months = mdates.MonthLocator() # every month
    fig, ax = plt.subplots()
    ax.plot(df.index, df[ts1], label=ts1)
    ax.plot(df.index, df[ts2], label=ts2)
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.set_xlim(start,end)
    ax.grid(True)
    fig.autofmt_xdate()
    plt.xlabel('Month/Year')
    plt.ylabel('Price ($)')
    plt.title('%s and %s Daily Prices' % (ts1, ts2))
    plt.legend()
    plt.show()

def plot_residuals(df,start,end):
    months = mdates.MonthLocator() # every month
    fig, ax = plt.subplots()
    ax.plot(df.index, df["res"], label="Residuals")
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.set_xlim(start,end)
    ax.grid(True)
    fig.autofmt_xdate()
    plt.xlabel('Month/Year')
    plt.ylabel('Price ($)')
    plt.title('Residual Plot')
    plt.legend()
    plt.plot(df["res"])
    plt.show()

def run_test(stock1,stock2,start,end,length=200,full=False,s1=None,s2=None):
    if full:
        print('CADF')
        print ' '
    
    first = web.DataReader(stock1, "yahoo", start, end)
    second = web.DataReader(stock2, "yahoo", start, end)
    df = pd.DataFrame(index=first.index)
    df[stock1] = first["Adj Close"]
    df[stock2] = second["Adj Close"]
    if full:
        plot_price_series(df, stock1, stock2,start,end)    
    
    res = ols(y=df[stock2], x=df[stock1])
    beta_hr = res.beta.x
    if full:
        temp = 'Beta = ' + str(beta_hr)
        print temp
        temp = 'EQN: ' + stock2 + ' - ' + str(beta_hr) + '*' + stock1
        print temp
        print ' '
    
    df["res"] = df[stock2] - beta_hr*df[stock1]
    df['MA'] = 0.000

    counter = length
    total = 0
    try:
        for i in range(length):
            total += df['res'][i]
        mean = total/length
        for i in range(length):
            df['MA'][i] = mean
    except:
        print 'Not enough data points'
    
    while counter < len(df['res']):
        total -= df['res'][counter-length]
        total += df['res'][counter]
        mean = total/length
        df['MA'][counter] = mean
        counter += 1

    total = 0
    counter = 0
    while counter < len(df['res']):
        total += df['res'][counter]
        counter += 1
        
    mean = total/counter
    df['mean'] = mean
    
    counter = 0
    total = 0
    while counter < len(df['res']):
        total += (df['res'][counter]-mean)**2
        counter += 1
    var = total/counter
    sd = math.pow(var,0.5)
    
    if full:
        temp = 'Mean = ' + str(mean)
        print temp
        temp = 'SD = ' + str(sd)
        print temp
        print ' '
    
    df['sd1'] = df['mean'] + sd
    df['sd2'] = df['mean'] + 3*sd
    df['sd3'] = df['mean'] + -1*sd
    df['sd4'] = df['mean'] + -3*sd
    df['sd5'] = df['mean'] + 0.5*sd
    df['sd6'] = df['mean'] + -0.5*sd
    curr = 0
    
    if s1!=None and s2!=None:
        curr = s2-beta_hr*s1
        df['curr'] = curr
    
    if full:
        months = mdates.MonthLocator() # every month
        fig, ax = plt.subplots()
        ax.plot(df.index, df["res"], label="Residuals")
        temp = str(length) + 'DMA'
#        ax.plot(df.index, df["MA"], label=temp)
        ax.plot(df.index, df["mean"],'k')
        ax.plot(df.index, df["sd1"],'r--')
        ax.plot(df.index, df["sd2"],'r--')
        ax.plot(df.index, df["sd3"],'r--')
        ax.plot(df.index, df["sd4"],'r--')
        ax.plot(df.index, df["sd5"],'c--')
        ax.plot(df.index, df["sd6"],'c--')
        if curr != 0:
            ax.plot(df.index, df["curr"],'m')
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.set_xlim(start,end)
        ax.grid(True)
        fig.autofmt_xdate()
        plt.xlabel('Month/Year')
        plt.ylabel('Price ($)')
        plt.title('Residual Plot')
        plt.legend()
        plt.plot(df["res"])
        plt.show()
    
    cadf = ts.adfuller(df["res"])
    if full:
        print cadf
        print('')
    
    test = cadf[0]
    crit = cadf[4]
    one = crit['1%']
    five = crit['5%']
    ten = crit['10%']

    hurst(df["res"],full) 
    
    return df
    
def hurst_calc(ts):
    lags = range(2, 100)
    
    tau = [np.sqrt(np.std(np.subtract(ts[lag:], ts[:-lag]))) for lag in lags]
    
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    
    return poly[0]*2.0
    
def hurst(ts,full):
    if full:    
        print('Hurst')
    
    gbm = np.log(np.cumsum(np.random.randn(100000))+1000)
    mr = np.log(np.random.randn(100000)+1000)
    tr = np.log(np.cumsum(np.random.randn(100000)+1)+1000)

    if full:    
        print "Hurst(GBM(Random)): %s" % hurst_calc(gbm)
        print "Hurst(MeanReverting): %s" % hurst_calc(mr)
        print "Hurst(Trending): %s" % hurst_calc(tr)
    
        print "Hurst: %s" % hurst_calc(ts)
        print('-----------------------------------------')
    else:
        result = {}
        result['GBM'] = hurst_calc(gbm)
        result['MR'] = hurst_calc(mr)
        result['TR'] = hurst_calc(tr)
        result['Hurst'] = hurst_calc(ts)

start = datetime.datetime(2014, 5, 7)
end = datetime.datetime(2015, 5, 7)  
s1 = 'BMY'
s2 =  'CERN'
temp = run_test(s1,s2,start,end,full=True)

#temp2 =run_test('PNC','STI',start,end,full=True)

#a = open('C:\Users\Daniel\Desktop\MR\BMYCERN\P.csv','w')
#row = csv.writer(a)

#for i in range(400,1000):
#    row.writerow([temp['BMY'][i],temp['CERN'][i],temp['res'][i],temp['MA'][i]])
    
#a.close()