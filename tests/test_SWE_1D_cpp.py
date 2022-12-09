import src.SWE_1D as SWE_1D
import filecmp
import os
import numpy as np
from numpy.typing import NDArray
from pytest import approx

# type alias (as per problem set 2)
FArray = NDArray[np.float64]

# Parameters setting
domainLength: float = 20.0  # meter
xTotalNumber: int = 100
timeLength: float = 10.0  # second
FPS: int = 20
TI = SWE_1D.eulerForward  # time integration method
SD = SWE_1D.centralDiff_Order2  # space differentiation method
choice: int = 1  # choice of the initial condition (Gaussian hump, to match cpp)

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
h, x = np.loadtxt("output.out", delimiter=" ", usecols=(0, 1), unpack=True)

# load the output from the cached benchmark c++ file into numpy arrays
h_cpp, x_cpp = np.loadtxt(
    "tests/benchmarks/SWE_1D_cpp_tests/h_default_cpp_end.txt",
    delimiter=" ",
    usecols=(0, 1),
    unpack=True,
)


def test_compwithcpp_height():
    """
    Compares Python code with the c++ code for height (at end time)

    Note: the c++ code only outputs the final state, whereas the python outputs the states
    per frame as specified.
    """

    # first, get the last timestep outputs of height, position

    h_py = h[-xTotalNumber:]

    # due to slight differences in the scheme (very minor), and due to difference
    # of outputt method in c++ and python, only check approximately the same

    assert h_cpp == approx(h_py, rel=1e-2)


def test_compwithcpp_x():
    """
    Compares Python code with the c++ code for x

    Note: the c++ code only outputs the final state, whereas the python outputs the states
    per frame as specified.
    """

    x_py = x[-xTotalNumber:]

    # due to slight differences in the scheme (very minor), and due to difference
    # of output method in c++ and python, only check approximately the same
    assert x_cpp == approx(x_py)


os.remove("output.out")
