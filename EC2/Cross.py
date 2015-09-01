#!/usr/bin/python

import urllib2
import datetime

def run(symbol,start,end):
    
    url = "http://ichart.finance.yahoo.com/table.csv?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s" % (symbol, start.month-1, start.day, start.year, end.month-1, end.day, end.year)
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

    temp1.reverse()
    temp1.pop()
    
    for i in temp1:
        close.append(float(i))

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
        
    counter = 0
    data = []
    
    while counter < len(dates):
        temp = [dates[counter],twenty[counter],fifty[counter]]
        counter += 1
        data.append(temp)
        
    data.reverse()
    out = []
    
    if data[0][1] > data[0][2]:
        #20MA above 40MA
        counter = 1
        while counter < len(data):
            if data[counter][1] < data[counter][2]:
                break
            counter += 1
        out.append(symbol)
        cross = data[counter][0]
        cross = cross.split('-')
        cross = cross[2] + '/' + cross[1] + '/' + cross[0]
        out.append(cross)
        out.append(counter)
    
    return out
        
if __name__ == '__main__':
    end = datetime.datetime.now()
    start = datetime.datetime(end.year-1, 1, end.month)
    a = run("588.SI",start,end)
    print a
