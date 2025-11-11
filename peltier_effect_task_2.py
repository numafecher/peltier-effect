# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 10:07:22 2025

@author: pcynf3
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as w
import time
import sys
sys.path.insert(1,"C:\\python")
import y2daq


def switchoffCallback(event):
    """ Callback function for button to switch off loop """
    global switchon
    global Voff
    switchon = False;
    print('switched off')
    
plt.figure(1, figsize=(11, 7))

axes1 = plt.axes([0.1, 0.6, 0.35, 0.3])
line1, = axes1.plot(0, 0, 'b-')
axes1.set_xlabel('Time (seconds)')
axes1.set_ylabel('Current (A)')

axes2 = plt.axes([0.1, 0.15, 0.35, 0.3])
line2, = axes2.plot(0, 0, 'r-')
axes2.set_xlabel('Time (seconds)')
axes2.set_ylabel('Voltage (V)')

axes3 = plt.axes([0.55, 0.6, 0.35, 0.3])
line3, = axes3.plot(0, 0, 'k-')
axes3.set_xlabel('Time (seconds)')
axes3.set_ylabel('Temperature Difference (K)')

#axes4 = plt.axes([0.55, 0.15, 0.35, 0.3])
#line4, = axes4.plot(0, 0, 'g-')
#axes4.set_xlabel('Time')
#axes4.set_ylabel('Signal')

# Button to stop acquisition
offax=plt.axes([0.65,0.25,0.1,0.1])
offHandle=w.Button(offax,'off')
offHandle.on_clicked(switchoffCallback) 

# 0-Temp upper  1-Temp lower  2-Voltage  3-Current
a = y2daq.analog() # create analog data acquisition object
a.addInput(0) #Temp upper
a.addInput(1) #Temp lower
a.addInput(2) #Voltage
a.addInput(3) #Current
a.Nscans = 500 # no. of points per acquisition
a.Rate = 1000 # no. of points per second

# initialize arrays
y=np.array([])
sy=np.array([])
x=np.array([])
uppt=np.array([])
suppt=np.array([])
lowt=np.array([])
slowt=np.array([])
curr=np.array([])
scurr=np.array([])
tempdiff=np.array([])
stempdiff=np.array([])

x0 = time.time()
switchon = True

# acquisition loop
while switchon == True:
    # acquire and plot data
    x1=time.time()
    data,timestamps = a.read() # acquire data from generator
    upptemp = data[:1]
    lowtemp = data[1:2]
    voltage = data[2:3]
    current = data[3:4]

    # finding mean of each variable
    newx = x1-x0+np.mean(timestamps) # time elapsed in seconds
    newy = np.mean(voltage)   # measured voltage at time x
    newsy = np.std(voltage)/np.sqrt(a.Nscans) # standard error of mean
    
    newuppt = np.mean((upptemp*100)+273.15)
    newsuppt = np.std(upptemp)/np.sqrt(a.Nscans)
    
    newlowt = np.mean((lowtemp*100)+273.15)
    newslowt = np.std(lowtemp)/np.sqrt(a.Nscans)

    newcurr = np.mean((current*10))
    newscurr = np.std(current)/np.sqrt(a.Nscans)
    
    newtempdiff = newuppt - newlowt
    newstempdiff = np.sqrt(newsuppt**2 + newslowt**2)

    
    
    plt.pause(0.5)
    
    # append data to arrays
    x = np.append(x,newx)  
    y = np.append(y,newy)  
    sy = np.append(sy,newsy)
    uppt = np.append(uppt, newuppt)
    suppt = np.append(uppt, newsuppt)
    lowt = np.append(lowt, newlowt)
    slowt = np.append(lowt, newslowt)
    curr = np.append(curr, newcurr)
    scurr = np.append(scurr, newscurr)
    tempdiff = np.append(tempdiff, newtempdiff)
    stempdiff = np.append(stempdiff, newstempdiff)
    
    # plot data sets
    line1.set_xdata(x)
    line1.set_ydata(curr)
    axes1.relim()
    axes1.autoscale()
 
    line2.set_xdata(x)
    line2.set_ydata(y)
    axes2.relim()
    axes2.autoscale()
 
    line3.set_xdata(x)
    line3.set_ydata(tempdiff)
    axes3.relim()
    axes3.autoscale()