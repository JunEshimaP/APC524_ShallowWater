# # -*- coding: utf-8 -*-
# Revised on Thu Nov  3 11:05:28 2022

# @author: Zehua Liu

# Shallow water flow
# ==================

# Solve the one-dimensional shallow water equations:

# .. math::
#     h_t + (hu)_x & = 0 \\
#     (hu)_t + (hu^2 + \frac{1}{2}gh^2)_x & = 0.

# Here h is the total fluid column height, u is the velocity, and g is the gravitational constant.
# Ref: Conservative form in https://en.wikipedia.org/wiki/Shallow_water_equations


# Boundary contions:
#     Periodic boundary condtion
    
    
# Initial conditions:
#     1. Gaussian hump
    
#     h shape:
        
#               /\
#              / \
#         -----   ------- a hump (Gaussian function) in the middle
        
#     u shape:
        
#         ------------------ 0 stationary 
    
#     2. break dums
#     This case is to mimick the water waves after a dam break
    
#     h shape:
        
#                 -----
#                 |   |
#                 |   | 
#                 |   | 
#         --------     ---------- a rectangle in the middle
        
#     u shape:
        
#         ------------------ 0 stationary 
        
        
#     3. traveling waves
#     Traveling waves, of which the shape will change due to nonlinearity
    
#     h shape:
#               /\
#              / \
#             /  \       a sin function wave 
#                \  /
#                \ /
#                \/
               
#     u shape:
        
#         -------------------- constant moving speed 3
        
    
#     4. hitting rocks
#     This case is to mimick the hitting rock on a quiet surface
    
#     h shape: 
        
#         ---------------- constant water height 1
        
#     u shape:
        
      
#                   /\
#                  / \
#                 /  \   a sin function wave; water moving apart from the middle
#             \  /
#             \ /
#             \/
    
    
    
# Finite difference:
#     Nodes on the edges
#     |-|-|-|-
   
    
# Physical constraints to run the simulation:
#     1. "Shallow" assumption: slope = dh/dx << 1 i.e. the domain length need to
#     much larger than the height.
#     2. Periodic BC: input for initial should be a smooth and periodic function of x.
#     3. No dry place for the shallow water layer. Suppose a total height h0 +h, the variation
#     of the height h should be much smaller than the base-line height h0
#     Note that by <<, a ratio of 0.3 is roughly enough.
    
    
# Time integration methods to choose:
#     Suppose an ODE du/dt = f(u), we provide XX methods to do the time integration. Note that 
#     in the following we use u^n and u^n+1 to represent the variables at the current and next
#     step respectively.
    
#     By order of accuracy n, I mean the error is proportional to dt^n
    
#     1. Euler forward
#     u^n+1 = u^n + f(u^n) * dt
    
#     2. 2nd-order Runge-Kutta (RK) method
#     u^n+1/2 = u^n + 0.5 * f(u^n) * dt
#     u^n+1 = u^n + f(u^n+1/2) * dt
    
#     Compared with Euler forward, the RK2 uses the slope at t + 0.5 * dt, which is more accurate
#     Based on the same idea, one can also get the following RK3 and RK4
    
#     3. 3rd-order RK method
#     u1 = u^n + f(u^n) * dt
#     u2 = 0.75 * u^n + 0.25 * u1 - 0.25 * dt * f(u1)
#     u^n+1 = 1.0/3.0 * u^n + 2.0 / 3.0 * u2 - 2.0 / 3.0 * dt * f(u2)
    
#     4. 4th-order RK method
#     u1 = u^n - 0.5 * dt * f(u^n)
#     u2 = u1 + 0.5 * dt * (f(u^n) - f(u1))
#     u3 = u2 + 0.5 * dt * (f(u1) - 2.0 * f(u2))
#     u^n+1 = u3 + 1.0 / 6.0 * dt * 
#     (-f(u) - 2.0 * f(u1) + 4.0 * f(u2) - f(u3))

        
# Spatial differentiation methods to choose:
    
    
#     1. 2nd order central difference
#     df/dx = (f(i+1) - f(i-1)) / (2 * dx)
    
