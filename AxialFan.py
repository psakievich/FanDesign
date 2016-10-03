# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 07:57:43 2016
AXIAL FAN CLASS
@author: psakievich
"""
import os
import numpy as NP
import XFOIL as XF

class AxialFan:
    def __init__(self,dHub,dTip,RPM,CFM,SP,zB):
        self.__dHub=float(dHub)            #dHub -> hub diameter (in)
        self.__dTip=float(dTip)            #dTip -> fan diameter at tip of blades (in)
        self.__RPM=float(RPM )             #RPM -> Rotational speed
        self.__CFM=float(CFM)              #CFM -> Volumetric flow rate
        self.__SP=float(SP)                #SP -> Static Pressure (in H2O)
        self.__zB=int(zB)                  #zB -> Number of blades on the fan
        #Default values -------------------------------------------------
        self.__aA=(self.__dTip**2-self.__dHub**2)*NP.pi/576.0
        self.__vA=self.__CFM/self.__aA
        self.__nu=1.64*10.0**-4.0*60.0  #kinematic viscosity of air (ft^2/min @ 70 deg F)
        self.__c=67716.56               #speed of sound feet per minute
        self.SetProfileNumber(10)
        self.SetConstantChord(3.4*self.__dHub/self.__zB)
        self.SetCl()
        self.SetReynolds()
        self.SetMach()
    #Get specs used to initialize object
    def GetInitSpecs(self):
        #Returns values in a tuple
        return (self.__dHub,self.__dTip,self.__RPM,self.__CFM,self.__SP,
                self.__zB)
    def SetViscosity(self, nu):
        self.__nu=nu
    def SetSpeedOfSound(self, ss):
        self.__c=ss
    def SetProfileNumber(self, n):
        n=int(n)
        self.__numProfiles=n
        self.__l=NP.empty(n)
        self.__alpha=NP.empty(n)
        self.__cl=NP.empty(n)
        self.__l.fill(None)
        self.__alpha.fill(None)
        self.__cl.fill(None)
        self.__r=NP.linspace(0.5*self.__dHub,0.5*self.__dTip,n)
        self.__vR=233.0*10.0**5/self.__RPM*self.__SP/self.__r
        self.__vB=self.__RPM*2.0*NP.pi/12.0*self.__r
        self.__w=NP.sqrt(self.__vA**2+(self.__vB-0.5*self.__vR)**2)
        self.__beta=NP.arctan(self.__vA/(self.__vB-0.5*self.__vR))
        self.__delta=NP.arctan(self.__vR/self.__vA)
    def SetConstantChord(self,chord):
        self.__l.fill(chord)
    def SetChordOfProfile(self,chord,i):
        self.__l[i]=chord
    def SetCl(self):
        self.__cl=self.__SP/(self.__RPM*self.__zB*self.__l* \
            self.__w*3.43*10.0**-9)
    def SetReynolds(self):
        self.__re=self.__w*self.__l/self.__nu/12.0
    def SetMach(self):
        self.__mach=self.__w/self.__c
    def CheckDimensions(self):
        Test=[False,False]
        if(self.__dHub>=19000.0/self.__RPM*NP.sqrt(self.__SP)):
            Test[0]=True
        if(self.__dTip>=NP.sqrt(self.__dHub**2+61.0*self.__CFM/self.__RPM)):
            Test[1]=True
        return Test
    def PrintProperties(self):
        bTests=self.CheckDimensions()
        r2d=180.0/NP.pi
        print('-'*75)
        print('Axial Fan Design')
        print('Coded by: Phil Sakievich')
        print('Last Update: 10/3/2016')
        print('-'*75)
        print('RPM={} \nCFM={} \nSP(inW)={} \nID(in)={} \nOD(in)={} \nzB={}'.format( \
            self.__RPM,self.__CFM,self.__SP,self.__dHub,self.__dTip,self.__zB))
        print('vA(ft/min)={:<6.2f} \naA(ft^2)={:<6.4f} \nnu(ft^2/min)={:<6.5e} \nC(ft/min)={}'.format(
            self.__vA,self.__aA,self.__nu,self.__c))
        print('{:<20} {}'.format('Is hub big enough?',bTests[0]))
        print('{:<20} {}'.format('Is OD big enough?',bTests[1]))
        print('\nVelocities(ft/min):')
        print('-'*75)
        print('{:>12} {:>12} {:>12} {:>12}'.format('Radius(in)','Radial', \
            'Blade','Relative'))
        for i in range(self.__r.shape[0]):
            print('{:12.4f} {:12.4f} {:12.4f} {:12.4f}'.format(self.__r[i],
                  self.__vR[i],self.__vB[i],self.__w[i]))
        print('\nScales:')
        print('-'*75)
        print('{:>12} {:>12} {:>12} {:>12}'.format('Radius(in)','Chord(in)', \
              'Reynolds','Mach'))
        for i in range(self.__r.shape[0]):
            print('{:12.4f} {:12.4f} {:12.4f} {:12.4f}'.format(self.__r[i],
                  self.__l[i],self.__re[i],self.__mach[i]))
        print('\nAngles(degrees):')
        print('-'*75)
        print('{:>12} {:>12} {:>12} {:>12} {:>12}'.format('Radius(in)','Alpha', \
              'Beta','Delta','CL'))
        for i in range(self.__r.shape[0]):
            print('{:12.4f} {:12.4f} {:12.4f} {:12.4f} {:12.4f}'. \
                format(self.__r[i],self.__alpha[i]*r2d,self.__beta[i]*r2d,
                       self.__delta[i]*r2d,self.__cl[i]))
    def SetAlpha(self,Airfoil,i,aMin=-10.0,aMax=10.0,inc=0.5):
        if(os.path.isdir('work')==False):
            os.mkdir('work')
        temp=Airfoil.name
        Airfoil.name='./work/'+temp
        Airfoil.WriteXfoil()
        Calc=XF.XFOIL()
        Calc.reynolds=self.__re[i]
        Calc.mach=self.__mach[i]
        Calc.verbose=False
        Calc.infile=Airfoil.name+'XF'+Airfoil.fileExtension
        Calc.fromFile=True
        Airfoil.name=temp
        Calc.outfile='./work/AlphaSweep'+str(i)
        if(os.path.isfile(Calc.outfile+Calc.fileExtension)):
            os.remove(Calc.outfile+Calc.fileExtension)
        Calc.RunAlpha(aMin,aMax,inc,True)
        Result=XF.ReadPACC(Calc.outfile+Calc.fileExtension)
        self.__alpha[i]=NP.interp(self.__cl[i],Result[1],Result[0])*NP.pi/180.0
    def GetAlpha(self):
        return self.__alpha.copy()
    def GetBeta(self):
        return self.__beta.copy()
    def GetDelta(self):
        return self.__delta.copy()
    def GetCl(self):
        return self.__cl.copy()
    def GetChord(self):
        return self.__l.copy()
    def GetMach(self):
        return self.__mach.copy()
    def GetReynolds(self):
        return self.__re.copy()
    def GetRadius(self):
        return self.__r.copy()
    def WriteProperties(self,fName):
        f=open(fName,'w')
        bTests=self.CheckDimensions()
        r2d=180.0/NP.pi
        f.write('-'*75+'\n')
        f.write('Axial Fan Design\n')
        f.write('Coded by: Phil Sakievich\n')
        f.write('Last Update: 10/3/2016\n')
        f.write('-'*75+'\n')
        f.write('RPM={} \nCFM={} \nSP(inW)={} \nID(in)={} \nOD(in)={} \nzB={}'.format( \
            self.__RPM,self.__CFM,self.__SP,self.__dHub,self.__dTip,self.__zB))
        f.write('vA(ft/min)={:<6.2f} \naA(ft^2)={:<6.4f} \nnu(ft^2/min)={:<6.5e} \nC(ft/min)={}'.format(
            self.__vA,self.__aA,self.__nu,self.__c))
        f.write('\n{:<20} {}'.format('Is hub big enough?',bTests[0]))
        f.write('\n{:<20} {}'.format('Is OD big enough?',bTests[1]))
        f.write('\n \nVelocities(ft/min):')
        f.write('\n'+'-'*75)
        f.write('\n{:>12} {:>12} {:>12} {:>12}'.format('Radius(in)','Radial', \
            'Blade','Relative'))
        for i in range(self.__r.shape[0]):
            f.write('\n{:12.4f} {:12.4f} {:12.4f} {:12.4f}'.format(self.__r[i],
                  self.__vR[i],self.__vB[i],self.__w[i]))
        f.write('\n \nScales:')
        f.write('\n'+'-'*75)
        f.write('\n{:>12} {:>12} {:>12} {:>12}'.format('Radius(in)','Chord(in)', \
              'Reynolds','Mach'))
        for i in range(self.__r.shape[0]):
            f.write('\n{:12.4f} {:12.4f} {:12.4f} {:12.4f}'.format(self.__r[i],
                  self.__l[i],self.__re[i],self.__mach[i]))
        f.write('\n \nAngles(degrees):')
        f.write('\n'+'-'*75)
        f.write('\n{:>12} {:>12} {:>12} {:>12} {:>12}'.format('Radius(in)','Alpha', \
              'Beta','Delta','CL'))
        for i in range(self.__r.shape[0]):
            f.write('\n{:12.4f} {:12.4f} {:12.4f} {:12.4f} {:12.4f}'. \
                format(self.__r[i],self.__alpha[i]*r2d,self.__beta[i]*r2d,
                       self.__delta[i]*r2d,self.__cl[i]))