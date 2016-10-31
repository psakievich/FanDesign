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
class Profile:
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
        #shift points
        self.points[0][:]=self.points[0][:]-xC
        self.points[1][:]=self.points[1][:]-yC
        temp=self.points.copy()
        #rotate
        self.points[0][:]=temp[0][:]*np.cos(angle)- \
            temp[1][:]*np.sin(angle)
        self.points[1][:]=temp[0][:]*np.sin(angle)+ \
            temp[1][:]*np.cos(angle)
        #shift back
        self.points[0][:]=self.points[0][:]+xC
        self.points[1][:]=self.points[1][:]+yC    
#Profile for axial fan
class AxialProfile(Profile):
    def __init__(self):
        Profile.__init__(self)
        self.name='fan'
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
    def P2dToC3d(self,radius):
        self.points[2][:]=self.points[1][:]
        self.points[1][:]=self.points[0][:]/radius
        self.points[0][:]=radius
        self.cartesian=False
#Design outlet veins        
class Stator(Profile):
    def __init__(self):
        Profile.__init__(self)
        self.cartesian=False
        self.name='stator'
        self.pntsPerFace=10
        self.pntsPerRadi=6
        self.pntsPerTip=4
        self.ratio=0.5
        self.shift=0.0 #angle in radians
        self.thickness=0.1
        self.nblades=11
        self.dHub=1.0
        self.SetPointDensity(self.pntsPerFace,self.pntsPerRadi,self.pntsPerTip)
    def SetPointDensity(self,PointsPerFace,PointsPerRadi,PointsPerTip):
        self.pntsPerFace=PointsPerFace
        self.pntsPerRadi=PointsPerRadi
        self.pntsPerTip=PointsPerTip
        self.points=np.zeros((3,2*(2*self.pntsPerFace+self.pntsPerRadi+2*self.pntsPerTip)))
    def BuildStator(self,delta,radius):
        #Set spacing
        thetaInit=2*np.pi/self.nblades
        cLength=thetaInit*self.dHub/2
        dY=(1.0-self.ratio-self.thickness*0.5)/float(self.pntsPerFace)
        dT=self.thickness*0.5/float(self.pntsPerTip)
        #Set original line for projecting faces and tip
        orgUpper=np.arange(1.0-0.5*self.thickness,self.ratio,-dY)
        orgLower=-orgUpper[::-1]
        orgUpTip=np.arange(1.0,1.0-self.thickness*0.5,-dT)
        orgLwTip=-orgUpTip[::-1]
        #set tip length offset
        tipLength=1.0/np.cos(delta)-self.thickness/2.0/np.tan(np.pi/2-delta)
        #stretch profiles accordingly
        orgUpper=(orgUpper-self.ratio)/self.ratio*(tipLength-1.0)+orgUpper
        orgUpTip=(orgUpTip-self.ratio)/self.ratio*(tipLength-1.0)+orgUpTip
        orgRadius=np.linspace(-0.5*self.ratio,0.5*self.ratio,self.pntsPerRadi)
        #perform rotation
        camberUpper=np.array([-orgUpper*np.sin(delta),orgUpper*np.cos(delta)])
        camberLower=np.array([np.zeros(self.pntsPerFace),orgLower])
        camberUpTip=np.array([-orgUpTip*np.sin(delta),orgUpTip*np.cos(delta)])
        #design radius
        alpha=delta/2
        R=self.ratio/np.tan(alpha)
        #create face1
        normal=[-np.cos(delta),np.sin(-delta)]
        face1Upper=np.array([camberUpper[0,:]+normal[0]*self.thickness/2, \
            camberUpper[1,:]+normal[1]*self.thickness/2])
        face1Lower=np.array([camberLower[0,:]-self.thickness/2,camberLower[1,:]])
        face1Radius=np.array([(R-self.thickness/2)*np.cos(delta*(self.ratio+orgRadius))-R, \
            (R-self.thickness/2)*np.sin(delta*(self.ratio+orgRadius))-self.ratio])
        #create face2
        face2Upper=np.array([camberUpper[0,:]-normal[0]*self.thickness/2, \
            camberUpper[1,:]-normal[1]*self.thickness/2])
        face2Lower=np.array([camberLower[0,:]+self.thickness/2,camberLower[1,:]])
        face2Radius=np.array([(R+self.thickness/2)*np.cos(delta*(self.ratio+orgRadius))-R, \
            (R+self.thickness/2)*np.sin(delta*(self.ratio+orgRadius))-self.ratio])
        #create tips
        tempY=self.thickness/2-(tipLength-orgUpTip)-dT/2
        tempX=np.sqrt(self.thickness**2/4-tempY**2)
        face1UpTip=np.array([camberUpTip[0,:]-normal[1]*dT/2+normal[0]*tempX, \
            camberUpTip[1,:]+normal[0]*dT/2+normal[1]*tempX])
        face2UpTip=np.array([camberUpTip[0,:]-normal[1]*dT/2-normal[0]*tempX[:], \
            camberUpTip[1,:]+normal[0]*dT/2-normal[1]*tempX[:]])
        tipTheta=np.pi/2*(orgLwTip+dT/2+1)/self.thickness/2
        face1LwTip=np.array([-self.thickness/2*np.sin(tipTheta), \
            -self.thickness/2*np.cos(tipTheta)-(1-self.thickness/2)])
        face2LwTip=np.array([self.thickness/2*np.sin(tipTheta), \
            -self.thickness/2*np.cos(tipTheta)-(1-self.thickness/2)])            
        #pack results to points array
        a=0
        b=self.pntsPerTip
        self.points[1:3,a:b]=face1LwTip[:,::-1]
        a=b
        b=b+self.pntsPerFace
        self.points[1:3,a:b]=face1Lower[:,::-1]
        a=b
        b=b+self.pntsPerRadi
        self.points[1:3,a:b]=face1Radius
        a=b
        b=b+self.pntsPerFace
        self.points[1:3,a:b]=face1Upper[:,::-1]
        a=b
        b=b+self.pntsPerTip
        self.points[1:3,a:b]=face1UpTip[:,::-1]
        a=b
        b=b+self.pntsPerTip
        self.points[1:3,a:b]=face2UpTip
        a=b
        b=b+self.pntsPerFace
        self.points[1:3,a:b]=face2Upper
        a=b
        b=b+self.pntsPerRadi
        self.points[1:3,a:b]=face2Radius[:,::-1]
        a=b
        b=b+self.pntsPerFace
        self.points[1:3,a:b]=face2Lower
        a=b
        b=b+self.pntsPerTip
        self.points[1:3,a:b]=face2LwTip
        #scale results
        self.points[0,:]=radius
        self.points[1,:]=self.points[1,:]*cLength/radius+self.shift*(radius-self.dHub)
        self.points[2,:]=-self.points[2,:]*self.chord/2
        
        
        
        