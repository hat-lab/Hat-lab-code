# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 10:47:54 2015

@author: HatLab_Xi Cao
"""

#T1 measurement

import qt
import create_sequence


#create_waveform.pi_pulse('Pi_1000_square_trigger2',1000,50)
AWG = qt.instruments['AWG']

create_sequence.t1_seq()


AWG.run()

