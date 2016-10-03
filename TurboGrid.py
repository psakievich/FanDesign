# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 13:04:58 2016
TURBOGRID
@author: psakievich
"""
import numpy as np
import Profiles as pf
class Profile:
    def __init__(self):
        self.fileName='default'
        self.__fileExtension='_profile.curve'
        self.__numProfiles=3
        self.__percentages=np.linspace(0,100,self.__numProfiles)
        self.__currentProfile=0
        self.__opened=False
    def SetPercentages(self,nProfiles):
        self.__numProfiles=nProfiles
        self.__percentages=np.linspace(0,100,self.__numProfiles)
    def AddProfile(self,profile):
        if(type(profile)!=pf.AxialProfile):
            print('ERROR::YOU MUST PASS A PROFILE OBJECT\n')
            pass
        else:
            if(self.__opened):
                f=open(self.fileName+self.__fileExtension,'a')
            else:
                f=open(self.fileName+self.__fileExtension,'w')
                self.__opened=True
            f.write('# Profile {} at {}%\n'.format(self.__currentProfile+1,
                    self.__percentages[self.__currentProfile]))
            self.__currentProfile=self.__currentProfile+1
            profile.WriteToOpenFile(f)
            f.write('\n')
            f.close()