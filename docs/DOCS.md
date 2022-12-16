# Basic Documentation
Overview documentation for the software in this repository

## `user_interface.py`

### Class `makemovie`
Builds the movie output from the SWE_1D simulator.

Input
+ `filename : string`

    This is the location and name of the output of SWE_1D.py (.txt file)

+ `N : int` 
    
    This is the number intervals in spatial coordinates

Methods
+ `__init__ :`

    Initialise values

+ `readvalues :`

    read out the output from SWE_1D.py

+ `initplot :`

    configure the plot

+ `update :`

    update plot every frame

+ `createanimation :`

    create the animation using matplotlib.animation

+ `saveanimation :`

    save the animation into .mp4

### Class `PrintLogger`
Generates a logging object so that console output may be redirected to the applet window.
    This class was in large part gathered from StackOverflow: https://stackoverflow.com/questions/68198575/how-can-i-displaymy-console-output-in-tkinter

Input
+ `textbox : ` a `Tkinter.ScrolledText()` instance

Methods
+ `__init__ :`

   saves the textbox input as a public reference for the class

+ `write : `

    handles the outputting of the text to the console

+ `flush : `

    allows the object to behave like a file

### Class `InteractiveUserInterface`
Generates and manages a stand-alone simulation window for the 1D SWE project

Input
+ `master :` an instance of the `tk.Tk()` class

    This requires a user to initialize an instance of the `tk.Tk()` class (a tk window) that is built into the simulation window

Methods
+ `__init__ :`

    initializes the window, building the individual tab framework and file menu

+ `intro_tab_construction :`

    builds the intro tab and its associated widgets

+ `input_tab_construction :`

    builds the input tab and its associated widgets

+ `numerical_simulation_tab_construction :`

    builds the numerical simulation tab and its associated widgets

+ `output_tab_construction :`

    updates the video player slider in the output tab's values

+ `update_slider :`

    updates the video player slider in the output tab's values

+ `settime_slider :`

    sets the value of the video player slider in the output tab based on the user's input

+ `play_pause : `

    controls the play/pause button in the video player

+ `pack_input_tab_plot :`

    redraws the plot figure in the input_tab_plot (used when domain/curve type changes)

+ `update_plot :`

    redraws the plot figure in the input_tab_plot (used when sliders are adjusted)

+ `run_custom_simulation :`

    executes the SWE_1D() method from SWE_1D.py, and makemovie() class, using the user-defined inputs

+ `run_default_simulation :`

    executes the SWE_1D() method from SWE_1D.py, and makemovie() class, using several pre-determined inputs

+ `clear_console_input :`
    
    clears the console in the "Input" tab

+ `clear_console_numerical :`

    clears the console in the "Numerical Simulation" tab


## SWE_1D.py
Here, `FArray = NDArray[numpy.float64]`

### `inputInitialValue(xArray: FArray, xTotalNumber: int, choice: int) -> tuple[FArray, FArray]:`
Sets the default input values that the user may choose from

Input
+ `xArray`

    the x coordinate of grid points

+ `xTotalNumber`

    the number of divisions

+ `choice`

    The index of the case
    - `1` initial gaussian hump
    - `2` break dams
    - `3` traveling waves
    - `4` hitting rocks

Output
+ initial values for `h` and `hu`

### `twoPlot(figNum: int, x: FArray, y1: FArray, y2: FArray, output_flag: int) -> None`
Plots the output

Input
+ `figNum`

    number of the figures to plot

+ `x`

    the x coordinates

+ `y1`

    the y coordinates for the left-half figure

+ `y2`

    the y coordinates for the right-half figure

+ `output_flag`
    - `1` save figure
    - `2` do not save figure


### `loopIndex(vecf: FArray, deviation: int)) -> FArray`
For periodic boundary conditions; builds an array for looping in the index

Input
+ `vecf` 

    an array e.g. `[1, 2, 3]`

+ `deviation`

    the deviation from the current point

Output
+ An index for looping

### `upwind_Interp(f: FArray, stencil: int) -> FArray`
Interpolation for calculating the difference df/dx using 1st order upwind scheme

Input
+ `f`

    an array to be interpolated

+ `stencil`

    the value at which grid points are used to do the interpolation

Output
+ `fp`

    interpolated values
    - if upwind direction is the left, `fp((i+1)/2) = fp(i)`

