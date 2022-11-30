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
    Periodic boundary condtion
    
Initial conditions:
    1. Gaussian hump in the middle
    
    2. Rock hitting the water
    ToDo ...
    
Finite difference:
    Nodes on the edges
    |-|-|-|-
    
Physical constraints to run the simulation:
    1. "Shallow" assumption: slope = dh/dx << 1 i.e. the domain length need to
    much larger than the height.
    2. Periodic BC: input for initial should be a smooth and periodic function of x.
    3. No dry place for the shallow water layer. Suppose a total height h0 +h, the variation
    of the height h should be much smaller than the base-line height h0
    Note that by <<, a ratio of 0.3 is roughly enough.
    
Time integration methods to choose:
    Suppose an ODE du/dt = f(u), we provide XX methods to do the time integration. Note that 
    in the following we use u^n and u^n+1 to represent the variables at the current and next
    step respectively.
    1. Explicit methods
    
        1.1 Euler forward
        u^n+1 = u^n + f(u^n) * dt
        
        1.2 2nd-order Runge-Kutta method
        u^n+1/2 = u^n + 0.5 * f(u^n) * dt
        u^n+1 = u^n + f(u^n+1/2) * dt
        
        1.3 others
        TODO ...
        
    2. Implicit methods
    TODO ...
    
Spatial differentiation methods to choose:
    1. 2nd order central difference
    df/dx = (f(i+1) - f(i-1)) / (2 * dx)
    
    2. 5th order WENO scheme
    TODO ...
        
        
        
