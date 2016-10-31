# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 14:31:57 2016

@author: psakievich
"""

import AxialFan as AF
import Profiles
import numpy as np
import TurboGrid as TG
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
'''
------------------------------------------------------------------------------
USER INPUT START
------------------------------------------------------------------------------
'''
RPM=11000.0
CFM=450
SP=2.0
HubDiameter=2.5
TipDiameter=4.69
NumberOfBlades=11
VariableChordLength=False
FanStatorClearance=0.5
FanInletDomainLength=0.25
StatorOutletDomainLength=0.25
StatorChord=0.75
StatorThickness=0.075
NumberOfStatorVanes=13
NumberOfCrossSections=10
AirfoilFile='testProfile.txt'
AirfoilName='test'
SummaryFile='AreaOptimization'
XfoilPath=r'C:\Users\psakievich\Desktop\XFOIL6.99\xfoil.exe'
alphaMin=-1.0
alphaMax=8.0
alphaInc=0.5
'''
------------------------------------------------------------------------------
USER INPUT END
------------------------------------------------------------------------------
'''
#Setup profile
wing=Profiles.AxialProfile()
wing.Read(AirfoilFile)
wing.name=AirfoilName
wing.Shift(-0.5)
stator=Profiles.Stator()
stator.chord=StatorChord
stator.thickness=StatorThickness
stator.nblades=NumberOfStatorVanes
stator.dHub=HubDiameter
profs=[]
#Setup turbogrid writer
writer=TG.Profile()#fan
writer.fileName='fan'
writer.SetPercentages(NumberOfCrossSections)
writer2=TG.Profile()#stator
writer2.fileName='stator'
writer2.SetPercentages(NumberOfCrossSections)
#Declare fan inputs
me=AF.AxialFan(HubDiameter, \
               TipDiameter, \
               RPM, \
               CFM, \
               SP, \
               NumberOfBlades)
radius=me.GetRadius()
beta=me.GetBeta()
chord=me.GetChord()
#Modify chord length
for i in range(NumberOfCrossSections):
    profs.append(wing.Copy())
if(VariableChordLength):
    for i in range(NumberOfCrossSections):
        #try to maximize azimuthal area for each cross section
        NewChord=np.pi*2.0*radius[i]/NumberOfBlades/np.cos(beta[i])
        me.SetChordOfProfile(NewChord,i)
        #keep chord length of unity for alpha calculation, but rescale thickness
        profs[i].Scale(1.0,chord[i]/NewChord)
#Set flow parameters        
me.SetCl()
me.SetReynolds()
me.SetMach()
chord=me.GetChord()

#Calculate angle of attack for desired Coefficient of lift
for i in range(NumberOfCrossSections):
    me.SetAlpha(profs[i],i,aMin=alphaMin,aMax=alphaMax,inc=alphaInc, \
                xFoilPath=XfoilPath)
alpha=me.GetAlpha()
#Out put Fan results
me.PrintProperties()
me.WriteProperties(SummaryFile+'1.txt')
if(VariableChordLength):
    #Adjust chord length for alpha's
    for i in range(NumberOfCrossSections):
        #try to maximize azimuthal area for each cross section
        NewChord=np.pi*2.0*radius[i]/NumberOfBlades/np.cos(beta[i]+alpha[i])
        me.SetChordOfProfile(NewChord,i)
        #keep chord length of unity for alpha calculation, but rescale thickness
        profs[i].Scale(1.0,chord[i]/NewChord)
    #Set flow parameters        
    me.SetCl()
    me.SetReynolds()
    me.SetMach()
    chord=me.GetChord()

    #Calculate angle of attack for desired Coefficient of lift
    for i in range(NumberOfCrossSections):
        me.SetAlpha(profs[i],i,aMin=alphaMin,aMax=alphaMax,inc=alphaInc/2, \
                    xFoilPath=XfoilPath)
    #Out put Fan results
    me.PrintProperties()
    me.WriteProperties(SummaryFile+'2.txt')

#write results to turbogrid files and plot blade profiles in 
#cartesian coordinates
alpha=me.GetAlpha()
delta=me.GetDelta()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i in range(NumberOfCrossSections):
    profs[i].Scale(chord[i],chord[i])
    profs[i].Rotate(np.pi-alpha[i]-beta[i])
    profs[i].P2dToC3d(radius[i])
    stator.BuildStator(delta[i],radius[i])
    writer.AddProfile(profs[i])
    writer2.AddProfile(stator)
    if(i==0):
        inPoint=0.25
        outPoint=0.25
        writer.WriteHub(profs[i],FanInletDomainLength,FanStatorClearance/2)
        writer2.WriteHub(stator,FanStatorClearance/2,StatorOutletDomainLength)
    if(i==9):
        writer.WriteShroud(profs[i],FanInletDomainLength,FanStatorClearance/2)
        writer2.WriteShroud(stator,FanStatorClearance/2,StatorOutletDomainLength)
    pnts=profs[i].points
    profs[i].points[0]=pnts[0]*np.cos(pnts[1])
    profs[i].points[1]=pnts[0]*np.sin(pnts[1])
    ax.scatter(profs[i].points[0],profs[i].points[1],profs[i].points[2])
plt.show()