#Plots Price Series with Bollinger Bands

import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pandas.io.data as web
from pandas.stats.api import ols
from numpy import std
    
def run_test(stock1,stock2,start,end,lookback,n1,n2,p1=None,p2=None,MA1=10,MA2=3):

    first = web.DataReader(stock1, "yahoo", start, end)
    second = web.DataReader(stock2, "yahoo", start, end)
    df = pd.DataFrame(index=first.index)
    df[stock1] = first["Adj Close"]
    df[stock2] = second["Adj Close"]
    
    res = ols(y=df[stock2], x=df[stock1])
    beta_hr = res.beta.x
    
    df["res"] = df[stock2] - beta_hr*df[stock1]          
    
    results = df["res"].tolist()
    
    ma1 = []
    ma2 = []
    
    counter = MA1
    while counter <= len(results):
        sub = results[counter-MA1:counter]
        temp = sum(sub)/MA1
        
        if counter == MA1:
            for i in range(MA1-1):
                ma1.append(temp)
        ma1.append(temp)
        counter += 1
        
    counter = MA2
    while counter <= len(results):
        sub = results[counter-MA2:counter]
        temp = sum(sub)/MA2
        
        if counter == MA2:
            for i in range(MA2-1):
                ma2.append(temp)
        ma2.append(temp)
        counter += 1

    df['MA1'] = ma1
    df['MA2'] = ma2
    s1 = str(MA1) + 'MA'
    s2 = str(MA2) + 'MA'        
        
#    mean = []
#    sd = []
#    counter = lookback
#    while counter <= len(results):
#        sub = results[counter-lookback:counter]
#        temp = sum(sub)/lookback
#        s = std(sub)
#        
#        if counter == lookback:
#            for i in range(lookback-1):
#                mean.append(temp)
#                sd.append(s)
#        mean.append(temp)
#        sd.append(s)

#        counter = counter + 1
    
#    df['mean'] = mean
    
    prev = 0
    curr = 0
    curr = n2-beta_hr*n1
    df['curr'] = curr
    
    if p1!=None and p2!=None:
        prev = p2-beta_hr*p1
        df['prev'] = prev
    
    months = mdates.MonthLocator() # every month
    fig, ax = plt.subplots()
    ax.plot(df.index, df["res"])
#    ax.plot(df.index, df["mean"],'k')
    ax.plot(df.index, df["MA1"],'k', label=s1)
    ax.plot(df.index, df["MA2"],'r', label=s2)
    if curr != 0:
        ax.plot(df.index, df["curr"],'y')
    if prev != 0:
        ax.plot(df.index, df["prev"],'m', label='Prev')
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
    
      
if __name__ == "__main__":
    end = datetime.datetime.now()
    start = datetime.datetime(end.year-2, end.month, end.day)
    
    XEL = 33.14
    CMS = 32.239
    PNC = 97.66
    STI = 43.704
    BMY = 67.045
    CERN = 69.68
    
    run_test('XEL','CMS',start,end,10,XEL,CMS)
#    run_test('PNC','STI',start,end,10,PNC,STI)
#    run_test('BMY','CERN',start,end,10,BMY,CERN)