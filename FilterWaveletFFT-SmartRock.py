# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 01:22:44 2020

@author: cheng
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
from scipy import signal

def getnames():
    global path
    path= 'Z:\\Projects\\BNSF\\data\\data sr\\total east\\test11'  #input('input the path:\n')
    filenames = os.listdir(path)
    return filenames

def cut(data):
    mean1=np.mean(data)
    std1=np.std(data)
    list1=np.where(data>=mean1+2*std1)
    start1=np.max([list1[0][0]-500,0])
    end1=np.min([list1[0][-1]+501,len(data)])
    range1=range(start1,end1)
    return range1

list1=[]
filenames=getnames()
peak=0.04
for name in filenames:
    if 'csv'and '20_02_27_15_37_Accel' in name:   #choose the files
        list1.append(name)

for file in list1:
    d1=open(path+'\\'+file)
    d=np.loadtxt(d1,dtype='float', delimiter=',' ,skiprows=5, usecols=(2,3,4) )
    s=np.size(d,0)
    
    a1=signal.detrend(d[0::,0])
    a2=signal.detrend(d[0::,1])
    a3=signal.detrend(d[0::,2])
    
    a11=a1[cut(a1)]
    a22=a2[cut(a2)]
    a33=a3[cut(a3)]
    
    #band filter
    sos = signal.butter(3, [0.1,20], 'bandpass', fs=50, output='sos')
    filtered3 = signal.sosfilt(sos, a33)
    filtered2 = signal.sosfilt(sos, a22)
    filtered1 = signal.sosfilt(sos, a11)

    #plot
    plotdata=filtered3[0:5000]
    t=np.arange(0,len(plotdata))/50
    plt.figure()
    plt.plot(t,plotdata, 'navy')
    plt.xlabel('Time [sec]')
#    plt.ylim(-0.2,0.2)
    plt.ylabel('Acceleration [g]')
    plt.grid(which='both', axis='y')
#    plt.savefig('C:\\Users\\cheng\\Desktop\\'+file+'zoom1.png', 
#                figsize=[8, 4.8],dpi=300, bbox_inches='tight')

    #Time FFT
#    fs=50  #Sampling frequency of the x time series
#    f1, t1, Zxx1 = signal.stft(filtered1, fs, nperseg=128)
#    f2, t2, Zxx2 = signal.stft(filtered2, fs, nperseg=80)
#    f3, t3, Zxx3 = signal.stft(filtered3, fs, nperseg=128)
#
#    X, Y = np.meshgrid(t2, f2)
#    Z=np.abs(Zxx2)
#    levels=20    
    #uniaxial plot
#    plt.figure()
#    plt.contourf(X, Y, Z, levels, cmap='hsv',vmin=0, vmax=0.04, extend='max')
#    plt.pcolormesh(t2, f2, np.abs(Zxx2),cmap='hsv',vmin=0, vmax=0.03)
    
#    plt.xlabel('Time, sec')
#    plt.ylabel('Frequency, Hz')
#    plt.ylim(0,20)
#    plt.colorbar(label='Acceleration',spacing='uniform',ticks=np.linspace(0,peak,levels+1))   
#    plt.savefig('C:\\Users\\cheng\\Desktop\\'+file+'.png',dpi=300)
#    plt.show() 


    #3D contour
#    fig = plt.figure(figsize=(8,6))
#    ax = fig.gca(projection='3d')    
#    ax.plot_surface(X, Y, Z, rstride=7, cstride=7, alpha=0.7)
#    cset = ax.contourf(X, Y, Z, zdir='z', offset=-0.02, cmap='hsv',vmin=0, vmax=0.04, alpha=1)
#    cset = ax.contourf(X, Y, Z, zdir='x', offset=0, cmap=cm.coolwarm)
#    cset = ax.contourf(X, Y, Z, zdir='y', offset=25, cmap=cm.coolwarm)    
#    ax.set_xlabel('Time, sec')
#    ax.set_xlim(0, t2[-1]+5)
#    ax.set_ylabel('Frequency, Hz')
#    ax.set_ylim(0, 20)
#    ax.set_zlabel('Acceleration, g')
#    ax.set_zlim(-0.02, peak)
#    plt.savefig('C:\\Users\\cheng\\Desktop\\'+file+'3D.png',dpi=300)
#    plt.show()
    
    
    #triaxial plot 
#    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
#    fig.suptitle('STFT Magnitude', ha='center', va='bottom')
#    
#    ax1.pcolormesh(t1, f1, np.abs(Zxx1))
#    ax1.set_ylim(0,25)
#    #ax1.set_ylabel('Frequency [Hz]')
#    
#    ax2.pcolormesh(t2, f2, np.abs(Zxx2))
#    ax2.set_ylim(0,25)
#    ax2.set_ylabel('Frequency [Hz]')
#    
#    ax3.pcolormesh(t3, f3, np.abs(Zxx3))
#    ax3.set_ylim(0,25)
#    #ax3.set_ylabel('Frequency [Hz]')
#    ax3.set_xlabel('Time [sec]')
#    
#    plt.savefig('C:\\Users\\cheng\\Desktop\\'+file+'.png',dpi=500)
    
    #Ricker wavelet
#    widths = np.arange(1, 25)
#    cwtmatr = signal.cwt(a33, signal.ricker, widths)
#    plt.figure()
#    plt.imshow(cwtmatr, cmap='hot', aspect='auto',
#                vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
#    plt.savefig('Z:\\Projects\\BNSF\\data\\analysis\\westdata_loading\\'+file+'wavelet.png',dpi=300)    
    