### `upwindDiff_Order1(vecu: FArray, dx: float) -> FArray`
Calculates the difference df/dx using 1st order upwind scheme

Input
+ `vecu`

    an array to be differentiated

+ `dx`

    the space distance between grid points

Output
+ `dfdx`

    the differentiation of `f` with respect to `x`

### `centralDiff_Order2(vecu: FArray, dx: float) -> FArray`
Calculate the difference df/dx using 2nd order central difference

Input
+ `vecu`

    an array to be differentiated

+ `dx`

    the space distance between grid points

Output
+ `dfdx`

    the differentiation of `f` with respect to `x`

### `weno_Interp(f: FArray, stencil: FArray) -> FArray`
Interpolation for calculating the difference df/dx using the 5th order WENO scheme

Input
+ `f`

    an array to be interpolated

+ `stencil`

    the value at which grid points are used to do the interpolation

Output
+ `fp`

    interpolated values
    - if upwind direction is the left, `fp((i+1)/2) = fp(i)`

### `weno5(vecu: FArray, dx: float) -> FArray`
Calculates the difference df/dx using the 5th order WENO scheme

Input
+ `vecu`

    an array to be differentiated

+ `dx`

    the space distance between grid points

Output
+ `dfdx`

    the differentiation of `f` with respect to `x`

### `eulerForward(h: FArray, hu: FAray, dx: float, dt: float, SD) -> list1`
Performs time integration using Euler forward method

Input
+ `h`

    water height

+ `hu`

    water momentum

+ `dx`

    the space distance between grid points

+ `dt`

    the time distance between time steps

+ `SD`
    spatial differentiation method, choices:
    - `centralDiff_Order2`
    - `upwindDiff_Order1`
    - `weno5`

Output
+ `[newh, newhu]`

    the `h` and `hu` at next time step

### `RK2(h: FArray, hu: FArray, dx: float, dt: float, SD) -> list`
Performs time integration using RK2, more detail in https://lpsa.swarthmore.edu/NumInt/NumIntSecond.html

Input
+ `h`

    water height

+ `hu`

    water momentum

+ `dx`

    the space distance between grid points

+ `dt`

    the time distance between time steps

+ `SD`
    spatial differentiation method, choices:
    - `centralDiff_Order2`
    - `upwindDiff_Order1`
    - `weno5`

Output
+ `[newh, newhu]`

    the `h` and `hu` at next time step

### `RK3(h: FArray, hu: FArray, dx: float, dt: float, SD) -> list`
Performs time integration using RK3

Input
+ `h`

    water height

+ `hu`

    water momentum

+ `dx`

    the space distance between grid points

+ `dt`

    the time distance between time steps

+ `SD`
    spatial differentiation method, choices:
    - `centralDiff_Order2`
    - `upwindDiff_Order1`
    - `weno5`

Output
+ `[newh, newhu]`

    the `h` and `hu` at next time step

### `RK4(h: FArray, hu: FArray, dx: float, dt: float, SD) -> list`
Performs time integration using RK4

Input
+ `h`

    water height

+ `hu`

    water momentum

+ `dx`

    the space distance between grid points

+ `dt`

    the time distance between time steps

+ `SD`
    spatial differentiation method, choices:
    - `centralDiff_Order2`
    - `upwindDiff_Order1`
    - `weno5`

Output
+ `[newh, newhu]`

    the `h` and `hu` at next time step

### `SWE_1D(dx: float, xArray: FArray, timelength: float, xTotalNumber: int, FPS: int, TI, SD, choice: int, **kwards) -> None`
Performs the 1D SWE numerical simulation

Input
+ `h`

    water height

+ `hu`

    water momentum

+ `dx`

    the space distance between grid points

+ `xArray`

    the x coordinates for grid points

+ `timeLength`

    total time to run the simulation

+ `xTotalNumber`

    the number of divisions for the domain in x

+ `FPS`

    write the output every `1/FPS` seconds

+ `TI`

    the time integration method

+ `SD`
    
    the spatial differentiation method

+ `choice`

    choice of the initial conditions

+ optional input (handled via `**kwargs`)
    - `h` 

        the water height defined from the user interface

    - `hu`

        the water momentum defined from the user interface

Output
+ an output file containing `h` and `hu` information at each gridpoint at every output time step
