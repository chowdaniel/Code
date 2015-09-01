import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import urllib2
import datetime
import pandas as pd


def run(symbol,start,end):
    
    url = "http://ichart.finance.yahoo.com/table.csv?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s" % (symbol, start.day - 1, start.month, start.year, end.day - 1, end.month, end.year)
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
    df[symbol] = close

    counter = 0
    fifty = []
    twenty = []
    
    total = sum(close[0:50])
    ave = total/len(close[0:50])
    while counter < len(close):
        if counter < 50:
            fifty.append(ave)
        else:
            total = sum(close[counter-49:counter+1])
            ave = total/50
            fifty.append(ave)
        counter += 1
    
    counter = 0 
    
    total = sum(close[0:20])
    ave = total/len(close[0:20])
    while counter < len(close):
        if counter < 20:
            twenty.append(ave)
        else:
            total = sum(close[counter-19:counter+1])
            ave = total/20
            twenty.append(ave)
        counter += 1
       
    df['50MA'] = fifty
    df['20MA'] = twenty

    months = mdates.MonthLocator() # every month
    fig, ax = plt.subplots()
    ax.plot(df.index, df[symbol], label="Price")
    ax.plot(df.index, df['50MA'],'m', label='50MA')
    ax.plot(df.index, df["20MA"],'y', label='20MA')
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.set_xlim(start,end)
    ax.grid(True)
    fig.autofmt_xdate()
    plt.xlabel('Month/Year')
    plt.ylabel('Price ($)')
    plt.title('MA Plot')
    plt.legend()
    plt.plot(df[symbol])
    plt.show()
            

if __name__ == '__main__':
    start = datetime.datetime(2014, 1, 1)
    end = datetime.datetime.now()
    run("Z74.SI",start,end)





















