# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 09:23:41 2016

@author: HatLab_Xi Cao
"""

# The Class of Pulse

import numpy as np

class pulse(object):
    def __init__(self, pulseform):
        self.ptype = pulseform[0]
        self.channel = pulseform[1]
        self.start = int(pulseform[2])
        self.width = int(pulseform[3])
        self.end = self.start + self.width
        self.datapoint = np.arange(self.start,self.end)
        self.idname = '_'
        
        for names in pulseform:
            self.idname = self.idname + names
        
    def pulseGenerator(self):
        #self.datapoint = np.zeros(self.datapoints)
        self.datapoint = np.zeros(self.width)