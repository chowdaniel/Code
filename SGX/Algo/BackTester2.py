from collections import deque
import datahandler
import Portfolio
import events
import datetime
import csv

class Backtest():
    
    def __init__(self,event,data,portfolio,symbol):
        
        self.event = event       
        self.handler = data        
        self.portfolio = portfolio
        self.symbol = symbol
        
    def run(self,capital):
        
        self.handler.continue_backtest = True
        self.portfolio.cash = capital
        self.portfolio.setcash(capital)
        
        for i in range(50):
            self.handler.update_bars()
            self.event.popleft()
        
        while self.handler.continue_backtest == True:
            
            self.portfolio.setup(self.handler)
            self.handler.update_bars()
            
            while len(self.event) != 0:
                
                if isinstance(self.event[0],events.MarketEvent) == True:

                    portfolio.calculate(self.handler)
                    
                elif isinstance(self.event[0],events.SignalEvent) == True:

                    portfolio.order(self.handler)
                    
                elif isinstance(self.event[0],events.OrderEvent) == True:

                    self.execute()

            
            portfolio.update(self.handler)
            
        return self.portfolio.value
        
    def execute(self):
        
        order = self.event.popleft()
        
        trade = events.TradeEvent(self.handler.get_latest_bar_datetime(self.symbol),order.symbol,'SGX',order.quantity,self.handler.get_latest_bar_value(order.symbol,''),' ',order.quantity*self.handler.get_latest_bar_value(order.symbol,''))
        self.portfolio.fill(trade)
    
        
if __name__ == '__main__':
    
    capital = 10000
    end = datetime.datetime(2015,6,1)
    start = datetime.datetime(2014,1,1)
    
    temp = open("C:\Users\Daniel\Desktop\TEMP.csv",'r')
    full = csv.reader(temp)
    symbol = []
    temp1 = open("C:\Users\Daniel\Desktop\NEW.csv",'w')
    result = csv.writer(temp1)
      
    for s in full:
        try:
            print s[1]
            event = deque()
            data = datahandler.SGXHandler(event,s[1],start,end)
            portfolio = Portfolio.Portfolio(event,s[1])
        
            a = Backtest(event,data,portfolio,s[1])
        
            res = a.run(capital)
            abc = []
            abc.append(s[0])
            abc.append(s[1])
            abc.append(s[2])
            abc.append(res)
            result.writerows([abc])
        except:
            continue

        
    
    
    
    
    