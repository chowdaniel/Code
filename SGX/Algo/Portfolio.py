import csv
import datetime 
import events   
import math
    
class Portfolio():
    
    def __init__(self,event,symbol):

        self.cash = 0
        self.value = 0
        self.prev = 0
        self.holdings = {}
        self.position = 0 
        self.symbol = symbol
        #1 - in the market
        #0 - out of market
        self.event = event
        self.MA1 = 0
        self.MA2 = 0
        
    def setcash(self,capital):
        
        self.cash = capital
        self.prev = self.cash
        self.value = self.cash
        
    def setup(self,handler):
        
        fifty = handler.get_latest_bar_values(self.symbol,'',50)
        twenty = handler.get_latest_bar_values(self.symbol,'',20)
        
        temp = sum(fifty)
        self.MA1 = temp/len(fifty)
        temp = sum(twenty)
        self.MA2 = temp/len(twenty)
                
    def calculate(self,handler):
        
        self.event.popleft()
        
        if self.position == 0:
            if self.MA2 > self.MA1:
                #Buy Signal
                self.event.append(events.SignalEvent(self.symbol,datetime.datetime.now(),'BUY',1))
        elif self.position == 1:
            if self.MA2 < self.MA1:
                #Sell Signal
                self.event.append(events.SignalEvent(self.symbol,datetime.datetime.now(),'SELL',-1))
    
    def order(self,handler):
        
        signal = self.event.popleft()
        
        if signal.direction == 'SELL':
            
            order1 = events.OrderEvent(self.symbol,'SELL',-1*self.holdings[self.symbol])
            self.event.append(order1)
            self.position = 0
            
        else:
            
            price = handler.get_latest_bar_value(signal.symbol,'')
            total = price*100
            units = math.floor((self.cash-100)/total)
            
            order1 = events.OrderEvent(self.symbol,'BUY',units*100)
            self.event.append(order1)
            self.position = 1
            
    def fill(self,tradeevent):

        
        self.cash = self.cash - tradeevent.comm
        self.cash = self.cash - tradeevent.cost
                
        if tradeevent.symbol in self.holdings:
            temp = self.holdings[tradeevent.symbol]
        else:
            temp = 0
        
        temp += tradeevent.quantity
        self.holdings[tradeevent.symbol] = temp

#        data = []
#        row = []
        # Edit to dynamic path
#        with open('C:\Users\Daniel\Desktop\SMA\Trades.csv','a') as t_data:
#            
#            tradedata = csv.writer(t_data)
#
#            data.append(tradeevent.time)
#            data.append(tradeevent.symbol)
#            data.append(tradeevent.quantity)
#            data.append(tradeevent.price)
#            data.append(tradeevent.comm)
#            data.append(tradeevent.comm + tradeevent.price*tradeevent.quantity)
#            row.append(data)
#            tradedata.writerows(row)
        
    def update(self,handler):
        #Updates end of day performance
        row = []        
        data = []
        h = 0
        
        data.append(handler.get_latest_bar_datetime(self.symbol))
        cash = self.cash
        data.append(cash)
        for c in self.holdings:
            
            h += self.holdings[c] * handler.get_latest_bar_value(c,'Close')
            
        data.append(h)
        self.value = cash + h
        data.append(self.value)
        
        row.append(data)
        #Edit to dynamic path
#        with open('C:\Users\Daniel\Desktop\SMA\EOD.csv','a') as EOD_data:
#            
#            EODdata = csv.writer(EOD_data)
#            
#            EODdata.writerows(row)
#        
#        self.prev = self.cash
    
    
    


