# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 12:44:44 2016

@author: psakievich
"""
import subprocess as sp
import numpy as np
#Class for running XFOIL in Python
class XFOIL:
    #set default constructor
    def __init__(self):
        self.outfile='default'
        self.fileExtension='.txt'
        self.infile=None
        self.fromFile=False
        self.xFoilPath='/Applications/Xfoil.app/Contents/Resources/xfoil'
        self.reynolds=5000.0
        self.naca=6512
        self.iterations=70
        self.mach=0.1
        self.verbose=False
    def RunAlpha(self,Amin,Amax=0,Ainc=0,seq=False):
        ps=sp.Popen([self.xFoilPath],stdin=sp.PIPE,stdout=None,stderr=None,
                    universal_newlines=True)
        def StdCmd(cmd):
            ps.stdin.write(cmd+'\n')
            #ps.wait()
            if (self.verbose):
                print(cmd)
        if(self.fromFile):
            StdCmd('LOAD '+self.infile)
        else:
            StdCmd('NACA '+str(self.naca))
        StdCmd('GDES')
        StdCmd('')
        StdCmd('')
        StdCmd('')
        StdCmd('')
        StdCmd('PANEL')
        StdCmd('OPER')
        StdCmd('ITER '+str(self.iterations))
        StdCmd('VISC '+str(self.reynolds))
        StdCmd('RE '+str(self.reynolds))
        StdCmd('MACH '+str(self.mach))
        StdCmd('PACC')
        StdCmd(self.outfile+self.fileExtension)
        StdCmd(' ')
        if(seq):
            StdCmd('Aseq '+str(Amin)+' '+str(Amax)+' '+str(Ainc))
        else:
            StdCmd('Alfa '+str(Amin))
        StdCmd('PACC')
        StdCmd(' ')
        StdCmd('QUIT ')
        ps.communicate()
    def RunCl(self,Cmin,Cmax=0,Cinc=0,seq=False):
        ps=sp.Popen([self.xFoilPath],stdin=sp.PIPE,stdout=None,stderr=None,
                universal_newlines=True)
        def StdCmd(cmd):
            ps.stdin.write(cmd+'\n')
            #ps.wait()
            if (self.verbose):
                print(cmd)
        if(self.fromFile):
            StdCmd('LOAD '+self.infile)
        else:
            StdCmd('NACA '+str(self.naca))
        StdCmd('OPER')
        StdCmd('ITER '+str(self.iterations))
        StdCmd('VISC '+str(self.reynolds))
        StdCmd('RE '+str(self.reynolds))
        StdCmd('MACH '+str(self.mach))
        StdCmd('PACC')
        StdCmd(self.outfile+self.fileExtension)
        StdCmd(' ')
        if(seq):
            StdCmd('Cseq '+str(Cmin)+' '+str(Cmax)+' '+str(Cinc))
        else:
            StdCmd('Cl '+str(Cmin))
        StdCmd('PACC')
        StdCmd(' ')
        StdCmd('QUIT ')
        ps.communicate()  
        
def ReadPACC(fName):
    f=open(fName,'r')
    i=0
    for line in f:
        i=i+1
    NumPnts=i-12
    PACC=np.zeros([7,NumPnts])
    f.seek(0)
    i=0
    j=0
    for line in f:
        if(i<12):
            pass
        else:
            data=line.strip().split()
            for k in range(7):
                PACC[k,j]=float(data[k])
            j=j+1
        i=i+1
    f.close()
    return PACC