#     2. 1st-order upwind method (flux splitting)
#     f = f+ + f-
#     df+/dx using the left point and current point
#     df-/dx using the right point and current point
    
#     3. 5th-order WENO method (flux splitting)
#     f = f+ + f-
#     The details can be found in this paper:
#         doi:10.1016/j.jcp.2005.02.006
#     It is a higher order interpolation for values at i+1/2 and i-1/2,
#     with upwinding stencils
    

import numpy
import pylab
import math
import os
from scipy.constants import g  # standard acceleration of gravity
from numpy.typing import NDArray
import numba
import time

# type alias (as per problem set 2)
FArray = NDArray[numpy.float64]

@numba.jit(forceobj=True)
def inputInitialValue(xArray: FArray, xTotalNumber: int, choice: int = 4) -> list:
    
    """
    Purpose: set default input values for user to choose
    Input: 
        -- xArray: the x coordinate of grid points
        -- xTotalNumber: the number of divisions
        -- choice: the index of the case
            -- 1 initial gaussian hump
            -- 2 break dams
            -- 3 traveling waves
            -- 4 hitting rocks
    Output:
        -- initial values for h and hu
    """
    
    # initial gaussian hump
    if (choice == 1):
        h_i: FArray = numpy.array([1 + 0.3 * math.exp(-1.0 * x**2) for x in xArray])
        hu_i: FArray = numpy.array([0 for x_index in range(xTotalNumber)])
        
    # break dams
    if (choice == 2):
        h_i: FArray = numpy.array([1 + 0.2 * (abs(x) < 2.5) for x in xArray])
        hu_i: FArray = numpy.array([0 for x_index in range(xTotalNumber)])
        
    # traveling waves
    if (choice == 3):
        h_i: FArray = numpy.array([1 + 0.1 * math.sin(x / 10 * math.pi) for x in xArray])
        hu_i: FArray = 3 * h_i
        
    # hitting rocks
    if (choice == 4):
        h_i: FArray = numpy.array([1 for x in xArray])
        hu_i: FArray = numpy.array([0.5 * math.sin(x / 10 * math.pi) for x in xArray])
    return [h_i, hu_i]


def twoPlot(figNum: int, x: FArray, y1: FArray, y2: FArray, output_flag: int) -> None:
    
    """
    Purpose: plot the output 
    h -- the water height
    hu -- the momentum of the water
    Input:
        -- figNum: number of the figures to plot
        -- x: the x coordinates
        -- y1: the y coordinates for the left-half figure
        -- y2: for the right-half
        -- output_flag:
            -- 1 save figure
            -- 0 not save
    Output:
        -- figure
    """
    
    # Set the x/y labels, titles and limits
    xLabel = "x(m)"
    yLabel1 = "h(m)"
    yLabel2 = "hu(m^2/s)"
    title1 = "Height"
    title2 = "Momentum"
    xLimL: float = x.min()
    xLimR: float = x.max()
    
    
    # Set the figure sizes
    pylab.figure(figNum, figsize=(10,5))
    pylab.subplots_adjust(left=0.08, right=0.97, bottom=0.15, top=0.9, wspace=0.3)
    
    # plot the water height
    pylab.subplot(121)
    pylab.title(title1)
    pylab.plot(x, y1, linewidth=1.0)
    pylab.axis("tight")
    pylab.xlabel(xLabel, fontsize=6)
    pylab.ylabel(yLabel1, fontsize=6)
    pylab.xlim(xLimL, xLimR)
    pylab.xticks(fontsize=6)
    pylab.yticks(fontsize=6)
    pylab.grid()

    # plot the water momentum
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

    # draw the figure
    pylab.draw()
    
    # save the figure
    if output_flag == 1:
        pylab.savefig(title1 + "+" + title2, facecolor="w", edgecolor="w")
    
