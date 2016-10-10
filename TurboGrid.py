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
        self.__fileExtension='.curve'
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
                f=open(self.fileName+'_profile'+self.__fileExtension,'a')
            else:
                f=open(self.fileName+'_profile'+self.__fileExtension,'w')
                self.__opened=True
            f.write('# Profile {} at {}%\n'.format(self.__currentProfile+1,
                    self.__percentages[self.__currentProfile]))
            self.__currentProfile=self.__currentProfile+1
            profile.WriteToOpenFile(f)
            f.write('\n')
            f.close()
    def _WriteCap(self,profile,inPoints,outPoints,syntax):
        f=open(self.fileName+syntax+self.__fileExtension,'w')
        #write inflow points
        for i in range(int(inPoints.shape[0])):
            f.write('{},{},{}\n'.format(inPoints[i,0],inPoints[i,1],
                    inPoints[i,2]))                    
        j=profile.points.shape[1]
        cSize=int(profile.points.shape[1]/2)
        camber=np.zeros(3)
        #write camberline
        for i in range(cSize):
            j=j-1
            camber=0.5*(profile.points[:,i]+profile.points[:,j])
            f.write('{},{},{}\n'.format(camber[0],camber[1],camber[2]))
        #write outflow points
        for i in range(int(outPoints.shape[0])):
            f.write('{},{},{}\n'.format(outPoints[i,0],outPoints[i,1],
                    outPoints[i,2]))
        f.close()
    def WriteHub(self,profile,inPoints,outPoints):
        self._WriteCap(profile,inPoints,outPoints,'_hub')
    def WriteShroud(self,profile,inPoints,outPoints):
        self._WriteCap(profile,inPoints,outPoints,'_shroud')