# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 11:20:58 2015

@author: HatLab_Xi Cao
"""

#test default value
'''
def test(a=1,b=2):
    print a
    print b
    


test(a,2)
'''

'''
import numpy as np
from scipy.optimize import fmin
import math

def f(x):
    exp = (math.pow(x[0], 2) + math.pow(x[1], 2)) * -1
    return math.exp(exp) * math.cos(x[0] * x[1]) * math.sin(x[0] * x[1])

fmin(f,np.array([0,0]))
'''




import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
#import AWG_calibration
import hdf5_data as h5


test = h5.HDF5Data(filepath=r"C:\Users\HatLab_Xi Cao\Box Sync\Programming\AWG\\" , name='fittest1')

length = len(np.arange(0.2,4.51,0.1))
data = test['/fit data'].value
data_ratio = data[0,...]
data_power_dB = data[1,...]

data_power_linear = np.power(10.0,data_power_dB/10.0)

print data_ratio
print data_power_linear

def func(x, a, b):
    return a*(np.power(x,2)+2*b*x+1)
    
xdata = data_ratio
ydata = data_power_linear
#ydata = y + 0.2 * np.random.normal(size=len(xdata))


popt, pcov = curve_fit(func, xdata, ydata)

print popt
print pcov

plt.plot(xdata,ydata)
plt.show()

test.close()