@numba.jit(forceobj=True)
def loopIndex(vecf: FArray, deviation: int) -> FArray:
    
    """
    Context: periodic boundary contion
    Purpose: to build an array for loop in the index
    Input: 
        -- vecf: an array e.g. [1,2,3]
        -- deviation: the deviation from the current point
            -- e.g. deviation = 1
            -- e.g. output = [1 2 0]
    Output: a index to loop in the array
    """
    
    nums: int = vecf.shape[1]
    loopindex: FArray =  numpy.linspace(deviation,nums+deviation-1,num=nums).astype(int) - \
        (deviation >=0) * nums                                   
    return loopindex

@numba.jit(forceobj=True)
def centralDiff_Order2(vecu: FArray, dx: float) -> FArray:
    
    """
    Purpose: calculate the difference df/dx using 2nd order central difference
    Input:
        -- vecu: an array to be differentiated
        -- dx: the space distance between grid points
    Output:
        -- dfdx: the differentiation of f
        -- i.e. (f(i+1) - f(i-1)) / (2 * dx)
    """
    
    vecf: FArray = numpy.vstack((vecu[1], (vecu[1]**2) / vecu[0] + 0.5 * g * (vecu[0]**2)))
    dfdx: FArray = numpy.gradient(vecf, dx, axis=1)
    dfdx[:,0] = (vecf[:,1] - vecf[:,-1]) / (2.0 * dx)
    dfdx[:,-1] = (vecf[:,0] - vecf[:,-2]) / (2.0 * dx)
    return dfdx

@numba.jit(forceobj=True)
def upwind_Interp(f: FArray, stencil: int) -> FArray:
    
    """
    Purpose: calculate the difference df/dx using 1st order upwind scheme
    Input:
        -- f: an array to be interpolated
        -- stencil: the value at which grid point are used to do the interpolation
    Output:
        -- fp: interpoltaed values
        -- if upwind direction is the left, fp(i+1/2) = fp(i)
    """
    
    fp: FArray = f
    I1: FArray = loopIndex(f, stencil)
    fp = f[:,I1]
    return fp

@numba.jit(forceobj=True)
def upwindDiff_Order1(vecu: FArray, dx: float) -> FArray:
    
    """
    Purpose: calculate the difference df/dx using 1st order upwind scheme
    Input:
        -- vecu: an array to be differentiated
        -- dx: the space distance between grid points
    Output:
        -- dfdx: the differentiation of f
        -- if the upwind direction is the left, then df/dx = (f(i) - f(i-1))/dx
        -- bascically, the idea is to use the information according to physical upwind direction
    """
    
    # form a vector array (2D array) using two 1D array
    vecf: FArray = numpy.vstack((vecu[1], (vecu[1]**2) / vecu[0] + 0.5 * g * (vecu[0]**2)))
    
    # flux splitting f = fp + fm
    alpha: float = math.sqrt(g * numpy.amax(vecu[0])) + numpy.amax(abs(vecu[1]/vecu[0]))
    fp: FArray = 0.5 * (vecf + alpha * vecu)
    fm: FArray = 0.5 * (vecf - alpha * vecu)
    loopindex: FArray =  loopIndex(vecf, -1)

    # interpolation using upwind values
    fpp: FArray = upwind_Interp(fp, 0)
    fmp: FArray = upwind_Interp(fm, 1)
    
    # differentiation using the interpolated vauels at i+1/2 and i-1/2
    # dfdx = (f(i+1/2) - f(i-1/2)) / dx
    dfpdx: FArray = (fpp - fpp[:,loopindex]) / (1.0 * dx)
    dfmdx: FArray = (fmp - fmp[:,loopindex]) / (1.0 * dx)
    dfdx: FArray = (dfpdx + dfmdx)
    return dfdx


