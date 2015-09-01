class Event():
    
    pass



class MarketEvent(Event):
    #Signals that there is a update in market data
    
    def __init__(self):
        
        self.type = "Market"
        
        
class SignalEvent(Event):
    
    def __init__(self,sym,date_time,direct,strength):
        
        self.type = "Signel"
        self.symbol = sym
        self.datetime = date_time
        self.direction = direct
        self.strength = strength
        
        
class OrderEvent(Event):
    
    def __init__(self,sym,o_type,quant):
        
        self.type = "Order"
        self.symbol = sym
        self.order_type = o_type
        self.quantity = quant        
        
    def print_order(self):
        
        print "Order: Symbol=%s, Type=%s, Quantity=%s, Direction=%s" %(self.symbol, self.order_type, self.quantity, self.direction)


class TradeEvent(Event):
    
    def __init__(self,time,sym,exchange,quantity,price,direct,cost,comm=None):
        
        self.type = "Trade"
        self.time = time
        self.symbol = sym
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direct
        self.cost = cost
        self.price = price
        
        if comm == None:
            self.comm = self.est_comm()
        else:
            self.comm = comm
            
    def est_comm(self):
        
        min_price = 25
        estimated = self.cost*0.18/100
            
        return max(min_price,estimated)
        
        

        