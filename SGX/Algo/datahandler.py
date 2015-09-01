import urllib2
import datetime

from abc import ABCMeta, abstractmethod

from events import MarketEvent

class DataHandler():
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def get_latest_bar(self,symbol):
        
        #Returns the latest data for 'symbol'
        pass
    @abstractmethod
    def get_latest_bars(self,symbol,n=1):
        
        #Returns the latest 'n' data for 'symbol'
        pass
    @abstractmethod
    def get_latest_bar_datetime(self,symbol):
        
        # Returns the latest date & time of 'symbol' as datetime object
        pass
    @abstractmethod
    def get_latest_bar_value(self,symbol,v_type):
        
        #v_type can be strings like 'Open', 'Close', 'High', 'Low'
        
        #Returns the latest 'v_type' value of 'symbol' 
        pass
    @abstractmethod
    def get_latest_bar_values(self,symbol,v_type,n=1):
        
        #v_type can be strings like 'Open', 'Close', 'High', 'Low'
        
        #Returns the latest 'n' 'v_type' value of 'symbol' 
        pass
    
    def update_bars(self):
        
        pass
    
class SGXHandler(DataHandler):
    
    def __init__(self,events,symbol,start,end):
        
        self.events = events
        self.continue_backtest = True
        self.index = 0
        
        dates = []
        close = []
        temp1 = []
        
        url = "http://ichart.finance.yahoo.com/table.csv?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s" % (symbol, start.day - 1, start.month, start.year, end.day - 1, end.month, end.year)
        data = urllib2.urlopen(url)
        
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
            
        counter = 0
        self.symbol_data = []
        
        while counter < len(close):
            temp = (dates[counter],close[counter])
            self.symbol_data.append(temp)
            counter += 1

    def get_latest_bar(self,symbol):
        
        return self.symbol_data[self.index]
        
    def get_latest_bars(self,symbol,n=1):
        
        start = self.index+1-n
        if start >= 0:
            a = self.symbol_data[start:self.index+1]
            return a
        else:
            return self.symbol_data[0:self.index+1]
            
    def get_latest_bar_datetime(self,symbol):
        
        return self.symbol_data[self.index][0]
        
    def get_latest_bar_value(self,symbol,v_type):
        
        return self.symbol_data[self.index][1]
    
    def get_latest_bar_values(self,symbol,v_type,n=1):
        
        start = self.index+1-n
        if start >= 0:
            temp = self.symbol_data[start:self.index+1]
        else:
            temp = self.symbol_data[0:self.index+1]
        
        res = []
        for i in temp:
            res.append(i[1])
        
        return res
        
    def update_bars(self):
        
        self.index += 1
        if self.index >= len(self.symbol_data):
            self.index -= 1
            self.continue_backtest=False
        else:
            self.events.append(MarketEvent())

if __name__ == '__main__':
    event = []
    start = datetime.datetime(2014, 1, 1)
    end = datetime.datetime(2015,1,1)
    a = SGXHandler(event,"S51.SI",start,end)

    
    
    