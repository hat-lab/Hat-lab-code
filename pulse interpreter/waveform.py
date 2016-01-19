# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 09:24:56 2016

@author: HatLab_Xi Cao
"""

# Class of waveform

import numpy as np
import struct
import qt
import matplotlib.pyplot as plt
AWG = qt.instruments['AWG']

class waveform:
    def __init__(self,waveform):
        self.start = waveform[0]
        self.end = waveform[1]        
        self.channel = waveform[2]
        self.wavedata = np.zeros(self.end-self.start)
        self.pulse = waveform[3:]
        self.pulsename = 'default'        
        self.wavename = 'default'
        self.wavrstr = 'default'
        self.idname = str(len(self.wavedata))
        
    def waveGenerator(self):
        for x in range(len(self.pulse)):
            self.wavedata[(self.pulse[x].start-self.start):(self.pulse[x].end-self.start)] = self.pulse[x].datapoint
            
    def plotwave(self):
        xdata = np.arange(self.end-self.start)
        plt.plot(xdata,self.wavedata)
    
    def get_name(self,pulsename):
        self.pulsename = pulsename
    
    def get_idname(self):
        idstring = '_'
        for x in range(len(self.pulse)):
            idstring = idstring + self.pulse[x].idname + str(self.pulse[x].start-self.start)
          
    def translation(self,idnamelist):
        
        length = len(self.wavedata)
        length_digits = len(str(2*length))
        header_string = '#' + str(length_digits) + str(2*length)
        self.wavename =  '"%s",' % self.pulsename + str(length) +',INTEGER' 
        self.wavestr = '"%s"' % self.pulsename + ',0,' + str(length) + ',' + header_string
        
        vmax = 1.0
        self.wavedata = (self.wavedata+vmax)*16383.0/(2.0*vmax)                
        for x in range(0,length):
            self.wavestr = self.wavestr + struct.pack('<H',int(self.wavedata[x]))

    def upload(self,idnamelist):
        for names in idnamelist:
            if (names == self.idname):
                break
        
    
        self.translation(idnamelist)
        AWG.newwaveform(self.wavename)
        AWG.setwaveform(self.wavestr)   
        
        
        
        
        
        
        
        
        
        
        
        
        