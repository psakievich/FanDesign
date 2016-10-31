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
        cSize=int(profile.points.shape[1]/2)
        pSize=int(profile.points.shape[1])
        camber=np.zeros([3,cSize])
        #create camberline
        j=cSize-1
        k=0
        for i in range(cSize,pSize):
            camber[:,k]=0.5*(profile.points[:,i]+profile.points[:,j])
            j=j-1
            k=k+1
        #writedata    
        f=open(self.fileName+syntax+self.__fileExtension,'w')
        if(type(inPoints)==type(float())):
            f.write('{},{},{}\n'.format(camber[0,0],camber[1,0],
                    float(camber[2,0]-inPoints)))
        else:
            for i in range(int(inPoints.shape[1])):
                f.write('{},{},{}\n'.format(inPoints[0,i],inPoints[1,i],
                        inPoints[2,i]))
        for i in range(cSize):
            f.write('{},{},{}\n'.format(camber[0,i],camber[1,i],camber[2,i]))
        if(type(outPoints)==type(float())):
            f.write('{},{},{}\n'.format(camber[0,cSize-1],camber[1,cSize-1],
                    float(camber[2,cSize-1]+outPoints)))
        else:
            for i in range(int(outPoints.shape[1])):
                f.write('{},{},{}\n'.format(outPoints[0,i],outPoints[1,i],
                        outPoints[2,i]))
        f.close()
    def WriteHub(self,profile,inPoints,outPoints):
        self._WriteCap(profile,inPoints,outPoints,'_hub')
    def WriteShroud(self,profile,inPoints,outPoints):
        self._WriteCap(profile,inPoints,outPoints,'_shroud')