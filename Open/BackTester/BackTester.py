from collections import deque
import events
import datetime
from pandasDataHandler import pandasDataHandler
from Portfolio import Portfolio
from Strategy import Strategy

class Backtest():
    
    def __init__(self,start,end,capital):
        
        self.event = deque()
        self.start = start
        self.end = end
        self.capital = capital
        
        self.dataHandler = None
        self.portfolio = None      
        self.strategy = None
        
        print "Starting new BackTest\n"
        
    def setStrategy(self,strategy):
        
        self.strategy = strategy
        print "BackTest Strategy: %s" % self.strategy.description
        
        self.initializeDataHandler()
        
        self.portfolio = Portfolio(self.capital,self.dataHandler)
        
        self.portfolio.setQueue(self.event)       
        self.strategy.setQueue(self.event)
        
    def initializeDataHandler(self):
        
        symbols = self.strategy.symbols
        
        print "Initializing DataHandler: Found %d symbols" % len(symbols)
        
        self.dataHandler = pandasDataHandler(symbols,self.start,self.end)   
        
        print "DataHandler Initialized. Ready to run BackTest\n"
        
    def run(self):
        
        if self.strategy == None:
            print "Error: Strategy not set"
            return
        
        while(self.data.continue_backtest==True):
            #Start of New Trading Day
            self.strategy.setup(self.dataHandler)
            self.data.updateBars()   
            market = events.MarketEvent()
            self.event.append(market)
            self.date = self.data.getDate()
            
            while len(self.event) != 0:
                
                self.parseEvent()
                
        #End of Trading Day
        self.portfolio.update(self.date)
            
    def parseEvent(self):
        
        event = self.event.popleft()
        
        if isinstance(event,events.MarketEvent) == True:
            self.strategy.calculateSignal(self.dataHandler)
                  
        elif isinstance(event,events.SignalEvent) == True:
            self.strategy.createOrder(event,self.portfolio)
                   
        elif isinstance(event,events.OrderEvent) == True:
            self.executeOrder(event) 
            
            
        elif isinstance(event,events.TradeEvent) == True:   
            self.portfolio.fill(event,self.date)
            
    def executeOrder(self,event):
        
        trade = events.TradeEvent(self.date,event.symbol,'NYSE',
                                  event.quantity,event.price,
                                  event.quantity*event.price)
        
        self.event.append(trade)
        
if __name__ == "__main__":
    end = datetime.datetime.now()
    start = datetime.datetime(end.year-2, end.month, end.day)    
    
    backTest = Backtest(start,end,10000)
    strategy = Strategy()
    backTest.setStrategy(strategy)
    
    
    
        
        
