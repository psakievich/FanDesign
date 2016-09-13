import XFOIL as XF
import os
me=XF.XFOIL()
#me.verbose=False
me.outfile='MyCLCD'
me.RunAlpha(-5.0,5.0,0.25,True)
os.system('clear')
#os.remove('MyCLCD.txt')