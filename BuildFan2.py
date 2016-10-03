# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 14:31:57 2016

@author: psakievich
"""

import AxialFan as AF
import Profiles

wing=Profiles.AxialProfile()
wing.Read('testProfile.txt')
wing.name='NACA'
wing.Shift(-0.5)

me=AF.AxialFan(2.5,4.69,11000,450,2.0,11)
for i in range(10):
    me.SetAlpha(wing,i,0.0,7.0,0.25)

me.PrintProperties()
me.WriteProperties('FanDesigned.txt')