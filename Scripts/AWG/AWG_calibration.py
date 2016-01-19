# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 17:51:22 2015

@author: HatLab_Xi Cao
"""

#find DC offset for AWG

#import create_waveform
import qt
import numpy as np
import matplotlib.pyplot as plt
import create_waveform
from scipy.optimize import curve_fit



AWG = qt.instruments['AWG']
MXA = qt.instruments['MXA']


def offset_optimize(start,end,step,ch_num,minimum,offset):

    for x in np.arange(start,end,step):
        AWG.set_ch_offset(ch_num,x)
        qt.msleep(0.1)
        temp = MXA.marker_Y_value()
        
        if (minimum < temp):
            pass
        else:
            minimum = temp
            offset = x

    result = np.array(np.arange(0,5,1.0))
    result[0] = minimum
    result[1] = offset
    result[2] = step
    result[3] = offset - result[2]
    result[4] = offset + result[2]
    AWG.set_ch_offset(ch_num,offset)

    return result
    
def offset_calibration():

    minimum = 0.0 
    result = [0.0,0.0]
    
    while (minimum > -60):
        temp1=np.array(range(0,5))
        temp1=[0.0,0.0,0.1,-2.2,2.3]
        temp2=temp1
        step1=0.1
    
        while (step1>=0.001):
            
            for x in range(0,5):
                temp1 = offset_optimize(temp1[3],temp1[4],temp1[2],1,minimum,temp1[1])
                temp2 = offset_optimize(temp2[3],temp2[4],temp2[2],2,minimum,temp2[1])
                minimum = min(temp1[0],temp2[0])
                       
            result[0] = temp1[1]
            result[1] = temp2[1]            
            
            temp1[2] = temp1[2]/10.0
            temp1[3] = temp1[1] - 10.0*temp1[2]
            temp1[4] = temp1[1] + 11.0*temp1[2]
            
            temp2[2] = temp2[2]/10.0
            temp2[3] = temp2[1] - 10.0*temp2[2]
            temp2[4] = temp2[1] + 11.0*temp2[2]
            
            step1 = temp1[2]
    
    return result
    
    
def ampratio_optimize(start=0.2,end=4.501,step=0.01,minimum = 0.0,ch2_amp=1.0):    
    
    AWG.set_ch2amp(ch2_amp)
    length = len(np.arange(start,end,step))
    result = np.zeros((3,length))
    temp = 0
    
    for x in np.arange(start,end,step):
        AWG.set_ch1amp(x)
        qt.msleep(0.1)
        result[0][temp] = x/ch2_amp
        result[1][temp] = MXA.marker_Y_value()
        
        
        if (minimum<result[1][temp]):
            pass
        else:
            minimum = result[1][temp]
            ratio = result[0][temp]
            ch1_amp = x

        temp = temp + 1        
        
    result[2][0] = minimum
    result[2][1] = ratio
    result[2][2] = ch1_amp
    
    AWG.set_ch1amp(ch2_amp*ratio)
    return result


def skew_optimize(start=-5.0,end=5.001,step=0.1,minimum = 0.0):
    
    skewtime = 0.0
    
    for x in np.arange(start,end,step):
        AWG.set_ch1skew(x)
        qt.msleep(0.1)
        temp = MXA.marker_Y_value()

        if (minimum < temp):
            pass
        else:
            minimum = temp
            skewtime = x
        
    AWG.set_ch1skew(skewtime)
    return skewtime
    
    
def amp_skew_calibration():
    start1 = 0.2
    end1 = 4.51
    step1 = 0.1
    minimum1 = 0.0

    start2 = -5.0
    end2 = 5.1
    step2 = 0.1 
   

    
    for x in range(0,2):
        
        for y in range(0,3):
            result = ampratio_optimize(start1,end1,step1,minimum1)
            result[2][3] = skew_optimize(start2,end2,step2,minimum1)
        
        minimum1 = result[2][0]
        
       
        start1 = result[2][2] - step1
        end1 = result[2][2] + step1
        step1 = step1/10.0
        
        start2 = result[2][3] - step2
        end2 = result[2][3] + step2
        step2 = step2/10.0
        
        '''
        print start1
        print 'hahaha'
        print start2
        '''
    return result

def sideband(center_freq,sideband_freq,marker_value,markernum,sideband='up'):
    center_freq = center_freq*1E9
    sideband_freq = sideband_freq*1E9
    up_side = center_freq + sideband_freq
    down_side = center_freq - sideband_freq
    test = False    
    
    while (test == False):
        marker_center = np.abs(marker_value - center_freq)

        if (sideband == 'up'):
            marker_sideband = np.abs(marker_value - up_side)
            if (marker_center > marker_sideband):
                test = True
            else:     
                MXA.next_peak_right()
                qt.msleep(0.1)
                marker_value = MXA.marker_X_value()
        
        if (sideband == 'down'):
            marker_sideband = np.abs(marker_value - down_side)
            if (marker_center > marker_sideband):
                test = True
            else:             
                MXA.next_peak_left()
                qt.msleep(0.1)
                marker_value = MXA.marker_X_value()
'''                
def offset(start,end,step,ch_num):
    result = np.zeros(len(np.arange(start,end,step)))
    temp = 0
    
    for x in np.arange(start,end,step):
        AWG.set_ch_offset(ch_num,x)
        qt.msleep(0.1)
        result[temp] = MXA.marker_Y_value()
        temp = temp + 1
        
    return result

def amp_ratio(start,end,step,ch2_amp):
    
    result = np.zeros((2,len(np.arange(start,end,step))))    
    temp = 0    
    AWG.set_ch2amp(ch2_amp)
    
    for x in np.arange(start,end,step):
        AWG.set_ch1amp(x)
        qt.msleep(0.1)
        result[0][temp] = x/ch2_amp
        result[1][temp] = MXA.marker_Y_value()        
        temp = temp + 1
        
    return result
        
def skew(start,end,step):
    result = np.zeros(len(np.arange(start,end,step)))
    temp = 0
    
    for x in np.arange(start,end,step):
        AWG.set_ch1skew(x)
        qt.msleep(0.1)
        result[temp] = MXA.marker_Y_value()
        temp = temp + 1
        
    return result
    
    
def ratio_fitfunc(x, c, x0, d, e):

    return c*np.power((x-x0),2)+d+e*(x-x0)
      

def skew_fitfunc(x,k,b):
    
    return k*x + b

def datafit(xdata,ydata,fit_type):
    
    if (fit_type == 'ratio'):
        popt, pcov = curve_fit(ratio_fitfunc, xdata, ydata)
        best_value = (2*popt[0]*popt[1] - popt[3])/(2*popt[0])
        return best_value    
    elif (fit_type == 'skew'):
        popt, pcov = curve_fit(skew_fitfunc, xdata, ydata)
        if(popt[0] > 0):
            best_value = min(xdata)
        elif(popt[0] < 0):
            best_value = max(xdata)
        return best_value
       

def calibration_fit(center_freq,sideband_freq):

        
    create_waveform.sinwave('test_sin',1000,'yes')      #create sin and cos wave for I and Q signal
    create_waveform.coswave('test_cos',1000,'yes')      
    AWG.addwaveform_nonseq(1,'test_sin')                #add the waveform to the channels
    AWG.addwaveform_nonseq(2,'test_cos')
    qt.msleep(1)
    AWG.channel_on(1)                                   #turn on the channels
    AWG.channel_on(2)            
    AWG.run()                                           #turn on the AWG    
    MXA.marker_off(markernum)    
    MXA.new_peak(markernum)                             #put a marker on the peak for the calibration
    marker_value = MXA.marker_X_value(markernum)    
    sideband(center_freq,sideband_freq,marker_value,markernum,'up')
    
    ratio = 0.0
    skew = 0.0
    ch2_amp = 1.0

    while ():
        ratio_result = amp_ratio(0.2,4.51,0.1,ch2_amp)
        ratio = datafit(ratio_result[0][...],ratio_result[1][...],'ratio')
        AWG.set_ch1amp(ch2_amp*ratio)
        skew_result = skew(-5.0,5.1,0.1)
'''


        
def calibration_min(center_freq,sideband_freq):
    #Input is frequency in GHz
    markernum = 1
    MXA.marker_off(markernum)
    result = np.zeros((1,4))
    #First, do the calibration for DC offset
    create_waveform.waitblock('zeropulse',1000,0,'yes') #create zero value pulse for I and Q signal
    AWG.addwaveform_nonseq(1,'zeropulse')               #add the waveform to the channels
    AWG.addwaveform_nonseq(2,'zeropulse')
    qt.msleep(1)
    AWG.channel_on(1)                                   #turn on the channels
    AWG.channel_on(2)
    AWG.run()                                           #turn on the AWG    
    MXA.marker_off(markernum)    
    MXA.new_peak(markernum)                             #put a marker on the peak for the calibration
    result[0][(range(0,2))] = offset_calibration()                                #do the calibration
    MXA.marker_off(markernum)                           #turn off the marker
    AWG.stop()                                          #turn off the AWG
     
    #Then, do the calibration for Amplitude ratio and skew time  
    create_waveform.sinwave('test_sin',1000,'yes')      #create sin and cos wave for I and Q signal
    create_waveform.coswave('test_cos',1000,'yes')      
    AWG.addwaveform_nonseq(1,'test_sin')                #add the waveform to the channels
    AWG.addwaveform_nonseq(2,'test_cos')
    qt.msleep(1)
    AWG.channel_on(1)                                   #turn on the channels
    AWG.channel_on(2)            
    AWG.run()                                           #turn on the AWG    
    MXA.marker_off(markernum)    
    MXA.new_peak(markernum)                             #put a marker on the peak for the calibration
    marker_value = MXA.marker_X_value(markernum)    
    sideband(center_freq,sideband_freq,marker_value,markernum,'up')
    temp = amp_skew_calibration()
    result[0][2] = temp[2][1]
    result[0][3] = temp[2][3]
    
    plt.plot(temp[0][...],temp[1][...])  
    plt.show()
    
    return result



    
    