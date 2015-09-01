import os,os.path
import numpy
import pandas

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
    
class CSVHandler(DataHandler):
        
    def __init__(self,events,csv_dir,symbol_list):
            
        #Events - Event Queue
        #symnol_list - List of symbol strings
        #csv_dir - Directory of CSV files to be stored into handler
            
        self.events = events
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list
            
        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.continue_backtest = True
            
        self._open_convert_csv_files()
            
    def _open_convert_csv_files(self):
            
        comb_index = None
            
        for s in self.symbol_list:
            
            self.symbol_data[s] =\
            pandas.io.parsers.read_csv(os.path.join(self.csv_dir,'%s.csv' % s),header=0, index_col=0,parse_dates=True, names=['Date','Open','High','Low','Close','Volume','Adj Close']).sort()
            if comb_index is None:
                comb_index = self.symbol_data[s].index
            else:
                comb_index.union(self.symbol_data[s].index)
                
            self.latest_symbol_data[s] = []
        
        for s in self.symbol_list:
            self.symbol_data[s] = self.symbol_data[s].\
                reindex(index=comb_index,method = 'pad').iterrows()
                    
    def _get_new_bar(self,symbol):
            
        for b in self.symbol_data[symbol]:
            yield b
                
    def get_latest_bar(self,symbol):
    
        #Returns the latest price of symbol
    
        try:
            bars_list = self.latest_symbol_data[symbol]
                
        except KeyError:
            print "That symbol is not available in the historical data set."
            raise
        else:
            return bars_list[-1]
          
    def get_latest_bars(self,symbol,n=1):
        
        #Returns the nth latest prices of symbol in a list
            
        try:
            bars_list = self.latest_symbol_data[symbol]
                
        except KeyError:
            print "That symbol is not available in the historical data set."
            raise
        else:
            return bars_list[-n:]
        
    def get_latest_bar_datetime(self,symbol):
            
        try:
            bars_list = self.latest_symbol_data[symbol]
                
        except KeyError:
            print "That symbol is not available in the historical data set."
            raise
        else:
            return bars_list[-1][0]
                
    def get_latest_bar_value(self,symbol,v_type):
            
        try:
            bars_list = self.latest_symbol_data[symbol]
                
        except KeyError:
            print "That symbol is not available in the historical data set."
            raise
        else:
            return getattr(bars_list[-1][1], v_type)           
                    
    def get_latest_bar_values(self,symbol,v_type,n=1):

        try:
            bars_list = self.get_latest_bars(symbol, n)
                
        except KeyError:
            print "That symbol is not available in the historical data set."
            raise
        else:
            return numpy.array([getattr(b[1], v_type) for b in bars_list])
                
    def update_bars(self):
            
        for s in self.symbol_list:
            try:
                bar = self._get_new_bar(s).next()
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    self.latest_symbol_data[s].append(bar)
        self.events.append(MarketEvent())

if __name__ == '__main__':
    event = []
    data = CSVHandler(event,'C:\Users\Daniel\Desktop',['XEL','CMS'])  
    
    
    
    