import urllib2
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
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
    
def plot_scatter_series(df, ts1, ts2):
    plt.xlabel('%s Price ($)' % ts1)
    plt.ylabel('%s Price ($)' % ts2)
    plt.title('%s and %s Price Scatterplot' % (ts1, ts2))
    plt.scatter(df[ts1], df[ts2])
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
    
def run_test(stock1,stock2,start,end,graph=False):
    print('CADF')
    
    df = get_data(stock1, stock2, start, end)
    
    res = ols(y=df[stock2], x=df[stock1])
    beta_hr = res.beta.x
    
    df["res"] = df[stock2] - beta_hr*df[stock1]       
    
    cadf = ts.adfuller(df["res"])
    
    test = cadf[0]
    crit = cadf[4]
    one = crit['1%']
    five = crit['5%']
    ten = crit['10%']
    
    print "Test Statistic: %s" % test
    temp = '1%: ' + str(one) + ' 5%: ' + str(five) + ' 10%: ' + str(ten)
    print(temp)
    print ' '
    
    if test<one:
        print('Confidence: 99%')      
    elif test<five:
        print('Confidence: 5%')        
    elif test<ten:
        print('Confidence: 10%')        
    else:
        print('Confidence: NIL')
        
    print "Beta: %s" % beta_hr
    print('-----------------------------------------')
        
    hurst(df["res"])   
    results = df["res"].tolist()
    counter = 1
    delta = []
    while counter < len(results):
        temp = results[counter] - results[counter-1]
        delta.append(temp)
        counter = counter + 1
    results.pop()
    
    half_life(delta,results)
    
    if graph == True:
        plot_price_series(df, stock1, stock2,start,end)    
        plot_scatter_series(df, stock1, stock2)
        plot_residuals(df,start,end)
    
    
def get_data(stock1,stock2,start,end):
    
    url = "http://ichart.finance.yahoo.com/table.csv?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s" % (stock1, start.day - 1, start.month, start.year, end.day - 1, end.month, end.year)
    data = urllib2.urlopen(url)
    
    dates = []
    close = []
    temp1 = []
    
    for i in data:
        temp = i.split(',')
        dates.append(temp[0])
        temp1.append(temp[6].strip())
        
    dates.reverse()
    dates.pop()
    
    counter = 0
    while counter < len(dates):
        dates[counter] = datetime.datetime.strptime(dates[counter], "%Y-%m-%d")
        counter = counter + 1

    temp1.reverse()
    temp1.pop()
    
    for i in temp1:
        close.append(float(i))
 
    df = pd.DataFrame(index=dates)
    df[stock1] = close

    close = []
    temp1 = []
    
    url = "http://ichart.finance.yahoo.com/table.csv?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s" % (stock2, start.day - 1, start.month, start.year, end.day - 1, end.month, end.year)
    data = urllib2.urlopen(url)
    
    for i in data:
        temp = i.split(',')
        temp1.append(temp[6].strip())
        
    temp1.reverse()
    temp1.pop()
    
    for i in temp1:
        close.append(float(i)) 
        
    df[stock2] = close
    
    return df

def hurst_calc(ts):
    lags = range(2, 100)
    
    tau = [np.sqrt(np.std(np.subtract(ts[lag:], ts[:-lag]))) for lag in lags]
    
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    
    return poly[0]*2.0
    
def hurst(ts):
    
    print('Hurst')
    
    gbm = np.log(np.cumsum(np.random.randn(100000))+1000)
    mr = np.log(np.random.randn(100000)+1000)
    tr = np.log(np.cumsum(np.random.randn(100000)+1)+1000)
    
    print "Hurst(GBM(Random)): %s" % hurst_calc(gbm)
    print "Hurst(MeanReverting): %s" % hurst_calc(mr)
    print "Hurst(Trending): %s" % hurst_calc(tr)
    
    print "Hurst: %s" % hurst_calc(ts)
    print('-----------------------------------------')
    
def half_life(delta,y):
    
    data = pd.DataFrame({'Delta':delta,'Y':y})
    results = ols(y=data['Delta'], x=data['Y'])
    halflife = -math.log(2)/results.beta.x
    
    print "HalfLife: %s" % halflife
    print('-----------------------------------------')
      
if __name__ == "__main__":
    start = datetime.datetime(2013, 1, 1)
    end = datetime.datetime(2015,1,1)
    run_test('Z77.SI','CC3.SI',start,end,True)
    