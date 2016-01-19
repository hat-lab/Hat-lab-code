# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 09:44:47 2016

@author: HatLab_Xi Cao
"""

# fuction that creat a sequence in AWG according to the input

from class_test import *


a = readinput('readtest.txt')
b = element_calulator(a)
print b
c = element_creator(b,a)
d = waveform_creator(c[0],c[1])
e = sequence(d[1],d[0])
print e.length
#e.upload()

