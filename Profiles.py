# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 09:52:05 2016

@author: psakievich
"""
"""
Class for storing AxialProfile that can translate between
XFOIL and python through a labeled coordinate file
"""
import numpy as np
"""
FUNCTIONS
    NORMALIZE
    
"""
class AxialProfile:
    def __init__(self):
        self.cartesian=True
        self.points=np.zeros((3,20))
        self.name='DEFAULT'
    def Read(self,fName):
        f=open(fName,'r')
        #Get number of points
        i=-1 #-1 because the file should have a name for the profile
        for line in f:
           i=i+1
        #Allocate Points
        self.points=np.zeros((3,i))
        #Reset the file           
        f.seek(0)
        i=-1
        for line in f:
            if(i==-1):
                self.name=line.strip()
            else:
                line=line.strip()
                columns=line.split()
                self.points[0,i]=float(columns[0])
                self.points[1,i]=float(columns[1])
            i=i+1
        f.close()
    def WriteXfoil(self):
        self.Normalize()
        f=open(self.name+'.dat','w')
        def WriteLine(val):
            f.write(val+'\n')
        WriteLine(self.name)
        shape=self.points.shape
        for i in range(shape[1]):
            WriteLine(str(self.points[0,i])+', '+str(self.points[1,i]))
        f.close()
    #Normalize profile so chord lenght =1.0
    def Normalize(self):
        rnge=self.points.shape
        mx=np.amax(self.points[0,0:rnge[1]])
        mn=np.amin(self.points[0,0:rnge[1]])
        chord=mx-mn
        self.points=self.points/chord
        
        