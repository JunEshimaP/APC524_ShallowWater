/**
More or less identical to SWE_1D. Solves the 1D shallow water wave equations:
    h_t + (hu)_x & = 0 \\
    (hu)_t + (hu^2 + \frac{1}{2}gh^2)_x & = 0.

This script acts as a performance comparison and also as an actual data comparison.

h is the height
u is the horizontal velocity
g is the gravitational constant, 9.81

The set up corresponds to the default that we are doing in python

Boundary conditions:
    Periodic

Initial conditions:
    Gaussian hump 1 + 0.3 exp(-x*x)
    zero velocity

Domain:
    [-10 10-Dx]

Number of spatial divisions 100:
    -10, -10+20*1/100,..., -10+20*99/100

We use central difference method

Duration:
    T=10

Temporal discretisation:
    Dt = 0.0001 * dx / sqrt(g * 2)
    [this is different from the user_interface since we replaced h.max with 2
    and the pre-factor is much smaller]

We use explicit forward Euler

Output:
    Just the end values. Explicitly of the form:

    h(x_0,10) x_0
    h(x_1,10) x_1
    ...
    h(x_{N-1},10) x_{N-1}

    The output is written into "h_default_cpp_end.txt"

*/
#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>
#include <cstdlib>
#include <tuple>

// gravitational constant
double g = 9.81;

// domain [-halfL, halfL-Dx]
double halfL = 10.0;

// spatial discretisation
int N = 100;
double Dx = 2.0 * halfL / N;

// total duration
double T = 10.0;

// temporal discretisation (take very fine)
double Dt = 0.0001 * Dx / sqrt(g * 2);

// number of time loops
int M = floor(T / Dt);

int main()
{
    /**

    Run the loops  in the main since the program is short.

    Since we are doing explicit Euler, we need to keep track of
    the next time step and old time step at the same time.

    Also, since we have edge cases, we need to write these
    out separately. We could do things such as ghost values,
    but this is faster.

    The steps are:

        1. Initialise
        2. Run the time steps
        3. Print out the end results to a separate file
        (with filename "h_default_cpp_end.txt")

    */

    // x array
    std::vector<double> x;

    // Initialise vectors (have an old and new
    // place holder)
    std::vector<double> h;
    std::vector<double> hu;
    std::vector<double> newh;
    std::vector<double> newhu;

    for (int i = 0; i < N; i++)
    {
        // initialise with gaussians for heights
        x.push_back(Dx * i - 10.0);
        h.push_back(1 + 0.3 * exp(-x[i] * x[i]));
        hu.push_back(0.0);
        newh.push_back(1 + 0.3 * exp(-x[i] * x[i]));
        newhu.push_back(0.0);
    }

    // The below is a coefficient that will be used over and over again.
    // Pre-computed for speed.
    double discret_coef = Dt / (2 * Dx);

    // the loop
    for (int n = 0; n < M; n++)
    {
        /**
        We go from left to right. For memory management purposes,
        we calculate 0,1, 2, ..., N-1


        Since we have periodic boundary conditions:
            Replace -1 by N-1
            Replace N by 0

        We calculate the new height h,
        then the new horizontal momentum hu
        */

        // left (note: periodic)
        newh[0] = h[0] - discret_coef * (hu[1] - hu[N - 1]);

        // internal
        for (int i = 1; i < N - 1; i++)
        {
            newh[i] = h[i] - discret_coef * (hu[i + 1] - hu[i - 1]);
        }

        // right (note: periodic)
        newh[N - 1] = h[N - 1] - discret_coef * (hu[0] - hu[N - 2]);

        // left (note: periodic)
        newhu[0] = hu[0] - discret_coef * ((hu[1] * hu[1] / h[1]) - (hu[N - 1] * hu[N - 1] / h[N - 1]) + 0.5 * g * (h[1] * h[1] - h[N - 1] * h[N - 1]));

        // internal
        for (int i = 1; i < N - 1; i++)
        {
            newhu[i] = hu[i] - discret_coef * ((hu[i + 1] * hu[i + 1] / h[i + 1]) - (hu[i - 1] * hu[i - 1] / h[i - 1]) + 0.5 * g * (h[i + 1] * h[i + 1] - h[i - 1] * h[i - 1]));
        }

        // right (note: periodic)
        newhu[N - 1] = hu[N - 1] - discret_coef * ((hu[0] * hu[0] / h[0]) - (hu[N - 2] * hu[N - 2] / h[N - 2]) + 0.5 * g * (h[0] * h[0] - h[N - 2] * h[N - 2]));

        // update
        for (int i = 0; i < N; i++)
        {
            h[i] = newh[i];
            hu[i] = newhu[i];
        }
    }

    // now save the values
    std::ofstream fwh("./h_default_cpp_end.txt", std::ofstream::out);
    if (fwh.is_open())
    {
        /**
        Output in the same format as expected for SWE_1D.py
        i.e. of the form
        h(x_0,10) x_0
        h(x_1,10) x_1
        ...
        h(x_{N-1},10) x_{N-1}
        */

        for (int i = 0; i < N; i++)
        {
            fwh << h[i] << " " << x[i] << std::endl;
        }

        // make sure to close the file
        fwh.close();
    }
    else
        std::cout << "Unable to open file";
}
