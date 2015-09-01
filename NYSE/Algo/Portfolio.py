import csv
import datetime 
import events   
from numpy import std
import math
    
class Portfolio():
    
    def __init__(self,event):

        self.cash = 0
        self.bpower = 0
        self.prev = 0
        self.holdings = {}
        self.position = 0 
        self.event = event
        #0 - not in marker
        #1 - in band 1
        #-1 - in band -1
        self.mean = 0
        self.sd = 0
        self.band2 = 0
        self.band1 = 0
        self.beta = 1.1044780978
        
    def setcash(self,capital):
        
        self.cash = capital
        self.prev = self.cash
        self.bpower = capital * 2
        
    def setup(self,handler):
        
        res = []
        
        XEL = handler.get_latest_bars('XEL',10)
        CMS = handler.get_latest_bars('CMS',10)
        
        counter = 0
        
        while counter < 10:
            temp = CMS[counter][1][5] - self.beta*XEL[counter][1][5]
            res.append(temp)
            counter = counter + 1
        
        self.mean = sum(res)/10
        self.sd = std(res)
        self.band1 = self.mean-self.sd
        self.band2 = self.mean+self.sd
                
    def calculate(self,handler):
        
        self.event.popleft()
        
        XEL = handler.get_latest_bar('XEL')[1][5]
        CMS = handler.get_latest_bar('CMS')[1][5]
        
        current = CMS - self.beta*XEL

        if self.position == 0:            
            if current > self.band2:
                signal = events.SignalEvent(('XEL','CMS'),datetime.datetime.now(),'BUY',1)
                self.event.append(signal)
                
            elif current < self.band1:
                signal = events.SignalEvent(('XEL','CMS'),datetime.datetime.now(),'BUY',-1)
                self.event.append(signal)

        elif self.position == 1:
            if current < self.mean:
                signal = events.SignalEvent(('XEL','CMS'),datetime.datetime.now(),'SELL',0)
                self.event.append(signal)
            
        elif self.position == -1:
            if current > self.mean:
                signal = events.SignalEvent(('XEL','CMS'),datetime.datetime.now(),'SELL',0)
                self.event.append(signal)
    
    def order(self,handler):
        
        signal = self.event.popleft()
        
        if signal.direction == 'SELL':
            
            order1 = events.OrderEvent('XEL',' ',-1*self.holdings['XEL'])
            order2 = events.OrderEvent('CMS',' ',-1*self.holdings['CMS'])
            self.event.append(order1)
            self.event.append(order2)
            self.position = 0
            
        else:
            
            XEL = handler.get_latest_bar('XEL')[1][5]
            CMS = handler.get_latest_bar('CMS')[1][5]
            total = XEL*100 + CMS*100
            units = math.floor(self.bpower/total)
            
            if signal.strength == 1:
                #Sell CMS buy XEL
                order1 = events.OrderEvent('XEL','BUY',units*100)
                order2 = events.OrderEvent('CMS','SELL',-1*units*100)
                self.event.append(order1)
                self.event.append(order2)  
                self.position = 1
                            
            elif signal.strength == -1:
                #Buy CMS sell XEL
                order1 = events.OrderEvent('XEL','SELL',-1*units*100)
                order2 = events.OrderEvent('CMS','BUY',units*100)
                self.event.append(order1)
                self.event.append(order2)
                self.position = -1
            
    def fill(self,tradeevent,index):

        
        self.cash = self.cash - tradeevent.comm
        self.cash = self.cash - tradeevent.cost
                
        if tradeevent.symbol in self.holdings:
            temp = self.holdings[tradeevent.symbol]
        else:
            temp = 0
        
        temp += tradeevent.quantity
        self.holdings[tradeevent.symbol] = temp

        data = []
        row = []
        # Edit to dynamic path
        with open('C:\Users\Daniel\Desktop\Trades.csv','a') as t_data:
            
            tradedata = csv.writer(t_data)
            
            data.append(index)
            data.append(tradeevent.time)
            data.append(tradeevent.symbol)
            data.append(tradeevent.quantity)
            data.append(tradeevent.price)
            data.append(tradeevent.comm)
            data.append(tradeevent.comm + tradeevent.price*tradeevent.quantity)
            row.append(data)
            
            tradedata.writerows(row)
        
    def update(self,handler,index):
        #Updates end of day performance
        if self.position == 0:
            self.bpower = self.cash * 2
        row = []        
        data = []
        h = 0
        
        data.append(datetime.date.today())   
        cash = self.cash
        data.append(index)
        data.append(cash)
        for c in self.holdings:
            
            h += self.holdings[c] * handler.get_latest_bar_value(c,'Close')
            
        data.append(h)
        data.append(cash+h)
        data.append(((cash+h-self.prev)/self.prev)*100)
        
        row.append(data)
        #Edit to dynamic path
        with open('C:\Users\Daniel\Desktop\EOD.csv','a') as EOD_data:
            
            EODdata = csv.writer(EOD_data)
            
            EODdata.writerows(row)
        
        self.prev = self.cash
    
    
    


