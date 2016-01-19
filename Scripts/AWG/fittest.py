# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 16:39:14 2015

@author: HatLab_Xi Cao
"""
import numpy as np
import hdf5_data as h5
import AWG_fit_calibration
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import operator

'''
test = h5.HDF5Data(filepath=r"C:\Users\HatLab_Xi Cao\Box Sync\Programming\AWG\\" , name='fittest1')
#result = AWG_calibration.ampratio_optimize(0.2,4.51,0.1,0.0,1.0)
result = AWG_fit_calibration.skew(-5,5.1,0.1)
length = len(np.arange(-5.0,5.1,0.1))
fit_data = test.create_dataset('fit data',(2,length),'d')
fit_data[...] = result
test.close()
'''
#result = AWG_calibration.ampratio_optimize(0.2,4.51,0.01,0.0,1.0)

test = h5.HDF5Data(filepath=r"C:\Users\HatLab_Xi Cao\Box Sync\Programming\AWG\\" , name='fittest1')

length = len(np.arange(-5.0,5.1,0.1))
data = test['/fit data'].value
xdata = data[0,...]
ydata = data[1,...]


def func(x, c, x0, d, e):
    #return a*np.power(x,2)+b*x+a
    return c*np.power((x-x0),2)+d+e*(x-x0)
    
def skew_fitfunc(x,k,b,c):
    sideband_freq = 0.01
    return k*np.cos(2*np.pi*sideband_freq*(x+c)) + b
    
    
ydata = np.power(10.0,ydata/10.0)
#ydata = y + 0.2 * np.random.normal(size=len(xdata))
'''
center,minmum = min(enumerate(ydata),key = operator.itemgetter(1))
xdata1 = xdata[center-length/10:center+length/10]
ydata1 = ydata[center-length/10:center+length/10]
popt,pcov = curve_fit(func, xdata1, ydata1)
'''

center,minmum = min(enumerate(ydata),key = operator.itemgetter(1))
low_bound = max(center-length/10,0)
up_bound = min(center+length/10,len(ydata))
    
xdata1 = xdata[low_bound:up_bound]
ydata1 = ydata[low_bound:up_bound]
xdata1 = xdata
ydata1 = ydata 


phase = 2*np.pi*xdata1*0.01
temp = phase
popt, pcov = curve_fit(skew_fitfunc, xdata1, ydata1)
if(popt[0] > 0):
    index,minmum = min(enumerate(temp),key = operator.itemgetter(1))
    best_value = xdata[index]
elif(popt[0] < 0):
    index,maxmum = max(enumerate(temp),key = operator.itemgetter(1))
    best_value = xdata[index]





print popt
#print pcov
#print (2*popt[0]*popt[1] - popt[3])/(2*popt[0])
print best_value
#plt.plot(np.cos(2*np.pi*0.01*xdata1),2.5*np.cos(2*np.pi*0.01*xdata1)+2.5625,'*k')

#yfit = popt[0]*np.power((xdata-popt[1]),2)+popt[3]*(xdata-popt[1])+popt[2]

yfit = popt[0]*np.cos(2*np.pi*0.01*(xdata1+popt[2])) + popt[1]

#yfit = np.cos(2*np.pi*0.01*xdata1)

print 'min y data is %f ' % min(ydata)
print 'min y fit is %f ' % min(yfit)


temp = np.cos(2*np.pi*0.01*xdata1)
plt.plot(xdata1,ydata1,'k*')
plt.plot(xdata1,yfit)
#plt.plot(temp,ydata1)
#plt.plot(xdata,0.01*np.cos(2*np.pi*0.01*xdata1),'k')
#plt.axis([1, 2, -0.0002, 0.0005])
plt.show()













