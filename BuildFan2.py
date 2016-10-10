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

#Setup profile
wing=Profiles.AxialProfile()
wing.Read('testProfile.txt')
wing.name='NACA'
wing.Shift(-0.5)
profs=[]
#Setup turbogrid writer
writer=TG.Profile()
writer.SetPercentages(10)
#Declare fan inputs
me=AF.AxialFan(2.5,4.69,11000,450,2.0,11)
radius=me.GetRadius()
ratio=radius[1]/radius[0]
chord=me.GetChord()

#Modify chord length
for i in range(radius.shape[0]):
    profs.append(wing.Copy())
    if(i>0):
        ratio=3.4*2.0*radius[i]/11.0
        me.SetChordOfProfile(ratio,i)
        profs[i].Scale(1.0,chord[0]/ratio)
#Set flow parameters        
me.SetCl()
me.SetReynolds()
me.SetMach()
chord=me.GetChord()

#Calculate angle of attack for desired Coefficient of lift
for i in range(10):
    me.SetAlpha(profs[i],i,-7.0,7.0,0.5)
#Out put Fan results
me.PrintProperties()
me.WriteProperties('FanDesigned.txt')

#write results to turbogrid files and plot blade profiles in 
#cartesian coordinates
alpha=me.GetAlpha()
beta=me.GetBeta()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i in range(10):
    profs[i].Scale(chord[i],chord[i])
    profs[i].Rotate(np.pi-alpha[i]-beta[i])
    profs[i].P2dToC3d(radius[i])
    writer.AddProfile(profs[i])
    if(i==0):
        inPoint=0.25
        outPoint=0.25
        writer.WriteHub(profs[i],inPoint,outPoint)
    if(i==9):
        writer.WriteShroud(profs[i],inPoint,outPoint)
    pnts=profs[i].points
    profs[i].points[0]=pnts[0]*np.cos(pnts[1])
    profs[i].points[1]=pnts[0]*np.sin(pnts[1])
    ax.scatter(profs[i].points[0],profs[i].points[1],profs[i].points[2])
plt.show()