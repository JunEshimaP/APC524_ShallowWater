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
from scipy.constants import g  # standard acceleration of gravity
from numpy.typing import NDArray

# type alias (as per problem set 2)
FArray = NDArray[numpy.float64]

print("Welcome to 1D-SWE")


# Parameters setting
domainLength: float = 20.0  # meter
xTotalNumber: int = 100
timeLength: float = 4.0  # second
timeOutput: FArray = numpy.array([0.5, 1, 2, 1e8])


dx: float = domainLength / xTotalNumber
xArray: FArray = numpy.linspace(-domainLength / 2, domainLength / 2 - dx, xTotalNumber)


# Input
def inputInitialValue() -> tuple[FArray, FArray]:
    # initial gaussian hump
    h_i: FArray = numpy.array([1 + 0.4 * math.exp(-1.0 * x**2) for x in xArray])
    hu_i: FArray = numpy.array([0 for x_index in range(xTotalNumber)])
    return h_i, hu_i


# Simple output
def twoPlot(figNum: int, x: FArray, y1: FArray, y2: FArray) -> None:
    xLabel = "x(m)"
    yLabel1 = "h(m)"
    yLabel2 = "hu(m^2/s)"
    title1 = "Height"
    title2 = "Momentum"
    xLimL: float = xArray.min()
    xLimR: float = xArray.max()
    yLimL1: float = 0.0
    yLimR1: float = 1.5 + 0.2

    pylab.figure(figNum, figsize=(8, 3), dpi=300)
    pylab.subplots_adjust(left=0.08, right=0.97, bottom=0.15, top=0.9, wspace=0.3)

    pylab.subplot(121)
    pylab.title(title1)
    pylab.plot(x, y1, linewidth=1.0)
    pylab.axis("tight")
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
    pylab.axis("tight")
    pylab.xlabel(xLabel, fontsize=6)
    pylab.ylabel(yLabel2, fontsize=6)
    pylab.xlim(xLimL, xLimR)
    # pylab.ylim(yLimL2, yLimR2)
    pylab.xticks(fontsize=6)
    pylab.yticks(fontsize=6)
    pylab.grid()

    pylab.draw()
    pylab.savefig(title1 + "+" + title2, facecolor="w", edgecolor="w")


# Second order central difference
def centralDiff_Order2(f: FArray) -> FArray:
    dfdx: FArray = numpy.gradient(f, dx)
    dfdx[0] = (f[1] - f[-1]) / (2.0 * dx)
    dfdx[-1] = (f[0] - f[-2]) / (2.0 * dx)
    return dfdx


def SWE_1D() -> None:

    # Input initial value
    h, hu = inputInitialValue()
    newh: FArray = 0 * h
    newhu: FArray = 0 * hu
    twoPlot(1, xArray, h, hu)

    # Time marching
    Index_output: int = 0
    Flag_output: int = 0
    t: float = 0.0
    while t < timeLength:
        dt: float = 0.1 * dx / math.sqrt(g * h.max())
        if t + dt > timeOutput[Index_output] and t < timeOutput[Index_output]:
            dt = timeOutput[Index_output] - t
            Index_output += 1
            Flag_output = 1

        # Euler forward
        newh = h - dt * centralDiff_Order2(hu)
        newhu = hu - dt * centralDiff_Order2((hu**2) / h + 0.5 * g * (h**2))
        t += dt
        h = newh
        hu = newhu

        # Output the file
        if Flag_output == 1:
            numpy.savetxt("output.out", (h, xArray, t * numpy.ones(xTotalNumber)))
            twoPlot(1, xArray, h, hu)
            print(f"=========Data at t={t} outputed===========")

        Flag_output = 0

    print("finish 1D-SWE!")


if __name__ == "__main__":
    SWE_1D()