@numba.jit(forceobj=True)
def weno_Interp(f: FArray, stencil: FArray) -> FArray:
    
    """
    Purpose: calculate the difference df/dx using 1st order upwind scheme
    Input:
        -- f: an array to be interpolated
        -- stencil: the value at which grid point are used to do the interpolation
    Output:
        -- fp: interpoltaed values using weno methods
        -- more details can be found at the paper:
            doi:10.1016/j.jcp.2005.02.006
    """
    
    fp: FArray = 0 * f
    
    # loop indexs
    Im2: FArray = loopIndex(f, stencil[0])
    Im1: FArray = loopIndex(f, stencil[1])
    Ie0: FArray = loopIndex(f, stencil[2])
    Ip1: FArray = loopIndex(f, stencil[3])
    Ip2: FArray = loopIndex(f, stencil[4])
    
    # vectors at different points
    fm2: FArray = f[:,Im2]
    fm1: FArray = f[:,Im1]
    fe0: FArray = f[:,Ie0]
    fp1: FArray = f[:,Ip1]
    fp2: FArray = f[:,Ip2]
    
    # nonlinear weights
    IS0: FArray = 13.0 / 12.0 * pow(fm2 - 2.0 * fm1 + fe0, 2) + 1.0 / 4.0 * pow(fm2 - 4.0 * fm1 + 3.0 * fe0, 2)
    IS1: FArray = 13.0 / 12.0 * pow(fm1 - 2.0 * fe0 + fp1, 2) + 1.0 / 4.0 * pow(fm1 - fp1, 2)
    IS2: FArray = 13.0 / 12.0 * pow(fe0 - 2.0 * fp1 + fp2, 2) + 1.0 / 4.0 * pow(3.0 * fe0 - 4.0 * fp1 + fp2, 2)
   
    EW: float = 1e-6
    al0: FArray = 1.0 / 10.0 * pow(1.0 / (EW + IS0), 2)
    al1: FArray = 6.0 / 10.0 * pow(1.0 / (EW + IS1), 2)
    al2: FArray = 3.0 / 10.0 * pow(1.0 / (EW + IS2), 2)
    
    w0: FArray = al0 / (al0 + al1 + al2)
    w1: FArray = al1 / (al0 + al1 + al2)
    w2: FArray = al2 / (al0 + al1 + al2)
    
    # interpolated values according to the nonlinear weights
    fp = w0 * (2.0 /6.0 * fm2 - 7.0 / 6.0 * fm1 + 11.0 / 6.0 * fe0) + \
    w1 * (-1.0 / 6.0 * fm1 + 5.0 / 6.0 * fe0 + 2.0 / 6.0 * fp1) + \
    w2 * (2.0 / 6.0 * fe0 + 5.0 / 6.0 * fp1 - 1.0 / 6.0 * fp2)

    return fp

@numba.jit(forceobj=True)
def weno5(vecu: FArray, dx: float) -> FArray:
    
    """
    Purpose: calculate the difference df/dx using 5th order weno scheme
    Input:
        -- vecu: an array to be differentiated
        -- dx: the space distance between grid points
    Output:
        -- dfdx: the differentiation of f
        -- more details can be found at the paper:
            doi:10.1016/j.jcp.2005.02.006

    """
    
    # form a 2D array using two 1D arrays
    vecf: FArray = numpy.vstack((vecu[1], (vecu[1]**2) / vecu[0] + 0.5 * g * (vecu[0]**2)))
    
    # flux splitting
    alpha: float = math.sqrt(g * numpy.amax(vecu[0])) + numpy.amax(abs(vecu[1]/vecu[0]))
    fp: FArray = 0.5 * (vecf + alpha * vecu)
    fm: FArray = 0.5 * (vecf - alpha * vecu)
    
    # prepare weno interpolation stencils
    upstencil: FArray = numpy.linspace(-2,2,num=5).astype(int)
    downstencil: FArray = numpy.array([3, 2, 1, 0, -1])
    loopindex: FArray =  loopIndex(vecf, -1)
    
    # interpolation using weno
    fpp: FArray = weno_Interp(fp, upstencil)
    fmp: FArray = weno_Interp(fm, downstencil)
    
    # differentiation based on the interpolated values
    dfpdx: FArray = (fpp - fpp[:,loopindex]) / (1.0 * dx)
    dfmdx: FArray = (fmp - fmp[:,loopindex]) / (1.0 * dx)
    dfdx: FArray = (dfpdx + dfmdx)
    return dfdx

