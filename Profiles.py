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
#from matplotlib import pyplot as plt
"""    
"""
class AxialProfile:
    def __init__(self):
        self.cartesian=True
        self.points=np.zeros((3,20))
        self.name='DEFAULT'
        self.fileExtension='.dat'
        self.chord=1.0
        self.angle=0.0
    def Copy(self):
        you=AxialProfile()
        you.name=self.name
        you.cartesian=self.cartesian
        you.points=self.points.copy()
        you.fileExtension=self.fileExtension
        you.angle=self.angle
        return you
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
                self.points[0][i]=float(columns[0])
                self.points[1][i]=float(columns[1])
            i=i+1
        f.close()
    def Write(self):
        f=open(self.name+self.fileExtension,'w')
        def WriteLine(val):
            f.write(val+'\n')
        WriteLine(self.name)
        shape=self.points.shape
        for i in range(shape[1]):
            WriteLine(str(self.points[0,i])+'  '+str(self.points[1,i])+'  '+
            str(self.points[2,i]))
        f.close()
    def WriteToOpenFile(self,f):
        def WriteLine(val):
            f.write(val+'\n')
        shape=self.points.shape
        for i in range(shape[1]-1):
            WriteLine(str(self.points[0,i])+'  '+str(self.points[1,i])+'  '+
            str(self.points[2,i]))
    def WriteXfoil(self):
        temp=self.Copy()
        f=open(temp.name+'XF'+temp.fileExtension,'w')
        def WriteLine(val):
            f.write(val+'\n')
        WriteLine(temp.name)
        shape=temp.points.shape
        for i in range(shape[1]):
            WriteLine(str(temp.points[0,i])+'  '+str(temp.points[1,i]))
        f.close()
    def Scale(self,xS,yS=1.0,zS=1.0):
        self.points[0][:]=self.points[0][:]*xS
        self.points[1][:]=self.points[1][:]*yS
        self.points[2][:]=self.points[2][:]*zS
    #shift profile in space
    def Shift(self,xC,yC=0.0,zC=0.0):
        self.points[0][:]=self.points[0][:]+xC
        self.points[1][:]=self.points[1][:]+yC
        self.points[2][:]=self.points[2][:]+zC
    #Rotate profile about point (xC,yC) by angle (radians)
    #Rotation is only performed in xy plane
    def Rotate(self,angle,xC=0.0,yC=0.0):
        self.angle=angle
        angRad=angle#*np.pi/180.0
        #shift points
        self.points[0][:]=self.points[0][:]-xC
        self.points[1][:]=self.points[1][:]-yC
        temp=self.points.copy()
        #rotate
        self.points[0][:]=temp[0][:]*np.cos(angRad)-temp[1][:]*np.sin(angRad)
        self.points[1][:]=temp[0][:]*np.sin(angRad)+temp[1][:]*np.cos(angRad)
        #shift back
        self.points[0][:]=self.points[0][:]+xC
        self.points[1][:]=self.points[1][:]+yC    
    def P2dToC3d(self,radius):
        self.points[2][:]=self.points[1][:]
        self.points[1][:]=self.points[0][:]/radius
        self.points[0][:]=radius
        self.cartesian=False
        
    