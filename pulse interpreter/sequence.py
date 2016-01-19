# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 09:29:56 2016

@author: HatLab_Xi Cao
"""

# class sequence

import qt

AWG = qt.instruments['AWG']

class sequence:
    def __init__(self,Empty,WaveForm):
        self.length = len(Empty) + len(WaveForm)/4
        self.Empty = Empty
        self.WaveForm = WaveForm

    def set_waveform_name(self):
        for x in range(len(self.Empty)):
            self.Empty[x].get_name('element_%i' % (2*x+1)) # 5 means all channel
            self.Empty[x].upload()
        for x in range(len(self.WaveForm)):
            elementnum = 2*((x-x%4)/4+1)
            self.WaveForm[x].get_name('element_%i_' % elementnum + 'channel_%i' % (x%4+1))
            self.WaveForm[x].upload()
            
    def upload(self):
        self.set_waveform_name()
        
        print self.length
        AWG.set_sequence_length(self.length)
        
        for x in range(len(self.Empty)):
            elementnum = self.Empty[x].pulsename
            elementnum = elementnum.split('_')
            elementnum = int(elementnum[1])
            
            AWG.addwaveform(elementnum,1,self.Empty[x].pulsename)
            AWG.addwaveform(elementnum,2,self.Empty[x].pulsename)
            AWG.addwaveform(elementnum,3,self.Empty[x].pulsename)            
            AWG.addwaveform(elementnum,4,self.Empty[x].pulsename)

        for x in range(len(self.WaveForm)):
            elementnum = self.WaveForm[x].pulsename
            elementnum = elementnum.split('_')
            channelnum = int(elementnum[3])
            elementnum = int(elementnum[1])           
            print channelnum
            print elementnum
            AWG.addwaveform(elementnum,channelnum,self.WaveForm[x].pulsename)