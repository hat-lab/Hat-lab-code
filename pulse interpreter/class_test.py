# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 14:14:06 2016

@author: HatLab_Xi Cao
"""
#learn class and super class


from bitstring import BitArray
import sys
sys.path.append('C:\Users\HatLab_Xi Cao\Box Sync\Programming\AWG\pulse interpreter\pulse')
from sinwave import sinwave
from stepwave import stepwave
from waveform import waveform
from sequence import sequence


def typechose(pulsename):
    if (pulsename[0] == 'sin'):
        result = sinwave(pulsename)
        result.pulseGenerator()
    elif (pulsename[0] == 'stepwave'):
        result = stepwave(pulsename)
        result.pulseGenerator()
    else:
        print 'No matched waveform'
        raise 
    return result
    
    
def readinput(filename):
    
    inputfile = open(filename,'r')
    pulsenames = inputfile.readlines()
    result = []
    
    for x in range(len(pulsenames)):
        pulsenames[x] = pulsenames[x].strip()
        pulsenames[x] = pulsenames[x].split(',')
        result.append(typechose(pulsenames[x]))
        
    return result
        
def element_calulator(Pulses):

    ch1 = [-1]
    ch2 = [-1]
    ch3 = [-1]
    ch4 = [-1]

    for arg in Pulses:
        if (arg.channel == 'ch1'):
            ch1.append(arg.start)
            ch1.append(arg.end)
        elif (arg.channel == 'ch2'):
            ch2.append(arg.start)
            ch2.append(arg.end)
        elif (arg.channel == 'ch3'):
            ch3.append(arg.start)
            ch3.append(arg.end)
        elif (arg.channel == 'ch4'):
            ch4.append(arg.start)
            ch4.append(arg.end)
            
    tot_length = max(max(ch1),max(ch2),max(ch3),max(ch4))
    del ch1[0]
    del ch2[0]
    del ch3[0]
    del ch4[0]
    
    
    channel1 = BitArray(int=0, length=tot_length)
    channel2 = BitArray(int=0, length=tot_length)
    channel3 = BitArray(int=0, length=tot_length)
    channel4 = BitArray(int=0, length=tot_length)
    for x in range(len(ch1)):
        if (x%2 == 0):
            channel1.invert(range(ch1[x],ch1[x+1]))
        else:
            pass
    
    for x in range(len(ch2)):
        if (x%2 == 0):
            channel2.invert(range(ch2[x],ch2[x+1]))
        else:
            pass    
    
    for x in range(len(ch3)):
        if (x%2 == 0):
            channel3.invert(range(ch3[x],ch3[x+1]))
        else:
            pass
        
    for x in range(len(ch4)):
        if (x%2 == 0):
            channel4.invert(range(ch4[x],ch4[x+1]))
        else:
            pass

    channel1 |= channel2
    channel3 |= channel4
    channel1 |= channel3    
    
    channel1.append('0b0')
    result = []
    count = 0    
    test = BitArray(int = 0, length = 1)
    empty = test.find('0b1')
    
    while (channel1.len != 0):
        
        test = channel1.find('0b1')
        if (test == empty):
            break
        else:
            result.append(channel1.find('0b1'))
            result[count] = result[count][0]
            del channel1[0:result[count]]
            count = count + 1
    
        test = channel1.find('0b0')
        if (test == empty):
            break
        else:
            result.append(channel1.find('0b0'))
            result[count] = result[count][0]
            del channel1[0:result[count]]
            count = count + 1

    return result


def element_creator(elements, pulses):
    
    # should be a function to find out if any element is too large 
    maxlength = 100000 # This should be the largest point number we can have in one element
    for x in range(len(elements)):
        if (elements[x] > maxlength):
            raise NameError('The length of the %ith element is too large' % (x+1))
                
    element_blocks = [0]  
    for x in range(len(elements)):
        element_blocks.append(elements[x]+sum(elements[0:x]))
                
    empty_elements = []
    for x in range(0,len(elements),2):
        temp = []
        temp.append(element_blocks[x])
        temp.append(element_blocks[x+1])
        temp.append('all')
        empty_elements.append(temp)
      
    nonempty_elements = []      
    for x in range(1,len(element_blocks),2):
        temp = [element_blocks[x],element_blocks[x+1]]
        for y in range(len(pulses)):
            if (pulses[y].start >= temp[0]) & (pulses[y].start < temp[1]):
                temp.append(pulses[y])
        nonempty_elements.append(temp)

               
    return (empty_elements,nonempty_elements)
    

def waveform_creator(empty_elements,nonempty_elements):    
    WaveForm = []    
    Empty = []
    
    for x in range(len(nonempty_elements)):
        ch1 = [nonempty_elements[x][0],nonempty_elements[x][1],'ch1']
        ch2 = [nonempty_elements[x][0],nonempty_elements[x][1],'ch2']
        ch3 = [nonempty_elements[x][0],nonempty_elements[x][1],'ch3']
        ch4 = [nonempty_elements[x][0],nonempty_elements[x][1],'ch4']
        
        for y in range(2,len(nonempty_elements[x])):               
            if (nonempty_elements[x][y].channel == 'ch1'):
                ch1.append(nonempty_elements[x][y])
            elif (nonempty_elements[x][y].channel == 'ch2'):
                ch2.append(nonempty_elements[x][y])
            elif (nonempty_elements[x][y].channel == 'ch3'):
                ch3.append(nonempty_elements[x][y])
            elif (nonempty_elements[x][y].channel == 'ch4'):
                ch4.append(nonempty_elements[x][y])

        ch1 = waveform(ch1)
        ch2 = waveform(ch2)
        ch3 = waveform(ch3)
        ch4 = waveform(ch4)
        ch1.waveGenerator()
        ch2.waveGenerator()
        ch3.waveGenerator()
        ch4.waveGenerator()
                
        WaveForm.append(ch1)
        WaveForm.append(ch2)
        WaveForm.append(ch3)
        WaveForm.append(ch4)
    
    for x in range(len(empty_elements)):
        Empty.append(waveform(empty_elements[x]))
        
    return (WaveForm,Empty)











