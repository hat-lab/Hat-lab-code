# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 10:08:32 2016

@author: HatLab_Xi Cao
"""

#step fuction
from pulse import pulse
import numpy as np

class stepwave(pulse):
    def __init__(self,pulseform):
        super(stepwave,self).__init__(pulseform[0:4])
        self.changepoint = int(pulseform[4])
        
    def pulseGenerator(self):
        self.datapoint = np.zeros(self.width)
        self.datapoint[0:self.changepoint] = 0.8