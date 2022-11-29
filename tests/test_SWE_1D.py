import src.SWE_1D as SWE_1D
import filecmp
import os
import numpy
from numpy.typing import NDArray

# type alias (as per problem set 2)
FArray = NDArray[numpy.float64]

# Parameters setting
domainLength: float = 20.0  # meter
xTotalNumber: int = 100
timeLength: float = 4.0  # second
#timeOutput: FArray = numpy.array([0.5, 1, 2, 1e8])
FPS: int = 20

dx: float = domainLength / xTotalNumber
xArray: FArray = numpy.linspace(-domainLength / 2, domainLength / 2 - dx, xTotalNumber)
h_i, hu_i = SWE_1D.inputInitialValue(xArray, xTotalNumber)


def test_of_outputs():
    SWE_1D.SWE_1D(
        dx, xArray, timeLength, xTotalNumber, FPS, h=h_i, hu=hu_i
    )
    os.remove("Height+Momentum.png")

    assert filecmp.cmp("tests/benchmarks/SWE_1D_tests/output.out", "output.out", shallow=False)
    os.remove("output.out")

