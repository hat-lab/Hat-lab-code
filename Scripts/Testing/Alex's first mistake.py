# -*- coding: utf-8 -*-
"""
Created on Fri Jan 08 14:43:14 2016

@author: Alex
"""

import qt
import numpy as np
import struct

AWG=qt.instruments['AWG']
    
def test():
    print 'test'
    
def sin_wave(pointnum,maxV,name):
    
    waveValues=np.zeros(pointnum)
    markers=range(0, pointnum*.642)
    
    for value in waveValues:
        value=maxV*np.sin(value)
        
        
    waveValues=(waveValues+maxV)*16383.0/(2.0*maxV)
    
    for mark in markers:
        waveValues[markers[mark]]+=16384
    
    makeNewCommand= '"'+name+'", '+str(pointnum)+', INTEGER'
    
    length=len(waveValues)
    
    length_dig=len(waveValues*2)
    dig=waveValues*2
    
    setCommand='"'+name+'", 0, '+str(length)+ ', #'+str(length_dig)+str(dig)
    
    for value in waveValues:
        value=struct.pack('<H', int(value))
        setCommand+=value
        
    AWG.newwaveform(makeNewCommand)
    AWG.setwaveform(setCommand)
    
    
    
    