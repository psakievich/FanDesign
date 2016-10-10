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

wing=Profiles.AxialProfile()
wing.Read('testProfile.txt')
wing.name='NACA'
wing.Shift(-0.5)
profs=[]
writer=TG.Profile()

me=AF.AxialFan(2.5,4.69,11000,450,2.0,11)
writer.SetPercentages(10)
radius=me.GetRadius()
ratio=radius[1]/radius[0]
chord=me.GetChord()
for i in range(radius.shape[0]):
    profs.append(wing.Copy())
    if(i>0):
        ratio=3.4*2.0*radius[i]/11.0
        me.SetChordOfProfile(ratio,i)
        profs[i].Scale(1.0,chord[0]/ratio)
        
me.SetCl()
me.SetReynolds()
me.SetMach()
chord=me.GetChord()
for i in range(10):
    me.SetAlpha(profs[i],i,-7.0,7.0,0.5)

me.PrintProperties()
me.WriteProperties('FanDesigned.txt')

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
        inPoint=np.zeros([1,3])
        outPoint=np.copy(inPoint)
        inPoint=inPoint+profs[i].points[:,0]+[0,0,0.1]
        sze=int(profs[i].points.shape[1])
        outPoint=outPoint+profs[i].points[:,sze/2-1]-[0,0,0.1]
        writer.WriteHub(profs[i],inPoint,outPoint)
    if(i==9):
        inPoint=np.zeros([1,3])
        outPoint=np.copy(inPoint)
        inPoint=inPoint+profs[i].points[:,0]+[0,0,0.1]
        sze=int(profs[i].points.shape[1])
        outPoint=outPoint+profs[i].points[:,sze/2-1]-[0,0,0.1]
        writer.WriteShroud(profs[i],inPoint,outPoint)
    pnts=profs[i].points
    profs[i].points[0]=pnts[0]*np.cos(pnts[1])
    profs[i].points[1]=pnts[0]*np.sin(pnts[1])
    ax.scatter(profs[i].points[0],profs[i].points[1],profs[i].points[2])
plt.show()