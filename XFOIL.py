# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 12:44:44 2016

@author: psakievich
"""
import numpy as np
import subprocess as sp

#Class for running XFOIL in Python
class XFOIL:
    #set default constructor
    def __init__(self):
        self.outfile='default'
        self.xFoilPath='/Applications/Xfoil.app/Contents/Resources/xfoil'
        self.reynolds=5000.0
        self.NACA=6512
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
        StdCmd('NACA '+str(self.NACA))
        StdCmd('OPER')
        StdCmd('ITER '+str(self.iterations))
        StdCmd('VISC '+str(self.reynolds))
        StdCmd('RE '+str(self.reynolds))
        StdCmd('MACH '+str(self.mach))
        StdCmd('PACC')
        StdCmd(self.outfile)
        StdCmd(' ')
        if(seq):
            StdCmd('Aseq '+str(Amin)+' '+str(Amax)+' '+str(Ainc))
        else:
            StdCmd('Alfa '+str(Amin))
        StdCmd('PACC')
        StdCmd(' ')
        StdCmd('QUIT ')
        ps.communicate()