@numba.jit(forceobj=True)
def eulerForward(h: FArray, hu: FArray, dx: float, dt: float, SD) -> list:
    
    """
    Purpose: time integration using Euler forward
    Input:
        -- h: water height
        -- hu: water momentum
        -- dx: the space distance between grid points
        -- dt: time step
        -- SD: space differetiation method; choices:
            -- centralDiff_Order2
            -- upwindDiff_Order1
            -- weno5
    Output:
        -- [newh, newhu]: the h and hu at next time step
    """
    
    vecu: FArray = numpy.vstack((h, hu))
    newvecu: FArray = vecu - dt * SD(vecu, dx)
    return [newvecu[0], newvecu[1]]

@numba.jit(forceobj=True)
def RK2(h: FArray, hu: FArray, dx: float, dt: float, SD) -> list:
    
    """
    Purpose: time integration using RK2
    Same input and output with eulerForward
    More detail in https://lpsa.swarthmore.edu/NumInt/NumIntSecond.html
    """
    
    vecu: FArray = numpy.vstack((h, hu))
    vecu1: FArray = 0 * vecu
    newvecu: FArray = 0 * vecu
    
    # intermediate estimation at t + dt/2
    vecu1 = vecu - 0.5 * dt * SD(vecu, dx)
    
    # the next step based on the flux at t + dt/2
    newvecu = vecu - dt * SD(vecu1, dx)
    
    return [newvecu[0], newvecu[1]]
    
@numba.jit(forceobj=True)
def RK3(h: FArray, hu: FArray, dx: float, dt: float, SD) -> list:
    
    """
    Purpose: time integration using RK3
    Same input and output with eulerForward
    More detail in p507 High order methods for computational physics
    """
    
    vecu: FArray = numpy.vstack((h, hu))
    vecu1: FArray = 0 * vecu
    vecu2: FArray = 0 * vecu
    newvecu: FArray = 0 * vecu
    
    # step 1
    vecu1 = vecu - dt * SD(vecu, dx)
    
    # step 2
    vecu2 = 0.75 * vecu + 0.25 * vecu1 - 0.25 * dt * SD(vecu1, dx)
    
    # the next step based on the flux at t + dt/2
    newvecu = 1.0 / 3.0 * vecu + 2.0 / 3.0 * vecu2 - 2.0 / 3.0 * dt * SD(vecu2, dx)

    return [newvecu[0], newvecu[1]]

@numba.jit(forceobj=True)
def RK4(h: FArray, hu: FArray, dx: float, dt: float, SD) -> list:
    
    """
    Purpose: time integration using RK4
    Same input and output with eulerForward
    """
    
    vecu: FArray = numpy.vstack((h, hu))
    vecu1: FArray = 0 * vecu
    vecu2: FArray = 0 * vecu
    vecu3: FArray = 0 * vecu
    newvecu: FArray = 0 * vecu
    
    # step 1
    vecu1 = vecu - 0.5 * dt * SD(vecu, dx)
    
    # step 2
    vecu2 = vecu1 + 0.5 * dt * (SD(vecu, dx) - SD(vecu1, dx))
    
    # step 3
    vecu3 = vecu2 + 0.5 * dt * (SD(vecu1, dx) - 2.0 * SD(vecu2, dx)) 
    
    # the next step based on the flux at t + dt/2
    newvecu = vecu3 + 1.0 / 6.0 * dt * (- SD(vecu, dx) - 2.0 * SD(vecu1, dx) + \
                                        4.0 * SD(vecu2, dx) - SD(vecu3, dx)) 
 
    return [newvecu[0], newvecu[1]]


