#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Monte-Carlo Option Pricing


from scipy.stats import norm
import math
from random import *
import statistics
import time



class MCStockOption:
    
    '''Defined a Monte Carlo Stock option class.'''
    
    def __init__(self, s, x, r, sigma, t, nsteps, ntrials):
        
        '''Initialize a MCStockOption object'''
        
        self.s = s
        self.x = x
        self.r = r
        self.sigma = sigma
        self.t = t
        self.nsteps = nsteps
        self.ntrials = ntrials
        
    
    def __repr__(self):
        
        '''Method to return a string representation of the object'''
        
        return 'MCStockOption, s=' + '%4.2f'%self.s +', x=' + '%4.2f'%self.x + ', r=' + '%0.2f'%self.r +\
                ', sigma='+'%4.2f'%self.sigma + ', t=' + '%4.2f'%self.t + ', nsteps=' + str(self.nsteps) +', ntrials=' + str(self.ntrials)
                
    
  
    def generate_stock_prices(self):
        
        '''Method to get stock prices from Monte Carlo Simulation.'''
        
        dt = self.t/self.nsteps
        
        a = self.r - ((self.sigma **2)/2)
        
        #here random.gauss gave me an error. So I imported random and used only gauss.
        sim_stk_rtn = [ math.exp((a*dt + gauss(0,1)*self.sigma*(dt ** 0.5))) for x in range(self.nsteps) ]
        
        stk_price = [self.s]
        
        for i in sim_stk_rtn:
            stk_price += [stk_price [-1] * i]
        
        return stk_price
    
   
    def value(self):
        
        '''Method to calculate the value of an option.'''
        
        print ('Base class MCStockOption has no concrete implementation of .value().')
        return 0
    
  
    def stderr(self):
        
        '''Method to calculate the standard deviation error.'''
        
        if 'stdev' in dir(self):
            return self.stdev / math.sqrt(self.ntrials)
        return 0
    


# European Call option
class MCEuroCallOption(MCStockOption):
    
    '''Defined a Monte Carlo European call option class.'''
    
    
    def __init__(self, s, x, r, sigma, t, nsteps, ntrials):
        
        '''Initialize a MCEuroCallOption object from MCStockOption class'''
        
        MCStockOption.__init__(self, s, x, r, sigma, t, nsteps, ntrials)
        
        
        
    def __repr__(self):
        
        '''Method to return a string representation of the object'''
        
        return 'MCEuroCallOption, s=' + '%4.2f'%self.s +', x=' + '%4.2f'%self.x + ', r=' + '%0.2f'%self.r +\
                ', sigma='+'%4.2f'%self.sigma + ', t=' + '%4.2f'%self.t + ', nsteps=' + str(self.nsteps) +', ntrials=' + str(self.ntrials)
    
     
    
    def value(self):
        
        '''Method to calculate the value of an european call option.'''
        
        opt_values = []
        for i in range(self.ntrials):
            
            stk_prices = MCStockOption.generate_stock_prices(self)
        
            opt_values += [(max(stk_prices[-1] - self.x, 0 )) * math.exp(-1*self.r * self.t)]
            
        self.mean = statistics.mean(opt_values)
        self.stdev = statistics.pstdev(opt_values)
        
        return statistics.mean(opt_values)
    




# European Put Option
class MCEuroPutOption(MCStockOption):
    
    '''Defined a Monte Carlo European put option class.'''
    
    def __init__(self, s, x, r, sigma, t, nsteps, ntrials):
        
        '''Initialize a MCEuroPutOption object from MCStockOption class'''
        
        MCStockOption.__init__(self, s, x, r, sigma, t, nsteps, ntrials)
        
        
    def __repr__(self):
        
        '''Method to return a string representation of the object'''
        
        return 'MCEuroPutOption, s=' + '%4.2f'%self.s +', x=' + '%4.2f'%self.x + ', r=' + '%0.2f'%self.r +\
                ', sigma='+'%4.2f'%self.sigma + ', t=' + '%4.2f'%self.t + ', nsteps=' + str(self.nsteps) +', ntrials=' + str(self.ntrials)
    
    
    
    
    def value(self):
        
        '''Method to calculate the value of an european put option using Monte Carlo Simulation.'''
        
        opt_values = []
        for i in range(self.ntrials):
            
            stk_prices = MCStockOption.generate_stock_prices(self)
        
            opt_values += [(max(self.x - stk_prices[-1] , 0 )) * math.exp(-1*self.r * self.t)]
            
        self.mean = statistics.mean(opt_values)
        self.stdev = statistics.pstdev(opt_values)
        
        return statistics.mean(opt_values)
    
    
   
    
# Asian Call option    
class MCAsianCallOption(MCStockOption):
    
    '''Defined a Monte Carlo Asian call option class.'''
    
    def __init__(self, s, x, r, sigma, t, nsteps, ntrials):
        
        '''Initialize a MCAsianCallOption object from MCStockOption class'''
        
        MCStockOption.__init__(self, s, x, r, sigma, t, nsteps, ntrials)
    
    
    
    def __repr__(self):
        
        '''Method to return a string representation of the object'''
        
        return 'MCAsianCallOption, s=' + '%4.2f'%self.s +', x=' + '%4.2f'%self.x + ', r=' + '%0.2f'%self.r +\
                ', sigma='+'%4.2f'%self.sigma + ', t=' + '%4.2f'%self.t + ', nsteps=' + str(self.nsteps) +', ntrials=' + str(self.ntrials)
    
    
    
    def value(self):
        
        '''Method to calculate the value of Asian call option using Monte Carlo Simulation.'''
        
        opt_values = []
        for i in range(self.ntrials):
            
            stk_prices = MCStockOption.generate_stock_prices(self)
            avg_stk_price = statistics.mean(stk_prices)
            opt_values += [(max(avg_stk_price - self.x, 0 )) * math.exp(-1*self.r * self.t)]
            
        self.mean = statistics.mean(opt_values)
        self.stdev = statistics.pstdev(opt_values)
        
        return statistics.mean(opt_values)
    
 
    
    
    
