# -*- coding: utf-8 -*-
"""
Created on Wed May 20 00:02:41 2020

This program is used to extract data segments with peaks

@author: cheng
"""

import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
import datetime
import sys, os


def dateparse(x):
    t = x.split(':')
    t[-1] = t[-1].zfill(3)
    time = ':'.join(t)
    return datetime.datetime.strptime(time, '%m:%d:%H:%M:%S:%f')

class cut_signal:
    def __init__(self, keyword, column, windows, a, dist, margin, euler=None):
        self.keyword = keyword
        self.column = column
        self.windows = windows
        self.dist = dist
        self.margin = margin
        self.a = a
        self.euler = euler
          
    def FindPeaks(self, signals):
        mean_line = signals.rolling(self.windows, min_periods=1).mean().to_numpy()
        std_line = signals.rolling(self.windows, min_periods=1).std().to_numpy()
        height_line = mean_line+self.a*std_line
        peaks, _ = signal.find_peaks(signals.to_numpy(), distance=self.dist, height=height_line)
        return peaks, height_line
        
    def LoadFiles(self, path, name=None, path_save=None):
        #build up name list
        name_list = []
        count_keyword = 0
        count_euler = 0
            
        if name:
            name_list.append(name)
            
        else:
            name_list = os.listdir(path)
            n = len(name_list)
            
            if n > 0:
                i = 0
                while i < n:
                    name = name_list.pop(0)
                    i += 1
                        
                    if self.keyword in name:
                        name_list.append(name)
                        count_keyword += 1
                        
                    elif self.euler in name:
                        count_euler += 1
                        
            else:
                print('error: check "keyword" or "path"')
        
        if len(name_list) <= 0:
            print('error: check "keyword" or "path"')
            
        if self.euler:
            if count_keyword != count_euler:
                print('error: check euler files')
            
        return name_list
            
    def __call__(self, name_list, detrend=None):
        # read data
        for i in name_list:
            index_f = []
            index_b = []
            data = pd.read_csv(path+i, parse_dates=['Month:Day:Hr:Min:Sec:MSec'], date_parser=dateparse)
            euler = pd.read_csv(path+i.replace(self.keyword, self.euler), parse_dates=['Month:Day:Hr:Min:Sec:MSec'], date_parser=dateparse)
            
            if detrend:
                sig = detrend(data.iloc[:, self.column])
                sig = pd.DataFrame(sig).iloc[:,0]
            else:
                sig = data.iloc[:, self.column]
                
            n = len(sig)
            peaks, _ = cut_signal.FindPeaks(self, sig)
            
            if len(peaks) <= 0:
                print("Didn't find peaks in {}".format(i))
            
            else:
                plt.figure()
                sig.plot(title=i)
                # plt.plot(height)
                plt.plot(peaks, sig[peaks], '*')
                
                for p in peaks:
                    x_f = max([0, p-self.margin[0]])
                    x_b = min([n, p+self.margin[1]])
                    index_f.append(x_f)
                    index_b.append(x_b)
                    
                    #plot data
                    plt.figure()
                    sig.iloc[x_f:x_b].plot(title=i.replace('.csv', '_{}.csv'.format(x_f)))
                    
                    #save data
                    data.iloc[x_f:x_b, :].to_csv(path_save+i.replace('.csv', '_{}.csv'.format(x_f)), 
                                                 date_format = '%m:%d:%H:%M:%S:%f', index=False)
                    euler.iloc[x_f:x_b, :].to_csv(path_save+i.replace(self.keyword, self.euler).replace('.csv', '_{}.csv'.format(x_f)), 
                                                 date_format = '%m:%d:%H:%M:%S:%f', index=False)
                    
                    print('save:'+i.replace('.csv', '_{}.csv'.format(x_f)))
        return index_f, index_b                      

a=10 #the factors of limit
dist= 50    #set the distance between two peaks
windows= 500 #moving average windows
margin=[40, 40] #the left and right margin of cutting
plot1='on'  #on or off

path = 'Z:\\Projects\\CIAMTIS SR\\SmartModulus\\Field test 07102020\\10072020\\'
path_save = 'Z:\\Projects\\CIAMTIS SR\\SmartModulus\\Field test 07102020\\10072020\\10072020seperated\\'
name = 'LoggedData_HT03_20_10_07_16_03_Stress.csv'
keyword ='Stress'
euler = 'Quaternion'
column = 2
detrend = signal.detrend

cut = cut_signal(keyword, column, windows, a, dist, margin, euler=euler)

name_list = cut.LoadFiles(path, path_save=path_save)

in_f, in_b = cut(name_list, detrend)
