from numpy import std,mean
from events import SignalEvent

class Strategy:
    
    def __init__(self):
        
        self.description = "XEL CMS Mean Reversion\n"
        self.symbols = ["XEL","CMS"]
        self.event = None
        
        self.mean = None
        self.band1 = None
        self.band2 = None
        
        self.beta = 1
        
    def setQueue(self,event):
        self.event = event
    
    def setup(self,dataHandler):
        #Run at start of each trading day
    
        XEL = dataHandler.getLatestValues("XEL",10,"Adj Close")
        CMS = dataHandler.getLatestValues("CMS",10,"Adj Close")
        
        if XEL == None or CMS == None:
            return
        
        res = []
        
        i = 0
        
        while i < len(XEL):
            res[i] = CMS[i] - self.beta*XEL[i]
            i += 1
            
        self.mean = mean(res)
        self.sd = std(res)
        
        self.band1 = self.mean + self.sd
        self.band2= self.mean - self.sd
    
    def calculateSignal(self,dataHandler):
        
        if self.mean == None:
            return
        
        XELp = dataHandler.getLatestValue(self,"XEL","Adj Close")
        CMSp = dataHandler.getLatestValue(self,"CMS","Adj Close")
        
        res = CMSp - self.beta*XELp
        
        date = dataHandler.getDate()
                
        if res > self.band1:
            signal = SignalEvent("XEL",date,1,1)
            self.event.append(signal)
            signal = SignalEvent("CMS",date,-1,1)
            self.event.append(signal)
        elif res < self.band2:
            signal = SignalEvent("XEL",date,-1,1)
            self.event.append(signal)
            signal = SignalEvent("CMS",date,1,1)
            self.event.append(signal)
    
    def createOrder(self,signal,portfolio):
        
        pass
    
    