# Asian put option    
class MCAsianPutOption(MCStockOption):
    
    '''Defined a Monte Carlo Asian put option class.'''
    
    def __init__(self, s, x, r, sigma, t, nsteps, ntrials):
        
        '''Initialize a MCAsianPutOption object from MCStockOption class'''
        
        MCStockOption.__init__(self, s, x, r, sigma, t, nsteps, ntrials)
    
    
    def __repr__(self):
        
        '''Method to return a string representation of the object'''
        
        return 'MCAsianPutOption, s=' + '%4.2f'%self.s +', x=' + '%4.2f'%self.x + ', r=' + '%0.2f'%self.r +\
                ', sigma='+'%4.2f'%self.sigma + ', t=' + '%4.2f'%self.t + ', nsteps=' + str(self.nsteps) +', ntrials=' + str(self.ntrials)
    
    
    def value(self):
        
        '''Method to calculate the value of Asian put option using Monte Carlo Simulation.'''
        
        opt_values = []
        for i in range(self.ntrials):
            
            stk_prices = MCStockOption.generate_stock_prices(self)
            avg_stk_price = statistics.mean(stk_prices)
            opt_values += [(max(self.x - avg_stk_price , 0 )) * math.exp(-1*self.r * self.t)]
            
        self.mean = statistics.mean(opt_values)
        self.stdev = statistics.pstdev(opt_values)
        
        return statistics.mean(opt_values)






# Lookback call option
class MCLookbackCallOption(MCStockOption):
    
     '''Defined a Monte Carlo Lookback call option.'''
     
     def __init__(self, s, x, r, sigma, t, nsteps, ntrials):
        
        '''Initialize a MCALookbackCallOption object from MCStockOption class'''
        
        MCStockOption.__init__(self, s, x, r, sigma, t, nsteps, ntrials)
    
    
     def __repr__(self):
         
         '''Method to return a string representation of the object'''
        
         return 'MCLookbackCallOption, s=' + '%4.2f'%self.s +', x=' + '%4.2f'%self.x + ', r=' + '%0.2f'%self.r +\
                ', sigma='+'%4.2f'%self.sigma + ', t=' + '%4.2f'%self.t + ', nsteps=' + str(self.nsteps) +', ntrials=' + str(self.ntrials)
    
    
     def value(self):
         
         '''Method to calculate the value of look back call option using Monte Carlo simulation.'''
         
         opt_values = []
         for i in range(self.ntrials):
            
            stk_prices = MCStockOption.generate_stock_prices(self)
            max_stk_price = max(stk_prices)
            opt_values += [(max(max_stk_price - self.x, 0 )) * math.exp(-1*self.r * self.t)]
            
         self.mean = statistics.mean(opt_values)
         self.stdev = statistics.pstdev(opt_values)
        
         return statistics.mean(opt_values)




# Lookback Put option
class MCLookbackPutOption(MCStockOption):
    
    '''Defined a Monte Carlo Lookback put option.'''
    
    def __init__(self, s, x, r, sigma, t, nsteps, ntrials):
        
        '''Initialize a MCLookbackPutOption object from MCStockOption class'''
        
        MCStockOption.__init__(self, s, x, r, sigma, t, nsteps, ntrials)
    
    
    def __repr__(self):
        
        '''Method to return a string representation of the object'''
        
        return 'MCLookbackPutOption, s=' + '%4.2f'%self.s +', x=' + '%4.2f'%self.x + ', r=' + '%0.2f'%self.r +\
                ', sigma='+'%4.2f'%self.sigma + ', t=' + '%4.2f'%self.t + ', nsteps=' + str(self.nsteps) +', ntrials=' + str(self.ntrials)
    
    
    def value(self):
        
        '''Method to calculate the value of look back put option using Monte Carlo Simulation.'''
        
        opt_values = []
        for i in range(self.ntrials):
            
            stk_prices = MCStockOption.generate_stock_prices(self)
            max_stk_price = min(stk_prices)
            opt_values += [(max(self.x - max_stk_price , 0 )) * math.exp(-1*self.r * self.t)]
            
        self.mean = statistics.mean(opt_values)
        self.stdev = statistics.pstdev(opt_values)
        
        return statistics.mean(opt_values)
    
    
    
# Calculate run times for different trials    
def run_time():
    trials = [10, 100, 1000, 10000, 100000, 1000000]
    for i in range(len(trials)):
        start_time = time.time()
        call = MCEuroCallOption (100, 100, 0.1, 0.3, 1, 100, trials[i])
        call_value = MCEuroCallOption.value(call)
        call_std_err = MCStockOption.stderr(call)
        end_time = time.time()
        elapsed = end_time - start_time
        print("ntrials = ", trials[i ], "value = $",'%4.4f'%call_value,", stderr = $",'%4.8f'%call_std_err, ", time = ",'%4.4f'%elapsed)
            
            