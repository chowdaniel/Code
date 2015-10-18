import datetime
import matplotlib.pyplot as plt
import pandas as pd
import pandas.io.data as web
from pandas.stats.api import ols
import statsmodels.tsa.stattools as ts
import numpy as np
import math

class PairsTrade:
    
    def __init__(self,start,end):
        self.start = start
        self.end = end
        
    def setFormula(self,formula):
        self.formula = formula
        
    def runTest(self,stock1,stock2):

        start = self.start
        end = self.end        
        
        first = web.DataReader(stock1, "yahoo", start, end)
        second = web.DataReader(stock2, "yahoo", start, end)

        first["Value"] = map(self.formula,first["Adj Close"].tolist()) 
        second["Value"] = map(self.formula,second["Adj Close"].tolist())
        
        df = pd.DataFrame(index=first.index)
        df[stock1] = first["Value"]
        df[stock2] = second["Value"]
        
        res = ols(y=df[stock2], x=df[stock1])
        
        beta = res.beta.x
        R2 = res.r2
        
        df["res"] = df[stock2] - beta*df[stock1]  
        
        #Runs CADF and get results
        cadf = ts.adfuller(df["res"])
        
        testStat = cadf[0]
        pValue = cadf[1]
        
        #Calculates Hurst Exponent
        hurst = self.hurst(df["res"])   
        
        results = df["res"].tolist()
        counter = 1
        delta = []
        while counter < len(results):
            temp = results[counter] - results[counter-1]
            delta.append(temp)
            counter = counter + 1
        results.pop()
    
        halfLife = self.half_life(delta,results)
        
        pair = Pair(stock1,stock2,beta,R2,testStat,pValue,hurst,halfLife)
        
        return pair
        
    def half_life(self,delta,y):
    
        data = pd.DataFrame({'Delta':delta,'Y':y})
        results = ols(y=data['Delta'], x=data['Y'])
        halfLife = -math.log(2)/results.beta.x
    
        return halfLife
        
    def hurst(self,ts):
        
        lags = range(2, 100)
        tau = [np.sqrt(np.std(np.subtract(ts[lag:], ts[:-lag]))) for lag in lags]
        poly = np.polyfit(np.log(lags), np.log(tau), 1)
        
        return poly[0]*2.0
        
class Pair:
    
    def __init__(self,stock1,stock2,beta,R2,testStat,pValue,hurst,halfLife):
        self.stock1 = stock1
        self.stock2 = stock2
        self.beta = beta
        self.R2 = R2
        self.testStat = testStat
        self.pValue = pValue
        self.hurst = hurst
        self.halfLife = halfLife
    
    def toTxt(self):
        return "%s,%s,%f,%f,%f,%f,%f,%f" % (self.stock1,self.stock2,self.beta,self.R2,self.testStat,self.pValue,self.hurst,self.halfLife)
        
    def printData(self):
        print "Eqn: %s - %f*%s\tR2: %f\n" % (self.stock2,self.beta,self.stock1,self.R2)
        print "CADF"
        print "Test Stat: %f\np-Value: %f\n" % (self.testStat,self.pValue)
        print "Hurst: %f\n" % (self.hurst)
        print "HalfLife: %f" % (self.halfLife)
        
if __name__ == "__main__":
    
    end = datetime.datetime.now()
    start = datetime.datetime(end.year-2, end.month, end.day)
    pair = PairsTrade(start,end)
    pair.setFormula(lambda x:x)
    a = pair.runTest("XEL","CMS")