import csv

class Portfolio():
    
    def __init__(self,capital,dataHandler):
        
        self.capital = capital
        self.prev = capital
        self.holdings = {}
        self.holdingsValue = 0
        self.totalValue = capital
        self.event = None
        self.dataHandler = dataHandler
        
    def setQueue(self,event):
        self.event = event
    
    def fill(self,event,date):
        
        self.cash = self.cash - event.comm
        self.cash = self.cash - event.cost
        
        symbol = event.symbol
        
        if symbol in self.holdings:
            oldQuantity = self.holdings[symbol]
        else:
            oldQuantity = 0
            
        newQuantity = oldQuantity + event.quantity
        
        if abs(newQuantity) > abs(oldQuantity):
            #Increased Position
            self.bpower -= (event.cost + event.comm) * 2
        else:
            self.bpower += (event.cost - event.comm) * 2
        
        if newQuantity == 0:
            del self.holdings[symbol]
        
        else:            
            self.holdings[symbol] = newQuantity

        data = []
        row = []
        # Edit to dynamic path
        with open('Trades.csv','a') as t_data:
            
            tradeData = csv.writer(t_data)
            
            data.append(date)
            data.append(event.time)
            data.append(event.symbol)
            data.append(event.quantity)
            data.append(event.price)
            data.append(event.comm)
            data.append(event.comm + event.cost)
            row.append(data)
            
            tradeData.writerows(row)        
            
    def update(self,date):
        
        self.valueHoldings()
        
        row = ['Symbol','Quantity','Price','TotalValue']       
        data = [row]
        
        EOD = open(date,'a')
        eodData = csv.writer(EOD)        
        eodData.writerows(data)
        
        for symbol in self.holdings.keys():               
            symbolQuantity = self.holdings[symbol]
            symbolPrice = self.data.getLatestPrice(symbol)
            row = [symbol,symbolQuantity,symbolPrice,symbolQuantity*symbolPrice]

            data = []
            eodData.writerows(data)

        row = ['Cash',self.cash,'Holdings',self.holdingsValue,'Total',self.cash+self.holdingsValue,'BPower',self.bpower]     
        data = [row]
        eodData.writerows(data)
        
        EOD.close()
        
        outputFile = open(date.strftime('%d/%m/%Y') + '.txt','w')
        header = "Symbol, Quantity, Price, TotalValue"
        outputFile.write(header)
        
        
        
    def valueHoldings(self):
        
        self.holdingsValue = 0
               
        for symbol in self.holdings.keys():               
            symbolQuantity = self.holdings[symbol]
            symbolPrice = self.data.getLatestPrice(symbol)
            self.holdingsValue += symbolQuantity * symbolPrice
            
    
            
            