def SWE_1D(
    dx: float, xArray: FArray, timeLength: float, xTotalNumber: int, FPS: int, 
    TI, SD, choice: int, **kwargs) -> None:
    
    """
    Purpose: do the 1D SWE simulation
    Input:
        -- h: water height
        -- hu: water momentum
        -- dx: the space distance between grid points
        -- xArray: the x coordinates for grid points
        -- timeLength: total time to run the simulation
        -- xTotalnumber: number of divisions for the domain
        -- FPS: write the output every 1/FPS (e.g. FPS = 20, output at 0 0.05 0.1 0.15 ...)
        -- TI: time integration method
        -- SD: space differentiation method
        -- choice: choice of the default input
        -- optional input:
            -- h: water height defined from the user interface
            -- hu: water momentum
    Output:
        -- an output recorded the h and hu at output time
    """
    
    # kwargs handling; if user has input h and hu, use it
    if ("h" in kwargs) == False or ("hu" in kwargs) == False:
        # Input initial value
        [h, hu] = inputInitialValue(xArray, len(xArray), choice)
        print("###Using pre-generated inputs!###\n")
    else:
        h = kwargs["h"]
        hu = kwargs["hu"]


    # define h and hu at next time step and output time based on FPS
    newh: FArray = 0 * h
    newhu: FArray = 0 * hu
    timeOutput: FArray = numpy.arange(1.0/FPS, timeLength + 1.0/FPS, 1.0/FPS)
    timeOutput = numpy.append(timeOutput,1e8)
    twoPlot(1, xArray, h, hu, 0)

    # prepare the output flag
    Index_output: int = 0
    Flag_output: int = 0
    t: float = 0.0
    
    # prepare the output and save the initial results
    try:
        os.remove("output.out")
    except Exception:
        pass
    f = open("output.out", "a")
    numpy.savetxt(f, numpy.transpose([h, xArray, t * numpy.ones(xTotalNumber)]))
    print(f"=========Data at t={t} outputed===========")
    
    # time marching
    # adjust the time step when close to the output time
    while t < timeLength:
        dt: float = min(0.1 * dx / math.sqrt(g * h.max()), 0.5/FPS)
        if (
            t + dt > timeOutput[Index_output]
            and t < timeOutput[Index_output]
        ):
            dt = timeOutput[Index_output] - t
            Index_output += 1
            Flag_output = 1

        # Time integration
        [newh, newhu] = TI(h, hu ,dx, dt, SD)
        t += dt
        h = newh
        hu = newhu

        # Output the file
        if Flag_output == 1:
            numpy.savetxt(
                f, numpy.transpose([h, xArray, t * numpy.ones(xTotalNumber)])
            )
            #twoPlot(1, xArray, h, hu, Flag_output)
            print(f"=========Data at t={t} outputed===========")

        Flag_output = 0
        
    f.close()
    return pylab.gcf()



if __name__ == "__main__":
    
    """
    Purpose: default SWE case
    parameters choice:
        
        -- TI: choose time integration method
            -- eulerForward
            -- RK2
            -- RK3
            -- RK4
            
        --SD: choose spatial differentiation method
            -- centralDiff_Order2
            -- upwindDiff_Order1
            -- weno5
    
        -- choice: choose initial conditions
            -- 1 initial gaussian hump
            -- 2 break dams
            -- 3 traveling waves
            -- 4 hitting rocks
    """
    
    # Parameters setting
    domainLength: float = 20.0  # meter
    xTotalNumber: int = 100 #number of divisions
    dx: float = domainLength / xTotalNumber # grid points distance
    xArray: FArray = numpy.linspace(
        -domainLength / 2, domainLength / 2 - dx, xTotalNumber
    ) # x coordinates of grid points
    timeLength: float = 10.0  # second
    FPS: int = 20 # frame rate
    TI = RK4 # time integration method
    SD = weno5 # space differentiation method
    choice: int = 4; # choice of the initial condition
     
    # run the simulation
    # DO NOT REPORT THIS... COMPILATION TIME IS INCLUDED IN THE EXECUTION TIME!
    start = time.time()
    SWE_1D(dx, xArray, timeLength, xTotalNumber, FPS, TI, SD, choice)
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    
    # NOW THE FUNCTION IS COMPILED, RE-TIME IT EXECUTING FROM CACHE
    start = time.time()
    SWE_1D(dx, xArray, timeLength, xTotalNumber, FPS, TI, SD, choice)
    end = time.time()
    print("Elapsed (after compilation) = %s" % (end - start))