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
    startindex = 599
    endindex = 600
    start = datetime.datetime(2013, 1, 1)
    end = datetime.datetime(2015,1,1)    
    
    temp = open("C:\Users\Daniel\Desktop\VOL.csv",'r')
    full = csv.reader(temp)
    symbol = []
    temp1 = open("C:\Users\Daniel\Desktop\R.csv",'a')
    result = csv.writer(temp1)
    
    for i in full:
        symbol.append(i[0])
        
    for i in range(startindex,endindex):
        if True:
            print i
            s = symbol[i]
            event = deque()
            data = datahandler.SGXHandler(event,s,start,end)
            portfolio = Portfolio.Portfolio(event,s)
        
            a = Backtest(event,data,portfolio,s)
        
            res = a.run(capital)
            abc = []
            abc.append(i)
            abc.append(s)
            abc.append(res)
            result.writerows([abc])
#        except:
#            continue

        
    
    
    
    
    