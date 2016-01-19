# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 09:24:24 2016

@author: HatLab_Xi Cao
"""

# Sub class sinwave of class pulse
from pulse import pulse
import numpy as np

class sinwave(pulse):
    def __init__(self, pulseform):
        super(sinwave,self).__init__(pulseform[0:4])        
        self.amp = float(pulseform[4])
        self.freq = float(pulseform[5])
        self.phase = float(pulseform[6])
        
    def pulseGenerator(self):
        self.datapoint = self.amp*np.sin(self.datapoint*self.freq*2*np.pi+self.phase)
        print self.idname

class empty(pulse):
    def __init__(self, pulseform):
        super(empty,self).__init__(pulseform[0:4])