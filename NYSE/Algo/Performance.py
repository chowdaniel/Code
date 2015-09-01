import math
import matplotlib.pyplot
import csv

def graph(EOD,date=False):
    
    dates = []
    start = 0
    value = 0
    relative = []
    
    with open(EOD,'r') as data:
        rows = csv.reader(data)
        
        for row in rows:
            if start == 0:
                start = float(row[3])
            
            try:
                value = float(row[3])
            except ValueError:
                pass
            
            day = row[0]
            dates.append(day)
            relative.append(value/start)
    
    f_dates = []
    f_relative = []
    counter = 0

    while counter < len(dates):
        f_dates.append(dates[counter])
        f_relative.append(relative[counter])
        counter += 2
    
    if date == False:
        matplotlib.pyplot.plot(f_relative)
    else:
        matplotlib.pyplot.plot(f_dates,f_relative)
            
def sharpe(EOD,risk_free = 0):

    returns = []
    
    with open(EOD,'r') as data:
        rows = csv.reader(data)
        
        for row in rows:
            
            try:
                value = float(row[4])
            except ValueError:
                pass
            
            returns.append(value)
    
    f_returns = []
    counter = 0

    while counter < len(returns):
        f_returns.append(returns[counter])
        counter += 2

    count = len(f_returns)
    total = 0
    
    for data in f_returns:
        total += data
        
    mean = total/count
    
    temp_var = 0
    
    for data in f_returns:
        temp_var += math.pow((data-mean),2)
    
    std = math.sqrt(temp_var/count)
    
    sharpe = (mean-risk_free)/std
    norm_sharpe = math.sqrt(count) * sharpe
    
    print 'Sharpe Ratio: ' + str(sharpe)
    print 'Normalized Sharpe Ratio: ' + str(norm_sharpe)

def drawdown(EOD):
    
    max_drawdown = 0
    max_duration = 0
    
    returns = []
    
    with open(EOD,'r') as data:
        rows = csv.reader(data)
        
        for row in rows:
            
            try:
                value = float(row[3])
            except ValueError:
                pass
            
            returns.append(value)
    
    f_returns = []
    counter = 0

    while counter < len(returns):
        f_returns.append(returns[counter])
        counter += 2
    
    counter = 1
    
    duration = 0
    drawdown = 0
    top = 0
    down = False
    
    while counter < len(f_returns):
        if down == False:
            if f_returns[counter] < f_returns[counter-1]:
                #Detected a DrawDown
                down = True
                duration = 1
                top = f_returns[counter-1]
                drawdown = top - f_returns[counter]
            
        else:
            if f_returns[counter] >= top:
                #End of Drawdown
                down = False
                max_duration = max(duration,max_duration)
                max_drawdown = max(drawdown,max_drawdown)
            else:
                duration += 1
                drawdown = max(drawdown,top - f_returns[counter])
                
        if counter == len(f_returns)-1:
            if down == True:
                max_duration = max(duration,max_duration)
                max_drawdown = max(drawdown,max_drawdown)                
                
        counter += 1
        
    print 'Max Drawdown Duration: ' + str(max_duration)
    print 'Max Drawdown: ' + str(max_drawdown)
    
    print max(f_returns)
                
        
if __name__ == '__main__':
    
    graph('C:\Users\Daniel\Desktop\Algo\EOD.csv')
    sharpe('C:\Users\Daniel\Desktop\Algo\EOD.csv')
    drawdown('C:\Users\Daniel\Desktop\Algo\EOD.csv')
    


