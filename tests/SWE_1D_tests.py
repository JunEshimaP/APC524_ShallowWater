import sys

sys.path.insert(0, "../src/")
import SWE_1D

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
timeOutput: FArray = numpy.array([0.5, 1, 2, 1e8])

dx: float = domainLength / xTotalNumber
xArray: FArray = numpy.linspace(-domainLength / 2, domainLength / 2 - dx, xTotalNumber)
h_i, hu_i = SWE_1D.inputInitialValue(xArray, xTotalNumber)


def test_of_outputs():
    SWE_1D.SWE_1D(
        dx, xArray, timeLength, xTotalNumber, h=h_i, hu=hu_i, time_output=timeOutput
    )
    os.remove("Height+Momentum.png")

    assert filecmp.cmp("../output0.5.out", "output0.5.out", shallow=False)
    assert filecmp.cmp("../output1.0.out", "output1.0.out", shallow=False)
    assert filecmp.cmp("../output2.0.out", "output2.0.out", shallow=False)
    os.remove("output0.5.out")
    os.remove("output1.0.out")
    os.remove("output2.0.out")
