import src.SWE_1D as SWE_1D
import os
import numpy as np
from numpy.typing import NDArray
from pytest import approx
import math

# type alias (as per problem set 2)
FArray = NDArray[np.float64]

# Parameters setting
domainLength: float = 20.0  # meter
xTotalNumber: int = 100
timeLength: float = 10.0  # second
FPS: int = 20
TI = SWE_1D.eulerForward  # time integration method
SD = SWE_1D.centralDiff_Order2  # space differentiation method
choice: int = 1  # choice of the initial condition

dx: float = domainLength / xTotalNumber
xArray: FArray = np.linspace(-domainLength / 2, domainLength / 2 - dx, xTotalNumber)
h_i, hu_i = SWE_1D.inputInitialValue(xArray, xTotalNumber, choice)

# run the code
SWE_1D.SWE_1D(
    dx,
    xArray,
    timeLength,
    xTotalNumber,
    FPS,
    TI,
    SD,
    choice,
    h=h_i,
    hu=hu_i,
)

# load the resulting output into numpy arrays
h, x, t = np.loadtxt("output.out", delimiter=" ", usecols=(0, 1, 2), unpack=True)

# load the cached benchmark file
h_b, x_b = np.loadtxt(
    "tests/benchmarks/SWE_1D_tests/output.out",
    delimiter=" ",
    usecols=(0, 1),
    unpack=True,
)


def test_against_benchmark_height():
    """
    Test against the benchmark file for height (produced from a working version of code)

    The benchmark code has exactly the same initial conditions as above
    """

    # check that the ending time outputs are the same
    assert h[-xTotalNumber:] == approx(h_b[-xTotalNumber:], rel=1e-2)


def test_against_benchmark_xn():
    """
    Test against the benchmark file for x (produced from a working version of code)

    The benchmark code has exactly the same initial conditions as above
    """

    # check that the ending time outputs are the same
    assert x[-xTotalNumber:] == approx(x_b[-xTotalNumber:])


def test_beginning_time():
    """
    Check that the beginning time is 0
    """
    assert t[0] == approx(0)


def test_time_format():
    """
    Check that the time is being repeated for each h,x
    """
    assert t[:xTotalNumber] == approx(np.zeros(xTotalNumber))


def test_end_time():
    """
    Check that the end time is the time specified
    """
    assert t[-1] == approx(timeLength)


def test_spatial_discretisation():
    """
    Check that the x is being discretised as specified
    """
    assert x[-xTotalNumber:] == approx(
        np.linspace(
            -domainLength / 2, domainLength / 2, num=xTotalNumber, endpoint=False
        )
    )


def test_initial_condition():
    """
    Check that the initial condition really is the initial condition
    """
    # set up the expected initial condition
    h_init_correct: FArray = [1 + 0.3 * math.exp(-x * x) for x in xArray]

    assert h[:xTotalNumber] == approx(h_init_correct)


# get rid of the test output
os.remove("output.out")
