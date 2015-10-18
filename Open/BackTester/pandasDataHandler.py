import pandas.io.data as web

class pandasDataHandler:
    
    def __init__(self,symbols,start,end):
        
        self.start = start
        self.end = end
        self.symbols = symbols
        
        self.continue_backtest = True
        
        self.symbolData = self.loadData(symbols)
        
        self.dates = self.symbolData[self.symbols[0]].index
        self.index = 0
            
    def loadData(self,symbols):
        
        data = {}
        
        for symbol in symbols:
            temp = web.DataReader(symbol, "yahoo", self.start, self.end)
            data[symbol] = temp
            
        return data
        
    def getDate(self):
        return self.dates[self.index]
          
    def updateBars(self):
        
        self.index += 1
        
        if self.index == len(self.dates):
            self.continue_backtest = False
        
    def getLatestValue(self,symbol,v_type):
        
        #v_type: 'Open", "High", "Low", "Close", "Volume", "Adj Close"
        date = self.dates[self.index]
        data = self.symbolData[symbol]
        
        return data.get_value(date,v_type)
        
    def getValue(self,symbol,date,v_type):
        
        data = self.symbolData[symbol]
        
        return data.get_value(date,v_type)
       
    def getLatestValues(self,symbol,n,v_type):
        
        if n > self.index:
            return None          
            
        else:
            dateRange = self.dates[self.index+1-n:self.index+1]
            
        res = []
        
        for date in dateRange:
            res.append(self.getValue(symbol,date,v_type))
            
        return res
    