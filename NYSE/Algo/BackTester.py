from collections import deque
import datahandler
import Portfolio
import events
import datetime

class Backtest():
    
    def __init__(self,event,data,portfolio):
        
        self.event = event       
        self.handler = data        
        self.portfolio = portfolio
        self.index = 0
        
    def run(self,capital):
        
        self.handler.continue_backtest = True
        self.portfolio.cash = capital
        self.portfolio.setcash(capital)
        
        for i in range(10):
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

                    self.execute(self.index)

            portfolio.update(self.handler,self.index)
            self.index = self.index + 1
    def execute(self,index):
        
        order = self.event.popleft()
        
        trade = events.TradeEvent(datetime.datetime.now(),order.symbol,'NYSE',order.quantity,self.handler.get_latest_bar(order.symbol)[1][5],' ',order.quantity*self.handler.get_latest_bar(order.symbol)[1][5])
        self.portfolio.fill(trade,index)
    
        
if __name__ == '__main__':
    
    event = deque()
    
    data = datahandler.CSVHandler(event,'C:\Users\Daniel\Desktop',['XEL','CMS'])
    portfolio = Portfolio.Portfolio(event)
    
    a = Backtest(event,data,portfolio)
    
    a.run(9000)
    
    
    
    