# -*- coding: utf-8 -*-
"""
Created on Tue Dec 01 18:27:24 2015

@author: HatLab_Xi Cao
"""
import qt
import numpy as np
import matplotlib.pyplot as plt
import create_waveform
from scipy.optimize import curve_fit
import operator

AWG = qt.instruments['AWG']
MXA = qt.instruments['MXA']


def offset(start,end,step,ch_num):
    result = np.zeros((2,len(np.arange(start,end,step)))) 
    temp = 0
    
    for x in np.arange(start,end,step):
        AWG.set_ch_offset(ch_num,x)
        qt.msleep(0.1)
        result[0][temp] = x
        result[1][temp] = MXA.marker_Y_value()
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
    result = np.zeros((2,len(np.arange(start,end,step)))) 
    temp = 0
    
    for x in np.arange(start,end,step):
        AWG.set_ch1skew(x)
        qt.msleep(0.1)
        result[0][temp] = x
        result[1][temp] = MXA.marker_Y_value()
        temp = temp + 1
        
    return result
    
    
def ratio_fitfunc(x, c, x0, d, e):

    return c*np.power((x-x0),2)+d+e*(x-x0)
      

def skew_fitfunc(x,k,b,c):
    sideband_freq = 0.01
    return k*np.cos(sideband_freq*(x-c)) + b
        









def datafit(xdata,ydata,fit_type):
    ydata = np.power(10.0,ydata/10.0)
    length = len(xdata)
    center,minmum = min(enumerate(ydata),key = operator.itemgetter(1))
    low_bound = max(center-length/10,0)
    up_bound = min(center+length/10,len(ydata))
    
    xdata1 = xdata[low_bound:up_bound]
    ydata1 = ydata[low_bound:up_bound]
    
    if (fit_type == 'ratio'):

        popt, pcov = curve_fit(ratio_fitfunc, xdata1, ydata1)
        best_value = (2*popt[0]*popt[1] - popt[3])/(2*popt[0])
        ch2_amp = AWG.get_ch2amp()
        qt.msleep(0.1)
        AWG.set_ch1amp(ch2_amp*best_value)
        qt.msleep(0.1)        
 
    elif (fit_type == 'skew'):
       
        popt, pcov = curve_fit(skew_fitfunc, xdata1, ydata1)
        best_value = popt[2]
        AWG.set_ch1skew(best_value)
        qt.msleep(0.1)
        
    elif (fit_type == 'offset'):
        
        popt, pocv = curve_fit(ratio_fitfunc,xdata1,ydata1)
        best_value = (2*popt[0]*popt[1] - popt[3])/(2*popt[0])
        
        
        
    return best_value

'''
def ratio_skew_calibration(ch2_amp):
    
    ratio_start = 0.2
    ratio_end = 4.51
    ratio_step = 0.1
    
    skew_start = -5.0
    skew_end = 5.1
    skew_step = 0.1
    
    while (test = True):
        
        ratio_result = amp_ratio(ratio_start,4.51,0.1,ch2_amp)
        ratio = datafit(ratio_result[0][...],ratio_result[1][...],'ratio')
        AWG.set_ch1amp(ch2_amp*ratio)        
'''




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
        

def calibration_fit(center_freq,sideband_freq):
    markernum = 1
    test = True
    
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

  
    while (test == True):
        
        
        offset1_result = offset(-2.2,2.3,0.1,1)
        offset1 = datafit(offset1_result[0][...],offset1_result[1][...],'offset')
        AWG.set_ch_offset(1,offset1)
        qt.msleep(0.1)

        offset2_result = offset(-2.2,2.3,0.1,2)
        offset2 = datafit(offset2_result[0][...],offset2_result[1][...],'offset')
        AWG.set_ch_offset(2,offset2)
        qt.msleep(0.1)
        marker_value = MXA.marker_Y_value()

        if (marker_value < -75):     
            test = False



    MXA.marker_off(markernum)                           #turn off the marker

    AWG.stop()                                          #turn off the AWG
     
   
   #start ratio and skew calibration:
            
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
    skew_time = 0.0
    ch2_amp = 1.0
    test = True
    
    while (test == True):
        
        
        ratio_result = amp_ratio(0.2,4.51,0.1,ch2_amp)
        ratio = datafit(ratio_result[0][...],ratio_result[1][...],'ratio')
        
        #if you are using skew calibration, please change the sideband_freq in functon skew_fitfunc
        skew_result = skew(-5.0,5.1,0.1)
        skew_time = datafit(skew_result[0][...],skew_result[1][...],'skew')
        marker_value = MXA.marker_Y_value()

        
        #if (((np.fabs(temp1-ratio)<0.001)&(np.fabs(temp2-skew_time)<0.003))|(marker_value<-70)):
        if (marker_value < -75):     
            test = False
     
    print 'best offset for ch1 is %f' % offset1
    print 'best offset for ch2 is %f' % offset2
    print 'best ratio is %f' % ratio
    print 'best skew time is %f' % skew_time
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        