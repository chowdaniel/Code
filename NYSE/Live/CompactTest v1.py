import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pandas.io.data as web

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
    
def run_test(stock1,stock2,start,end,mean,sd,beta,n1,n2,p1=None,p2=None,full=False):
    
    first = web.DataReader(stock1, "yahoo", start, end)
    second = web.DataReader(stock2, "yahoo", start, end)
    df = pd.DataFrame(index=first.index)
    df[stock1] = first["Adj Close"]
    df[stock2] = second["Adj Close"]
        
    beta_hr = beta
    
    temp = 'EQN: ' + stock2 + ' - ' + str(beta_hr) + '*' + stock1
    print temp
    print ' '
    
    df["res"] = df[stock2] - beta_hr*df[stock1]
    df['mean'] = mean
    
    temp = 'Mean = ' + str(mean)
    print temp
    temp = 'SD = ' + str(sd)
    print temp
    temp = 'Beta = ' + str(beta_hr)
    print temp
    
    df['sd1'] = df['mean'] + sd
    df['sd2'] = df['mean'] + 3*sd
    df['sd3'] = df['mean'] + -1*sd
    df['sd4'] = df['mean'] + -3*sd
    df['sd5'] = df['mean'] + 0.5*sd
    df['sd6'] = df['mean'] + -0.5*sd
    
    prev = 0
    curr = 0
    curr = n2-beta_hr*n1
    df['curr'] = curr
    
    if p1!=None and p2!=None:
        prev = p2-beta_hr*p1
        df['prev'] = prev
    if full:
        plot_price_series(df, stock1, stock2,start,end)         
    months = mdates.MonthLocator() # every month
    fig, ax = plt.subplots()
    ax.plot(df.index, df["res"])
    ax.plot(df.index, df["mean"],'k')
    ax.plot(df.index, df["sd1"],'r--')
    ax.plot(df.index, df["sd2"],'r--')
    ax.plot(df.index, df["sd3"],'r--')
    ax.plot(df.index, df["sd4"],'r--')
    ax.plot(df.index, df["sd5"],'c--')
    ax.plot(df.index, df["sd6"],'c--')
    if curr != 0:
        ax.plot(df.index, df["curr"],'y')
    if prev != 0:
        ax.plot(df.index, df["prev"],'m')
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
    
    
    return df
    
start = datetime.datetime(2013, 5, 28)
end = datetime.datetime(2015, 5, 28)   
XEL = 34.06
CMS = 34.14
PNC = 95.685
STT = 42.955
BMY = 68.49
CERN = 68.51

run_test('XEL','CMS',start,end,-5.68557116032,0.414662507209,1.14767289667,XEL,CMS,34.1196,34.07)
#run_test('PNC','STI',start,end,2.65507793609,0.48655499872,0.422904300182,PNC,STT,0,0)
#run_test('BMY','CERN',start,end,5.68517971052,2.32827562466,1.0188011627,BMY,CERN,0,0)
