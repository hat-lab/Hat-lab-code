# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 11:26:57 2015

@author: HatLab_Xi Cao
"""

#create different waveforms
import qt
import numpy as np
import struct


AWG = qt.instruments['AWG']

def test():
    print 'test'

def pi_pulse(pulsename,pointnum,rabifreq,overwrite = 'no'):
    #create a gaussian wave in AWG waveform list that can be used as a pi pulse
    #input: name of the waveform (string), number of points in the wave (int)
    #       Rabi frequency of the system

    
    #create an array with size of pointnum to store the value of each point in the desired waveform    
    wavedata = np.array(range(0,pointnum))
    #set the No. of point that is needed to turn on the marker
    markerdata = np.array(range(0,pointnum*60/100))

    #calculate the parameter we need to create the wave
    sigma = (rabifreq/np.pi)/2.35482
    #calculate the value of each point and store it in the wavedata
    wavedata = (1/(sigma*np.sqrt(2*np.pi)))*np.exp(-1.0*np.power(((wavedata-(pointnum*4/5))/sigma),2)/2.0)

    #calculate the parameter to create a waveform in AWG
    length = len(wavedata)
    length_digits = len(str(2*length))
    header_string = '#' + str(length_digits) + str(2*length)
    
    
    wavename =  '"%s",' % pulsename + str(length) +',INTEGER' 
    wavestr = '"%s"' % pulsename + ',0,' + str(length) + ',' + header_string
 
    #The following is for integer waveform, change the value of each point into integer form
    vmax = 1/(sigma*np.sqrt(2*np.pi))
    wavedata = (wavedata+vmax)*16383.0/(2.0*vmax)
    #Add the marker
    for x in range(0,len(markerdata)):
        wavedata[markerdata[x]] = wavedata[markerdata[x]] + 16384 #This is to turn on the marker1 to turn marker 2, add 2^15
    

    
    for x in range(0,length):
            wavestr = wavestr + struct.pack('<H',int(wavedata[x]))
            #print int(wavedata[x])
            
    if (overwrite == 'yes'):
        AWG.deletewaveform(pulsename)
    else:
        pass
    
    AWG.newwaveform(wavename)
    AWG.setwaveform(wavestr)
    
    
def halfpi_pulse(pulsename,pointnum,rabifreq,overwrite = 'no'):
    #create a gaussian wave in AWG waveform list that can be used as a pi pulse
    #input: name of the waveform (string), number of points in the wave (int)
    #       Rabi frequency of the system

    
    #create an array with size of pointnum to store the value of each point in the desired waveform    
    wavedata = np.array(range(0,pointnum))

    #calculate the parameter we need to create the wave
    sigma = (rabifreq/(0.5*np.pi))/2.35482
    #calculate the value of each point and store it in the wavedata
    wavedata = (1/(sigma*np.sqrt(2*np.pi)))*np.exp(-1.0*np.power(((wavedata-(pointnum/2))/sigma),2)/2.0)

    #calculate the parameter to create a waveform in AWG
    length = len(wavedata)
    length_digits = len(str(2*length))
    header_string = '#' + str(length_digits) + str(2*length)
    
    
    wavename =  '"%s",' % pulsename + str(length) +',INTEGER' 
    wavestr = '"%s"' % pulsename + ',0,' + str(length) + ',' + header_string
 
    #The following is for integer waveform
    vmax = 1/(sigma*np.sqrt(2*np.pi))
    wavedata = (wavedata+vmax)*16383.0/(2.0*vmax)
    

    
    for x in range(0,length):
            wavestr = wavestr + struct.pack('<H',int(wavedata[x]))
            #print int(wavedata[x])

    if (overwrite == 'yes'):
        AWG.deletewaveform(pulsename)
    else:
        pass
    
    AWG.newwaveform(wavename)
    AWG.setwaveform(wavestr)
    
    
  
def testtrigger(pulsename,pointnum,rabifreq,overwrite = 'no'):
    #create a gaussian wave in AWG waveform list that can be used as a pi pulse
    #input: name of the waveform (string), number of points in the wave (int)
    #       Rabi frequency of the system

    
    #create an array with size of pointnum to store the value of each point in the desired waveform    
    wavedata = np.array(range(0,pointnum))
    #set the No. of point that is needed to turn on the marker
    #markerdata = np.array(range(0,pointnum*5/100))
    length = len(wavedata)
    
    wavedata = np.sin(2*np.pi*wavedata*10/length)*np.exp(-wavedata/200)
    #print wavedata

    #calculate the parameter to create a waveform in AWG
    
    length_digits = len(str(2*length))
    header_string = '#' + str(length_digits) + str(2*length)
    
    
    wavename =  '"%s",' % pulsename + str(length) +',INTEGER' 
    wavestr = '"%s"' % pulsename + ',0,' + str(length) + ',' + header_string
 
    #The following is for integer waveform, change the value of each point into integer form
    vmax = 1
    wavedata = (wavedata+vmax)*16383.0/(2.0*vmax)
    #Add the marker
    '''
    for x in range(0,len(markerdata)):
        wavedata[markerdata[x]] = wavedata[markerdata[x]] + 16384 #This is to turn on the marker1 to turn marker 2, add 2^15
    '''

    
    for x in range(0,length):
            wavestr = wavestr + struct.pack('<H',int(wavedata[x]))
            #print int(wavedata[x])
 
    if (overwrite == 'yes'):
        AWG.deletewaveform(pulsename)
    else:
        pass

           
    AWG.newwaveform(wavename)
    AWG.setwaveform(wavestr)
    
    
def waitblock(pulsename,pointnum,DCoffset,overwrite = 'no'):
    #create a blcok that is used for wait
    wavedata = np.array(range(0,pointnum))
    wavedata = 0.0*wavedata + DCoffset




    length = len(wavedata)
    length_digits = len(str(2*length))
    header_string = '#' + str(length_digits) + str(2*length)
        
    wavename =  '"%s",' % pulsename + str(length) +',INTEGER' 
    wavestr = '"%s"' % pulsename + ',0,' + str(length) + ',' + header_string
    
#    markerdata = np.arange(pointnum*8/10,pointnum*9/10)
    
    vmax = 1+DCoffset 
    wavedata = (wavedata+vmax)*16383.0/(2.0*vmax)
 
    
#    for x in range(0,len(markerdata)):
#        wavedata[markerdata[x]] = wavedata[markerdata[x]] + 16384 #This is to turn on the marker1 to turn marker 2, add 2^15


    for x in range(0,length):
            wavestr = wavestr + struct.pack('<H',int(wavedata[x]))
            #print int(wavedata[x])

    if (overwrite == 'yes'):
        AWG.deletewaveform(pulsename)
    else:
        pass

            
    AWG.newwaveform(wavename)
    AWG.setwaveform(wavestr)

def waitblock_marker(pulsename,pointnum,DCoffset,overwrite = 'no'):
    #create a blcok that is used for wait
    wavedata = np.array(range(0,pointnum))
    wavedata = 0.0*wavedata + DCoffset




    length = len(wavedata)
    length_digits = len(str(2*length))
    header_string = '#' + str(length_digits) + str(2*length)
        
    wavename =  '"%s",' % pulsename + str(length) +',INTEGER' 
    wavestr = '"%s"' % pulsename + ',0,' + str(length) + ',' + header_string
    
    markerdata = np.arange(pointnum*8/10,pointnum*9/10)
    
    vmax = 1+DCoffset 
    wavedata = (wavedata+vmax)*16383.0/(2.0*vmax)
 
    
    for x in range(0,len(markerdata)):
        wavedata[markerdata[x]] = wavedata[markerdata[x]] + 16384 #This is to turn on the marker1 to turn marker 2, add 2^15


    for x in range(0,length):
            wavestr = wavestr + struct.pack('<H',int(wavedata[x]))
            #print int(wavedata[x])

    if (overwrite == 'yes'):
        AWG.deletewaveform(pulsename)
    else:
        pass

            
    AWG.newwaveform(wavename)
    AWG.setwaveform(wavestr)


def sinwave(pulsename,pointnum,freq,amp,phase,overwrite = 'no'):
    # Create a sine wave
    # Input: name of the sine wave (string)
    #        number of points of the waveform (int)
    #        frequency of the sine wave with unit GHz (double)
    #        amplitude of the sine wave with unit volt (double)
    wavedata = np.array(range(0,pointnum))
    length = len(wavedata)
    wavedata = np.sin(wavedata*2*np.pi*freq + phase)

    
    length_digits = len(str(2*length))
    header_string = '#' + str(length_digits) + str(2*length)
        
    wavename =  '"%s",' % pulsename + str(length) +',INTEGER' 
    wavestr = '"%s"' % pulsename + ',0,' + str(length) + ',' + header_string

    vmax = amp
    wavedata = (wavedata+vmax)*16383.0/(2.0*vmax)
    '''
    markerdata = np.arange(0,pointnum*1/10)
    for x in range(0,len(markerdata)):
        wavedata[markerdata[x]] = wavedata[markerdata[x]] + 16384 #This is to turn on the marker1 to turn marker 2, add 2^15
    '''

    for x in range(0,length):
            wavestr = wavestr + struct.pack('<H',int(wavedata[x]))
            #print int(wavedata[x])

    if (overwrite == 'yes'):
        AWG.deletewaveform(pulsename)
    else:
        pass

            
    AWG.newwaveform(wavename)
    AWG.setwaveform(wavestr)


def coswave(pulsename,pointnum,freq,amp,phase,overwrite = 'no'):
    #create a blcok that is used for wait
    wavedata = np.array(range(0,pointnum))

    length = len(wavedata)
    wavedata = np.cos(wavedata*2*np.pi*freq + phase)

    
    length_digits = len(str(2*length))
    header_string = '#' + str(length_digits) + str(2*length)
        
    wavename =  '"%s",' % pulsename + str(length) +',INTEGER' 
    wavestr = '"%s"' % pulsename + ',0,' + str(length) + ',' + header_string

    vmax = 1
    wavedata = (wavedata+vmax)*16383.0/(2.0*vmax) 
    markerdata = np.array(range(0,pointnum*10/100))
     
     
    for x in range(0,len(markerdata)):
        wavedata[markerdata[x]] = wavedata[markerdata[x]] + 16384 #This is to turn on the marker1 to turn marker 2, add 2^15

    for x in range(0,length):
            wavestr = wavestr + struct.pack('<H',int(wavedata[x]))
            #print int(wavedata[x])

    if (overwrite == 'yes'):
        AWG.deletewaveform(pulsename)
    else:
        pass

            
    AWG.newwaveform(wavename)
    AWG.setwaveform(wavestr)

def alazar_test(pulsename,pointnum,input_string):

    length = pointnum

    length_digits = len(str(2*length))
    header_string = '#' + str(length_digits) + str(2*length)
        
    wavename =  '"%s",' % pulsename + str(length) +',INTEGER' 
    wavestr = '"%s"' % pulsename + ',0,' + str(length) + ',' + header_string
    
    wavestr = wavestr + input_string
    
    AWG.newwaveform(wavename)
    AWG.setwaveform(wavestr)
   