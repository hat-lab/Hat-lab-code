# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 11:23:36 2015

@author: HatLab_Xi Cao
"""

#create sequence data


import qt
import numpy as np
import struct
import create_waveform


AWG = qt.instruments['AWG']

def t1_seq():
    #set a wave sequence that can do the t1 measurement
    #first we create the pluses we need for this measurement
    create_waveform.pi_pulse('Pi_1000',1000,50)
    create_waveform.testtrigger('testtrigger_1000',1000,50)
    create_waveform.waitblock('waitblock_T',1000,0,'yes')
    create_waveform.waitblock('waitblock_deltaT',1000,0,'yes')
    
    #second we write the sequence we need
    seqlength = 28
    t1_sequence = [[] for index in range(0,seqlength)]
    for x in range(0,seqlength):
        t1_sequence[x] = [[] for index in range(0,6)]
        
    for x in range(0,seqlength,4):
        looptimes = 1
        t1_sequence[x][0] = 'wait'
        t1_sequence[x][1] = 'no_loop'
        t1_sequence[x][2] = 'Pi_1000'
        t1_sequence[x+1][0] = 'no_wait'
        t1_sequence[x+1][1] = 'no_loop'
        t1_sequence[x+1][2] = 'waitblock_T'
        t1_sequence[x+2][0] = 'no_wait'
        t1_sequence[x+2][1] = str((x/4+1)*looptimes)
        t1_sequence[x+2][2] = 'waitblock_deltaT'
        t1_sequence[x+3][0] = 'no_wait'
        t1_sequence[x+3][1] = 'no_loop'
        t1_sequence[x+3][2] = 'testtrigger_1000'
        
        
    
    for x in range(0,seqlength):
        for y in range(3,6):
            t1_sequence[x][y] = 'empty'
            
            
    #third we write the sequence into the AWG
    AWG.setmode('SEQUENCE') #set AWG to sequence mode
    AWG.set_sequence_length(seqlength) #create a empty sequence
    
    for x in range(0,seqlength):
        if (t1_sequence[x][0] == 'wait' ):
            AWG.waittrigger(x+1,1)
        else:
            AWG.waittrigger(x+1,0)
            
        if (t1_sequence[x][1] == 'no_loop'):
            pass
        else:
            AWG.setloop(x+1,int(t1_sequence[x][1]))
            
        for y in range(1,5):
            if (t1_sequence[x][y] == 'empty'):
                pass
            else:
                AWG.addwaveform(x+1,y-1,t1_sequence[x][y])

                
    
def alazar_test():
    
    AWG.set_sequence_length(0)
    seqlength = 40
    create_waveform.waitblock('waitblock_T',100,0,'yes')
    create_waveform.waitblock_marker('waitblock_marker',1000,0,'yes')
    for x in range(seqlength/2):
        create_waveform.sinwave('Sinewave%i' %x, 2000, 0.001, 1, 4.0*np.pi*x/seqlength,'yes')
        create_waveform.sinwave('Sinewave_inverse%i' %x, 2000, 0.001, 1, -4.0*np.pi*x/seqlength,'yes')
     
     
    alazar_sequence = [[] for index in range(0,seqlength)]
    for x in range(0,seqlength):
        alazar_sequence[x] = [[] for index in range(0,6)]    
        
        
    for x in range(0,seqlength,2):
        temp = x/2
        alazar_sequence[x][0] = 'no_wait'
        alazar_sequence[x][1] = 'no_loop'
        alazar_sequence[x+1][2] = 'Sinewave%i' % temp
        alazar_sequence[x+1][3] = 'Sinewave_inverse%i' % temp  
        alazar_sequence[x+1][0] = 'no_wait'
        alazar_sequence[x+1][1] = 'no_loop'
        alazar_sequence[x][2] = 'waitblock_T'
        alazar_sequence[x][3] = 'waitblock_T'  
        for y in range(4,6):
            alazar_sequence[x][y] = 'empty'
    
    alazar_sequence[0][2] = 'waitblock_marker'
    alazar_sequence[0][3] = 'waitblock_marker'    
    
    AWG.setmode('SEQUENCE') #set AWG to sequence mode
    AWG.set_sequence_length(seqlength) #create a empty sequence            
            
    for x in range(0,seqlength):
        if (alazar_sequence[x][0] == 'wait' ):
            AWG.waittrigger(x+1,1)
        else:
            AWG.waittrigger(x+1,0)
            
        if (alazar_sequence[x][1] == 'no_loop'):
            pass
        else:
            AWG.setloop(x+1,int(alazar_sequence[x][1]))
            
        for y in range(1,5):
            if (alazar_sequence[x][y] == 'empty'):
                pass
            else:
                AWG.addwaveform(x+1,y-1,alazar_sequence[x][y])      
                
    AWG.channel_on(1)
    AWG.channel_on(2)                   
                
def alazar_test1():
    
    AWG.set_sequence_length(0)
    seqlength = 40
    create_waveform.waitblock('waitblock_T',100,0,'yes')
    create_waveform.waitblock_marker('waitblock_marker',1000,0,'yes')
    for x in range(seqlength/2):
        create_waveform.sinwave('Sinewave%i' %x, 2000, 0.001, 1, 8.0*np.pi*x/seqlength,'yes')
     
     
    alazar_sequence = [[] for index in range(0,seqlength)]
    for x in range(0,seqlength):
        alazar_sequence[x] = [[] for index in range(0,6)]    
        
        
    for x in range(0,seqlength,2):
        temp = x/2
        alazar_sequence[x][0] = 'no_wait'
        alazar_sequence[x][1] = 'no_loop'
        alazar_sequence[x+1][2] = 'Sinewave%i' % temp
        alazar_sequence[x+1][3] = 'Sinewave0'  
        alazar_sequence[x+1][0] = 'no_wait'
        alazar_sequence[x+1][1] = 'no_loop'
        alazar_sequence[x][2] = 'waitblock_marker'
        alazar_sequence[x][3] = 'waitblock_marker'  
        for y in range(4,6):
            alazar_sequence[x][y] = 'empty'
    
    alazar_sequence[0][2] = 'waitblock_marker'
    alazar_sequence[0][3] = 'waitblock_marker'    
    
    AWG.setmode('SEQUENCE') #set AWG to sequence mode
    AWG.set_sequence_length(seqlength) #create a empty sequence            
            
    for x in range(0,seqlength):
        if (alazar_sequence[x][0] == 'wait' ):
            AWG.waittrigger(x+1,1)
        else:
            AWG.waittrigger(x+1,0)
            
        if (alazar_sequence[x][1] == 'no_loop'):
            pass
        else:
            AWG.setloop(x+1,int(alazar_sequence[x][1]))
            
        for y in range(1,5):
            if (alazar_sequence[x][y] == 'empty'):
                pass
            else:
                AWG.addwaveform(x+1,y-1,alazar_sequence[x][y])      
                
    AWG.channel_on(1)
    AWG.channel_on(2)                   
                
def alazar_test2():
    
    AWG.set_sequence_length(0)
    seqlength = 4
    create_waveform.waitblock_marker('waitblock_test',1000,0,'yes')
    create_waveform.waitblock('wait',1000,0,'yes')
    create_waveform.sinwave('Sinewave_test0' , 2048, 0.001, 1, 0,'yes')
    create_waveform.sinwave('Sinewave_test1' , 2048, 0.001, 1, 45,'yes')
    create_waveform.sinwave('Sinewave_test2', 2048, 0.001, 1, 90,'yes')
     
     
    alazar_sequence = [[] for index in range(0,seqlength)]
    for x in range(0,seqlength):
        alazar_sequence[x] = [[] for index in range(0,6)]    
        
        
    for x in range(1,seqlength):
        alazar_sequence[x][0] = 'no_wait'
        alazar_sequence[x][1] = 'no_loop'
        alazar_sequence[x][2] = 'Sinewave_test%i' %x
        alazar_sequence[x][3] = 'Sinewave_test0'  
        for y in range(4,6):
            alazar_sequence[x][y] = 'empty'
    
    alazar_sequence[0][0] = 'no_wait'
    alazar_sequence[0][1] = 'no_loop'    
    alazar_sequence[0][2] = 'waitblock_test'
    alazar_sequence[0][3] = 'waitblock_test'    

    alazar_sequence[2][0] = 'no_wait'
    alazar_sequence[2][1] = 'no_loop'    
    alazar_sequence[2][2] = 'wait'
    alazar_sequence[2][3] = 'wait'  

    alazar_sequence[3][0] = 'no_wait'
    alazar_sequence[3][1] = 'no_loop'    
    alazar_sequence[3][2] = 'Sinewave_test2'
    alazar_sequence[3][3] = 'Sinewave_test0'  
    
    AWG.setmode('SEQUENCE') #set AWG to sequence mode
    AWG.set_sequence_length(seqlength) #create a empty sequence            
            
    for x in range(0,seqlength):
        if (alazar_sequence[x][0] == 'wait' ):
            AWG.waittrigger(x+1,1)
        else:
            AWG.waittrigger(x+1,0)
            
        if (alazar_sequence[x][1] == 'no_loop'):
            pass
        else:
            AWG.setloop(x+1,int(alazar_sequence[x][1]))
            
        for y in range(1,5):
            if (alazar_sequence[x][y] == 'empty'):
                pass
            else:
                AWG.addwaveform(x+1,y-1,alazar_sequence[x][y])                             
                
            
    AWG.channel_on(1)
    AWG.channel_on(2)               
                
                
                
            
#t1_seq()
#create_waveform.testtrigger('testtrigger_1000',1000,2*np.pi)
'''
wait_unit = 1e-2
wait_time = 1e-2

index = 0
AWG.run()
while (index<100):

    AWG.force_trigger()
    for x in range(1,6):
        qt.msleep(wait_unit/x)
        AWG.force_trigger()
        qt.msleep(wait_time)
            
    index = index + 1
    
    
AWG.stop()
'''