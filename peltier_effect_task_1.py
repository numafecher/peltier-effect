"Code to acquire data on AI channel 0"

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
    
        
fig=plt.figure(figsize=(7,5))

# Button to stop acquisition
offax=plt.axes([0.83,0.75,0.1,0.1])
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

# prepare the graph
ax1=plt.axes([0.2,0.55,0.55,0.35])
ax2=plt.axes([0.2, 0.1, 0.55, 0.35])

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

    newx = x1-x0+np.mean(timestamps) # time elapsed in seconds
    newy = np.mean(voltage)   # measured voltage at time x
    newsy = np.std(voltage)/np.sqrt(a.Nscans) # standard error of mean
    
    newuppt = np.mean(upptemp)
    newsuppt = np.std(upptemp)/np.sqrt(a.Nscans)
    
    newlowt = np.mean(lowtemp)
    newslowt = np.std(lowtemp)/np.sqrt(a.Nscans)

    newcurr = np.mean(current)
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
    
    ax1.clear()
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Amplitude (Volts)')
    #ax1.errorbar(x,y,yerr=sy,fmt='b.')
    ax1.plot(x, y)
    
    ax2.clear()
    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylabel('Temperature Difference (kelvin)')
    #ax2.errorbar(x, tempdiff, yerr=stempdiff, fmt='b.')
    ax2.plot(x, tempdiff)