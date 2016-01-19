# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 17:24:21 2015

@author: HatLab_Xi Cao
"""

#mixer test
import qt
import create_waveform


AWG = qt.instruments['AWG']
#create_waveform.waitblock('zeropulse',1000,0,'yes')
create_waveform.sinwave('sinwave',1000,'yes')
create_waveform.coswave('coswave',1000,'yes')

AWG.set_sequence_length(0)
AWG.set_sequence_length(1)

AWG.addwaveform(1,1,'sinwave')
AWG.addwaveform(1,2,'coswave')