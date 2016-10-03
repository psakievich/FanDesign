# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 17:02:26 2016

@author: psakievich
"""
import os
import numpy as np
from matplotlib import pyplot as plt
import XFOIL as XF
import Profiles
import TurboGrid

dHub=2.5
dOut=4.69
dArea=np.pi*(dOut**2-dHub**2)/576.0
nu=1.64*10.0**-4.0
CFM=450.0
RPM=11000.0
Chord=0.773
NumBlades=11.0
SP=2.0
NumProfiles=10
dRadius=0.5*(dOut-dHub)/(NumProfiles-1.0)
vA=CFM/dArea

WriteProfile=TurboGrid.Profile()
WriteProfile.SetPercentages(NumProfiles)
WriteProfile.fileName='testTurbo'
GetAlpha=XF.XFOIL()
GetAlpha.iterations=100
blade=Profiles.AxialProfile()
blade.Read('testProfile.txt')
blade.name='NACA6512'
#center blade
blade.Shift(-0.5)
#blade.chord=Chord
blade.WriteXfoil()
alpha=[]

for i in range(NumProfiles):
    rCur=0.5*dHub+i*dRadius
    vR=233.0*10**5.0/RPM*SP/rCur
    vB=2.0*rCur*np.pi/12.0*RPM
    w=np.sqrt(vA**2.0+(vB-0.5*vR)**2.0)
    CL=SP/(3.43*10**-9.0*RPM*NumBlades*Chord*w)
    Mach=w/(1125.33*60.0)
    Re=w*Chord/nu/12.0/60.0
    print('Radius, Chord: ',rCur,Chord)
    print('Velocity: ',vA,vR,vB,w)
    print('CL: ',CL)
    print('Mach: ',Mach)
    print('Reynolds: ',Re)
    bCalc=1#int(input('Compute? (1=yes, 0=no) '))
    if(bCalc==1):
        GetAlpha.reynolds=Re
        GetAlpha.mach=Mach
        GetAlpha.fromFile=True
        GetAlpha.infile=blade.name+'XF'+blade.fileExtension
        GetAlpha.outfile=blade.name+str(i)
        if(os.path.isfile(GetAlpha.outfile+GetAlpha.fileExtension)):
            os.remove(GetAlpha.outfile+GetAlpha.fileExtension)
        #GetAlpha.RunCl(CL)
        GetAlpha.RunAlpha(-7.0,7.0,0.5,True)
        Result=XF.ReadPACC(GetAlpha.outfile+GetAlpha.fileExtension)
        alfa=np.interp(CL,Result[1],Result[0])     
        alpha.append(alfa)
        printer=blade.Copy()
        printer.Rotate(alfa)
        printer.Scale(Chord)
        printer.P2dToC3d(rCur)
        WriteProfile.AddProfile(printer)
        plt.plot(printer.points[1][:],printer.points[2][:],
                 label='R={}'.format(rCur))
        plt.legend()
        plt.axis([-0.5,0.5,-0.5,0.5])
plt.show()
        
    
    