"""
import numpy
import pylab
import math
import os
from scipy.constants import g  # standard acceleration of gravity
from numpy.typing import NDArray

# type alias (as per problem set 2)
FArray = NDArray[numpy.float64]


# Input used for benchmarking/testing
def inputInitialValue(xArray: FArray, xTotalNumber: int) -> tuple[FArray, FArray]:
    # initial gaussian hump
    h_i: FArray = numpy.array([1 + 0.4 * math.exp(-1.0 * x**2) for x in xArray])
    hu_i: FArray = numpy.array([0 for x_index in range(xTotalNumber)])
    return h_i, hu_i


# Simple output
def twoPlot(figNum: int, x: FArray, y1: FArray, y2: FArray, output_flag: int) -> None:
    xLabel = "x(m)"
    yLabel1 = "h(m)"
    yLabel2 = "hu(m^2/s)"
    title1 = "Height"
    title2 = "Momentum"
    xLimL: float = x.min()
    xLimR: float = x.max()
    yLimL1: float = 0.0
    yLimR1: float = 1.5 + 0.2

    pylab.figure(figNum, figsize=(10,5))
    pylab.subplots_adjust(left=0.08, right=0.97, bottom=0.15, top=0.9, wspace=0.3)

    pylab.subplot(121)
    pylab.title(title1)
    pylab.plot(x, y1, linewidth=1.0)
    pylab.axis("tight")
    pylab.xlabel(xLabel, fontsize=6)
    pylab.ylabel(yLabel1, fontsize=6)
    pylab.xlim(xLimL, xLimR)
    # pylab.ylim(yLimL1, yLimR1)
    pylab.xticks(fontsize=6)
    pylab.yticks(fontsize=6)
    pylab.grid()

    pylab.subplot(122)
    pylab.title(title2)
    pylab.plot(x, y2, linewidth=1.0)
    pylab.axis("tight")
    pylab.xlabel(xLabel, fontsize=6)
    pylab.ylabel(yLabel2, fontsize=6)
    pylab.xlim(xLimL, xLimR)
    pylab.xticks(fontsize=6)
    pylab.yticks(fontsize=6)
    pylab.grid()

    pylab.draw()
    if output_flag == 1:
        pylab.savefig(title1 + "+" + title2, facecolor="w", edgecolor="w")
    
    


# Second order central difference
def centralDiff_Order2(f: FArray, dx: float) -> FArray:
    dfdx: FArray = numpy.gradient(f, dx)
    dfdx[0] = (f[1] - f[-1]) / (2.0 * dx)
    dfdx[-1] = (f[0] - f[-2]) / (2.0 * dx)
    return dfdx

# Euler forward
def eulerForward(h: FArray, hu: FArray, dx: float, dt: float, SD) -> list:
    newh: FArray = 0 * h
    newhu: FArray = 0 * hu
    
    newh = h - dt * SD(hu, dx)
    newhu = hu - dt * SD((hu**2) / h + 0.5 * g * (h**2), dx)
    return [newh, newhu]
    
# 2nd-order Runge-Kutta method
# https://lpsa.swarthmore.edu/NumInt/NumIntSecond.html
def RK2(h: FArray, hu: FArray, dx: float, dt: float, SD) -> list:
    newh: FArray = 0 * h
    newhu: FArray = 0 * hu
    h1: FArray = 0 * h
    hu1: FArray = 0 * hu
    
    # intermediate estimation at t + dt/2
    h1 = h - 0.5 * dt * SD(hu, dx)
    hu1 = hu - 0.5 * dt * SD((hu**2) / h + 0.5 * g * (h**2), dx)
    
    # the next step based on the flux at t + dt/2
    newh = h - dt * SD(hu1, dx)
    newhu = hu - dt * SD((hu1**2) / h1 + 0.5 * g * (h1**2), dx)
    
    return [newh, newhu]
    
# 3rd-order Runge-Kutta method
# p507 High order methods for computational physics
def RK3(h: FArray, hu: FArray, dx: float, dt: float, SD) -> list:
    newh: FArray = 0 * h
    newhu: FArray = 0 * hu
    h1: FArray = 0 * h
    hu1: FArray = 0 * hu
    h2: FArray = 0 * h
    hu2: FArray = 0 * hu
    
    # step 1
    h1 = h -  dt * SD(hu, dx)
    hu1 = hu - dt * SD((hu**2) / h + 0.5 * g * (h**2), dx)
    
    # step 2
    h2 = 0.75 * h + 0.25 * h1 -  0.25 * dt * SD(hu1, dx)
    hu2 = 0.75 * hu + 0.25 * hu1 - 0.25 * dt * SD((hu1**2) / h1 + 0.5 * g * (h1**2), dx)    
    
    # the next step based on the flux at t + dt/2
    newh = 1.0 / 3.0 * h + 2.0 / 3.0 * h2 - 2.0 / 3.0 * dt * SD(hu2, dx)
    newhu = 1.0 / 3.0 * hu + 2.0 / 3.0 * hu2 - 2.0 /3.0 * dt * SD((hu2**2) / h2 + 0.5 * g * (h2**2), dx)
    
    return [newh, newhu]

# 4th-order Runge-Kutta method
# p507 High order methods for computational physics
def RK4(h: FArray, hu: FArray, dx: float, dt: float, SD) -> list:
    newh: FArray = 0 * h
    newhu: FArray = 0 * hu
    h1: FArray = 0 * h
    hu1: FArray = 0 * hu
    h2: FArray = 0 * h
    hu2: FArray = 0 * hu
    h3: FArray = 0 * h
    hu3: FArray = 0 * hu
    
    # step 1
    h1 = h - 0.5 * dt * SD(hu, dx)
    hu1 = hu - 0.5 * dt * SD((hu**2) / h + 0.5 * g * (h**2), dx)
    
    # step 2
    h2 =  h1 + 0.5 * dt * (SD(hu, dx) - SD(hu1, dx))
    hu2 = hu1 + 0.5 * dt * (SD((hu**2) / h + 0.5 * g * (h**2), dx) - 
                            SD((hu1**2) / h1 + 0.5 * g * (h1**2), dx))  
    
    # step 3
    h3 =  h2 + 0.5 * dt * (SD(hu1, dx) - 2.0 * SD(hu2, dx))
    hu3 = hu2 + 0.5 * dt * (SD((hu1**2) / h1 + 0.5 * g * (h1**2), dx) - 
                            2.0 * SD((hu2**2) / h2 + 0.5 * g * (h2**2), dx))  
    
    # the next step based on the flux at t + dt/2
    newh = h3 + 1.0 / 6.0 * dt * ( - SD(hu, dx) - 2.0 * SD(hu1, dx) + 
                                  4.0 * SD(hu2, dx) - SD(hu3, dx))
    newhu = hu3 + 1.0 / 6.0 * dt * ( - SD((hu**2) / h + 0.5 * g * (h**2), dx)
                                    - 2.0 * SD((hu1**2) / h1 + 0.5 * g * (h1**2), dx)
                                    + 4.0 * SD((hu2**2) / h2 + 0.5 * g * (h2**2), dx)
                                    - SD((hu3**2) / h3 + 0.5 * g * (h3**2), dx))
    return [newh, newhu]

def SWE_1D(
    dx: float, xArray: FArray, timeLength: float, xTotalNumber: int, FPS: int, TI, SD, **kwargs
) -> None:
    """
    1D shallow water wave equations.
    h = input height, hu = input momentum, time_output = output array
    """
    # kwargs handling
    if ("h" in kwargs) == False or ("hu" in kwargs) == False:
        # Input initial value
        h, hu = inputInitialValue(xArray, len(xArray))
        print("###Using pre-generated inputs!###\n")
    else:
        h = kwargs["h"]
        hu = kwargs["hu"]

    #if "time_output" in kwargs:
        #timeOutput = kwargs["time_output"]

    newh: FArray = 0 * h
    newhu: FArray = 0 * hu
    timeOutput: FArray = numpy.arange(1.0/FPS, timeLength + 1.0/FPS, 1.0/FPS)
    timeOutput = numpy.append(timeOutput,1e8)
    twoPlot(1, xArray, h, hu, 0)

    # Time marching
    Index_output: int = 0
    Flag_output: int = 0
    t: float = 0.0
    os.remove('output.out')
    f=open('output.out','a')
    numpy.savetxt(
        f, numpy.transpose([h, xArray, t * numpy.ones(xTotalNumber)])
    )
    print(f"=========Data at t={t} outputed===========")
    while t < timeLength:
        dt: float = min(0.01 * dx / math.sqrt(g * h.max()), 0.5/FPS)
        if (
            t + dt > timeOutput[Index_output]
            and t < timeOutput[Index_output]
        ):
            dt = timeOutput[Index_output] - t
            Index_output += 1
            Flag_output = 1

        # Euler forward
        [newh, newhu] = TI(h, hu ,dx, dt, SD)
        t += dt
        h = newh
        hu = newhu

        # Output the file
        if Flag_output == 1:
            numpy.savetxt(
                f, numpy.transpose([h, xArray, t * numpy.ones(xTotalNumber)])
            )
            twoPlot(1, xArray, h, hu, Flag_output)
            print(f"=========Data at t={t} outputed===========")

        Flag_output = 0
    f.close()

    return pylab.gcf()



if __name__ == "__main__":
    # Parameters setting
    domainLength: float = 20.0  # meter
    xTotalNumber: int = 100
    timeLength: float = 4.0  # second
    FPS: int = 20
    #TI = eulerForward # time integration method
    TI = RK4
    SD = centralDiff_Order2 # space differentiation method
    #timeOutput: FArray = numpy.array([0.5, 1, 2, 1e8])

    dx: float = domainLength / xTotalNumber
    xArray: FArray = numpy.linspace(
        -domainLength / 2, domainLength / 2 - dx, xTotalNumber
    )

    SWE_1D(dx, xArray, timeLength, xTotalNumber, FPS, TI, SD)
    
