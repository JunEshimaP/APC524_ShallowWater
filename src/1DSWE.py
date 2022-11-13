# -*- coding: utf-8 -*-
"""
Revised on Thu Nov  3 11:05:28 2022

@author: Zehua Liu
"""

"""
Shallow water flow
==================

Solve the one-dimensional shallow water equations:

.. math::
    h_t + (hu)_x & = 0 \\
    (hu)_t + (hu^2 + \frac{1}{2}gh^2)_x & = 0.

Here h is the total fluid column height, u is the velocity, and g is the gravitational constant.
Ref: Conservative form in https://en.wikipedia.org/wiki/Shallow_water_equations

Boundary contions:
    Periodic boundary contion
    
Initial conditions:
    Gaussian hump in the middle
    
Finite difference:
    Nodes on the edges

|-|-|-|-
"""
import numpy
import pylab
import matplotlib
import math
from scipy.constants import g      #standard acceleration of gravity

print ("Welcome to 1D-SWE")


# Parameters setting
domainLength = 20.   # meter
xTotalNumber = 100
timeLength = 4.     # second
timeOutput = numpy.array([0.5, 1, 2, 1e8])


dx = domainLength / xTotalNumber
xArray = numpy.linspace(-domainLength/2, domainLength/2 - dx, xTotalNumber)


# Input 
def inputInitialValue():
    # initial gaussian hump
    h_i = numpy.array([1 + 0.4 * math.exp(-1. * x**2) for x in xArray])
    hu_i = numpy.array([0 for x_index in range(xTotalNumber)])       
    return h_i, hu_i

# Simple output
def twoPlot(figNum, x, y1, y2):   
    xLabel='x(m)'
    yLabel1='h(m)'
    yLabel2='hu(m^2/s)'
    title1 = 'Height'
    title2 = 'Momentum'
    xLimL = xArray.min()
    xLimR = xArray.max()
    yLimL1 = 0
    yLimR1 = 1.5 + 0.2
    
    
    
    pylab.figure(figNum, figsize=(8, 3), dpi=300)
    pylab.subplots_adjust(left=0.08, right=0.97, bottom=0.15, top=0.9, wspace=0.3)

    pylab.subplot(121)
    pylab.title(title1)
    pylab.plot(x, y1, linewidth=1.0)
    pylab.axis('tight')
    pylab.xlabel(xLabel, fontsize=6)
    pylab.ylabel(yLabel1, fontsize=6)
    pylab.xlim(xLimL, xLimR)
    pylab.ylim(yLimL1, yLimR1)
    pylab.xticks(fontsize=6)
    pylab.yticks(fontsize=6)
    pylab.grid()

    pylab.subplot(122)
    pylab.title(title2)
    pylab.plot(x, y2, linewidth=1.0)
    pylab.axis('tight')
    pylab.xlabel(xLabel, fontsize=6)
    pylab.ylabel(yLabel2, fontsize=6)
    pylab.xlim(xLimL, xLimR)
    #pylab.ylim(yLimL2, yLimR2)
    pylab.xticks(fontsize=6)
    pylab.yticks(fontsize=6)
    pylab.grid()

    pylab.draw()
    pylab.savefig(title1+'+'+title2, facecolor='w', edgecolor='w')


#Second order central difference
def centralDiff_Order2(f):
    dfdx = numpy.gradient(f, dx)
    dfdx[0] = (f[1] - f[-1]) / (2. * dx)
    dfdx[-1] = (f[0] - f[-2]) / (2. * dx)
    return dfdx


def SWE_1D():

    # Input initial value
    h, hu = inputInitialValue();
    newh = 0 * h
    newhu = 0 * hu
    twoPlot(1,xArray, h, hu)
    
    
    # Time marching
    Index_output = 0
    Flag_output = 0
    t = 0.
    while t < timeLength :
        dt = 0.1 * dx / math.sqrt(g * h.max())
        if t + dt > timeOutput[Index_output] and t < timeOutput[Index_output]:
            dt = timeOutput[Index_output] - t
            Index_output += 1
            Flag_output = 1
        
        # Euler forward
        newh = h - dt * centralDiff_Order2(hu)
        newhu = hu - dt * centralDiff_Order2((hu**2)/h+0.5*g*(h**2))
        t += dt
        h = newh
        hu = newhu
        
        # Output the file
        if Flag_output == 1:
            numpy.savetxt('output.out', (h, xArray, t * numpy.ones(xTotalNumber)))  
            twoPlot(1,xArray, h, hu)
            print(f"=========Data at t={t} outputed===========")
           
        Flag_output = 0


        
    
    print ("finish 1D-SWE!")




if __name__ == "__main__":
    SWE_1D()
