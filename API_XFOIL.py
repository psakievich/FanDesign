# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 08:43:09 2016

@author: psakievich
"""

import subprocess as sp
import shutil
import sys
import string


ps=sp.Popen(['/Applications/Xfoil.app/Contents/Resources/xfoil'],
            stdin=sp.PIPE,
            stdout=None,
            stderr=None,universal_newlines=True)

def issueCmd(cmd,echo=True):
    ps.stdin.write(cmd+'\n')
    if echo:
        print(cmd)
 
method = 2
if method==1:
    res = ps.communicate( string.join(["NACA 6512","oper","alfa 0.0","cpwr cp_a0.dat","hard","alfa 2.0","cpwr cp_a2.dat","hard","alfa 4.0","cpwr cp_a4.dat","hard","alfa 6.0","cpwr cp_a6.dat","hard"],'\n') )
    print(res)
elif method==2:
    issueCmd('NACA 6512')
 
    """
    GDES              (enter GDES menu)        |
    CADD              (add points at corners)  |  These commands are optional,
              (accept default input)   |  and are recommended only for
              (accept default input)   |  Eppler and Selig airfoils
              (accept default input)   |  to give smoother LE shapes
              (return to Top Level)    |
 
    PANEL           (regenerate paneling since better panel node spacing is needed)
    """
   # issueCmd('GDES')  # enter GDES menu
   # issueCmd('CADD')  # add points at corners
   # issueCmd('')      # accept default input
   # issueCmd('')      # accept default input
   # issueCmd('')      # accept default input
   # issueCmd('')      # accept default input
   # issueCmd('PANEL') # regenerate paneling
   # issueCmd('SAVE e387coords.dat') # save panel geometry
    issueCmd('OPER')
    count = 0
    for aoa in [-10+0.2*i for i in range(2)]:
        issueCmd('ALFA %7.4f' % (aoa,))
        issueCmd('CPWR cpprof%02d.dat' % (count,))
        issueCmd('HARD')
        #print "resp:",ps.stdout.read()
        print ("renaming",count)
        shutil.copyfile('plot.ps','plot%02d.ps' % (count,))
        count += 1
 
    resp = ps.stdout.read()
    print ("resp:",resp)
else:
    pass