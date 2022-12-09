"""
Script to plot the output from c++ file
(the default set up - see SWE_1D.cpp/SWE_1D.py)

Uses matplotlib, deliberately made similar to moviemake class
"""
import numpy as np
import matplotlib.pyplot as plt

h, x = np.loadtxt(
    r"src/c++_files/h_default_cpp_end.txt", delimiter=" ", usecols=(0, 1), unpack=True
)

plt.plot(x, h)
plt.ylim(0, 2)
plt.xlim(-10.0, 10.0)
plt.xlabel("x")
plt.ylabel("height")
plt.title(f"c++ Output of Default Set Up at T=10")

# save the plot
plt.savefig("c++_output.png")

plt.show()
