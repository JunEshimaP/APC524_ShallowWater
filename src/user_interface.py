import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import numpy as np
from matplotlib.pylab import close
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from SWE_1D import *
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import math
from tkVideoPlayer import *
from pathlib import Path
from PIL import ImageTk, Image
import sys
import os


class makemovie:
    """Sets up an interactive output

    Input
    -----
    filename : string
        This is the location and name of the output of SWE_1D.py (.txt file)

    N : int
        This is the number intervals in spatial coordinates

    Methods
    -------
    __init__ :
        initialise values

    readvalues :
        read out the output from SWE_1D.py

    initplot :
        configure the plot

    update :
        update plot every frame

    createanimattion :
        create the animation using matplotlib.animation

    saveanimation :
        save the animation into .mp4
    """

    def __init__(self, filename: Path, N: int, xlim: float, FPS: int):
        """
        Initialise the variables.

        self.filename:
            the filename of the data file with the output from our numerical
            solvers

        self.N:
            the number of x points taken in the spatial discretisation

        self.plottedgraphfig, self.plottedgraph.figax:
            This sets up the plots to be animated.

            [For details, see https://matplotlib.org/stable/api/animation_api.html]

        self.curve:
            This is the curve that will be changed every frame

        self.xlim:
            This is the right most limit of the x domain

        self.FPS:
            The frames per second at which the movie will be made

        """
        self.filename: Path = filename
        self.N = N

        # set up matplotlib as in matplotlib.animation documentation
        self.plottedgraphfig, self.plottedgraphfigax = plt.subplots()
        (self.curve,) = self.plottedgraphfigax.plot([], [])
        self.xlim = xlim
        self.FPS = FPS

    # read out values from .txt file
    def readvalues(self):
        """
        Use the np.loadtxt file to immediately get numpy arrays
        in order to get the desired physical values.
        [much simpler than csv etc]

        The physical set up is:

        x is discretised with N, so:
        x_0 = 0, x_1 = L/N , ..., x_i = i L/N, ..., x_N = L

        (note, we only look at the right half of the physical set up [-L,L]
        for the set up - please see the report for details)

        Time is discretised by M, so:
        t_0 = 0, t_1 = T/M, ..., t_i = i T/M, ..., t_M = T

        The file to be read is expected to be in the following format:

        h (x_0, t_0) x_0 t_0
        h (x_1, t_0) x_1 t_0
        h (x_2, t_0) x_2 t_0
        ….
        h (x_N, t_0) x_N t_0
        h (x_0, t_1) x_0 t_1
        h (x_1, t_1) x_1 t_1
        h (x_2, t_1) x_2 t_1
        …
        h (x_N, t_1) x_N t_1
        h (x_0, t_1) x_0 t_2
        ...
        h (x_0, t_M) x_0 t_M
        h (x_1, t_M) x_1 t_M
        h (x_2, t_M) x_2 t_M
        ...
        h (x_N, t_M) x_N t_M


        self.h:
            stores the height values as numpy array

            h(x_i,t_j) can be accessed by h[i+j*N]

            h is of the form
            [h (x_0, t_0) h (x_1, t_0) h (x_2, t_0) ... h (x_N, t_0) h (x_0, t_1) ...]

        self.x:
            stores the x values as numpy array

            x is of the form
            [x_0 x_1 x_2 ... x_N x_0 x_1 x_2 ... x_N ...]

        self.t:
            stores the t values as t array

            t is of the form
            [t_0 t_0 t_0 ... t_0 t_1 t_1 t_1 ... t_1 ...]

        self.numberoftimesteps:
            stores the number of timesteps in the output
            [this could be made redundant if the moviemaker coordinated
            better with the numerical algoithm solver]

        """
        self.h, self.x, self.t = np.loadtxt(
            self.filename, delimiter=" ", usecols=(0, 1, 2), unpack=True
        )
        # we need the number of timesteps in the program from the
        # output so that we know how many frames to expect later.
        numberofvalues = self.h.size
        self.numberoftimesteps = int(numberofvalues / self.N)

    # initialise the plot
    def initplot(self):
        """
        Initialise the plot in a way that the plot is easy to see

        i.e. the plotted x domain is the same as the domain of the
        computational domain

        The y limits are chosen so that we would never physically reach
        the limits (0 and double the initial height).

        Since we are dealing with shallow water waves, we plot from the bottom
        to emphasise the set up (we could zoom into h_min, h_max, but then this may
        not look verty shallow).

        """
        self.plottedgraphfigax.set_xlim(-self.xlim, self.xlim)
        self.plottedgraphfigax.set_ylim(0, 2)
        return (self.curve,)

    # update the plot every frame
    def update(self, frame):
        """
        This method plots the curve for each frame.

        The complicated indexing of self.x and self.h is in such a form since
        the x values and h values are stored in a vector with each frame added
        in one after the other (see comments in the readvalues() method)

        """
        x_val = []
        y_val = []
        for i in range(self.N):
            x_val.append(self.x[i + frame * self.N])
            y_val.append(self.h[i + frame * self.N])
        self.curve.set_data(x_val, y_val)
        return (self.curve,)

    # create animation
    def createanimation(self):
        """
        We wish to create the animation using animation.FuncAnimation.

        For details, see:
        https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html

        self.plottedgraphfig:
            The matplotlib object in which we will create the animation

        self.update:
            How each frame will be updated

        frames:
            The list of frames that will be produced

        init_func:
            Initial plot (see self.initplot comments)

        blit:
            A technical point about optimising drawing
            [see https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html]

        """
        # read in the values from the output
        self.readvalues()

        # create the animation using animation.FuncAnimation
        self.ani = animation.FuncAnimation(
            self.plottedgraphfig,
            self.update,
            frames=range(self.numberoftimesteps),
            init_func=self.initplot,
            blit=True,
        )

    # save the animaton
    def saveanimation(self):
        """
        This method saves the movie using FFmpegwriter. We use the fps information
        obtained from the user to write out the movie.

        See https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FFMpegWriter.html

        Note: ffmpeg needs to be installed.

        At the end of the method, there is a notification that the movie has
        been made.

        """
        # create the animation
        self.createanimation()

        # set up the writer
        # note: need to have ffmpeg installed.
        writervideo = animation.FFMpegWriter(fps=self.FPS)
        self.ani.save(
            Path("src/sample_movies/sample_generated.mp4"), writer=writervideo
        )
        print("Movie Made")


class PrintLogger:
    """
    Generates a logging object so that console output may be redirected to the applet window.
    This class was in large part gathered from StackOverflow: https://stackoverflow.com/questions/68198575/how-can-i-displaymy-console-output-in-tkinter

    Input
    -----
    textbox : a tk.ScrolledText() instance
        This class uses a ScrolledText() instance to mimic the behavior of a console

    Methods
    -------
    __init__ :
        safes the textbox input as a public reference for the class

    write :
        handles the outputting of the text to the console

    flush :
        allows the object to behave like a file
    """

    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, text):
        """
        In order of lines, this method:
        1. makes the textbox editable
        2. inserts the text to the end of the textbox
        3. scrolls the textbox to the end of the statement
        4. sets the textbox to be read-only
        """
        self.textbox.configure(state="normal")
        self.textbox.insert("end", text)
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def flush(self):
        pass


class InteractiveUserInterface:
    """
    Generates and manages a stand-alone simulation window for the 1D SWE project.

    Input
    -----
    master : an instance of the tk.Tk class
        This requires a user to initialize an instance of the tk.Tk() class (a tk window) that is built into the simulation window

    Methods
    -------
    __init__ :
        initializes the window, building the individual tab framework and file menu

    intro_tab_construction :
        builds the intro tab and its associated widgets

    input_tab_construction :
        builds the input tab and its associated widgets

    numerical_simulation_tab_construction :
        builds the numerical simulation tab and its associated widgets

    output_tab_constructions :
        builds the output tab and its associated widgets

    update_slider :
        updates the video player slider in the output tab's values

    settime_slider :
        sets the value of the video player slider in the output tab based on the user's input

    play_pause :
        controls the play/pause button in the video player

    pack_input_tab_plot :
        redraws the plot figure in the input_tab_plot (used when domain/curve type changes)

    update_plot :
        redraws the plot figure in the input_tab_plot (used when sliders are adjusted)

    run_custom_simulation :
        executes the SWE_1D() method from SWE_1D.py, and makemovie() class, using the user-defined inputs

    run_default_simulation :
        executes the SWE_1D() method from SWE_1D.py, and makemovie() class, using several pre-determined inputs
    """

    def __init__(self, master):
        """
        Initializes the window, building the individual tab framework and file menu

        self.root:
            the master Tk() instance window that the simulation is being built inside of

        menu_bar:
            the standard file menu structure for program.
            The only function is to have a clean exit of the program (self.root.destroy) via File -> Exit

        tab_control:
            the controlling object for the building of the tab frames
        """
        self.root = master
        # Menu bar
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)

        self.root.config(menu=menu_bar)
        # Create the tabs for the plotting
        tab_control = ttk.Notebook(self.root)
        intro_tab = ttk.Frame(tab_control)
        input_tab = ttk.Frame(tab_control)
        self.numerical_simulation_tab = ttk.Frame(tab_control)
        output_tab = ttk.Frame(tab_control)

        tab_control.add(intro_tab, text="Introduction")
        tab_control.add(input_tab, text="Input")
        tab_control.add(self.numerical_simulation_tab, text="Numerical Simulation")
        tab_control.add(output_tab, text="Output")

        self.intro_tab_construction(intro_tab)
        self.input_tab_construction(input_tab)
        self.numerical_simulation_tab_construction(self.numerical_simulation_tab)
        self.output_tab_construction(output_tab)
        tab_control.pack(expand=1, fill="both")

    def intro_tab_construction(self, tab):
        """
        Builds the intro tab and its associated widgets

        tab:
            the input tab which points this function to the frame where it should build these widgets

        grouped_frame:
            more aesthetic packing of the widgets within the tab if they are nested in a frame within the tab

        image_*:
            the images used in the tab; uses the Pillow library to handle image interfacing with Tkinter

        body_*:
            a tk.Label() object holding an element of the body of the tab (paragraphs/images)

        *_title:
            a tk.Label() object holding a section/subsection title

        label_equations and label_image:
            The two image_* objects stored in tk.Label() objects; uniquely require anchoring of the images to the instance of tk.Label()
        """
        grouped_frame = tk.Frame(tab)

        ### Text and image(s)
        title_text = r"Welcome to the 1D Shallow-Water Equation Simulator!"
        tab_description_title_text = r"How to Use This Program"
        paragraph_1 = (
            "This applet is designed to simulate the 1D shallow-water equations that describe the wave motion of a fluid surface. "
            "This simple case of fluid flow allows the user to play with parameters like wave height, initial conditions, and "
            "different numerical simulation schemes to see how these knobs affect the fluid dynamics."
        )
        paragraph_2 = (
            "\nThe 1D shallow-water equations are derived from the famous Navier-Stokes fluid equations, in the specific case where "
            "the pool of water has a much larger horizontal length scale than the vertical length scale. "
            "The mathematical equations and schematic describing this system are as follows: "
        )
        paragraph_3 = "This program has separated the simulation into three components:"
        paragraph_input = (
            "The input tab allows users to describe the state of the system prior to simulating. "
            "Several options are available to the user in text boxes to describe the spatial discretization and how long to simulate. "
            'The text box for "X Limit" describes the length of the pool (from 0 to <X Limit>). '
            'The text box for "T Limit" describes the length of time to simulate (from 0 to <T Limit>).'
            'The text box for "Frames per second" allow the user to choose how many simulation frames to output per second of video. '
            "The user also has the option to set the shape of the initial wave, with a dropdown box to switch between a sinusoid and "
            "a gaussian. There are several slidersto adjust the shape of these curves. "
            "To the right of these options is a plot which allows the user to preview their input wave shape. "
            'The user must click the "Update Plot" button to see changes to the input wave shape, as well as get the appropriate curve sliders.'
        )
        paragraph_numerical_simulation = "The numerical simulation tab allows users to choose the numerical schemes and then run either their custom simulation or a default simulation."
        paragraph_output = "The output tab allows the user to view a movie of the evolution of their wave in time."
        # TODO: "edit these equations to be 1D"
        image_equations = ImageTk.PhotoImage(
            Image.open("swe_math_1D.png").resize((400, 200), Image.LANCZOS)
        )
        image_schematic = ImageTk.PhotoImage(
            Image.open("system_schematic.png").resize((400, 200), Image.LANCZOS)
        )

        header_title = tk.Label(grouped_frame, font=("Sans Serif", 40), text=title_text)
        tab_description_title = tk.Label(
            grouped_frame, font=("Sans Serif", 30), text=tab_description_title_text
        )
        input_title = tk.Label(grouped_frame, font=("Sans Serif", 24), text="Input Tab")
        numerical_simulation_title = tk.Label(
            grouped_frame, font=("Sans Serif", 24), text="Numerical Simulation Tab"
        )
        output_title = tk.Label(
            grouped_frame, font=("Sans Serif", 24), text="Output Tab"
        )

        body_1 = tk.Label(
            grouped_frame,
            font=("Sans Serif", 15),
            text=paragraph_1,
            wraplength=1400,
            justify="left",
        )
        body_2 = tk.Label(
            grouped_frame,
            font=("Sans Serif", 15),
            text=paragraph_2,
            wraplength=1400,
            justify="left",
        )
        body_3 = tk.Label(
            grouped_frame,
            font=("Sans Serif", 15),
            text=paragraph_3,
            wraplength=1400,
            justify="left",
        )
        body_input = tk.Label(
            grouped_frame,
            font=("Sans Serif", 15),
            text=paragraph_input,
            wraplength=1400,
            justify="left",
        )
        body_numerical_simulation = tk.Label(
            grouped_frame,
            font=("Sans Serif", 15),
            text=paragraph_numerical_simulation,
            wraplength=1400,
            justify="left",
        )
        body_output = tk.Label(
            grouped_frame,
            font=("Sans Serif", 15),
            text=paragraph_output,
            wraplength=1400,
            justify="left",
        )

        label_equations = tk.Label(grouped_frame)
        label_equations.image = image_equations
        label_equations.configure(image=image_equations)
        caption_equations = tk.Label(
            grouped_frame,
            text="1D shallow water wave equations",
            font=("Sans Serif", 10),
        )

        label_schematic = tk.Label(grouped_frame)
        label_schematic.image = image_schematic
        label_schematic.configure(image=image_schematic)
        caption_schematic = tk.Label(
            grouped_frame,
            text="Schematic of 1D shallow water wave system (via Wikipedia user Maistral01 under (CC BY-SA 4.0)",
            font=("Sans Serif", 10),
        )

        header_title.grid(row=0, column=0, columnspan=2)
        body_1.grid(row=1, column=0, columnspan=2)
        body_2.grid(row=2, column=0, columnspan=2)
        label_equations.grid(row=3, column=0)
        label_schematic.grid(row=3, column=1)
        caption_equations.grid(row=4, column=0)
        caption_schematic.grid(row=4, column=1)
        tab_description_title.grid(row=5, column=0, columnspan=2)
        body_3.grid(row=6, column=0, columnspan=2)
        input_title.grid(row=7, column=0, sticky="W")
        body_input.grid(row=8, column=0, columnspan=2)
        numerical_simulation_title.grid(row=9, column=0, sticky="W")
        body_numerical_simulation.grid(row=10, column=0, columnspan=2)
        output_title.grid(row=11, column=0, sticky="W")
        body_output.grid(row=12, column=0, columnspan=2)

        grouped_frame.grid(row=0, column=0, sticky="EWNS")
        grouped_frame.grid_columnconfigure(0, weight=1)

        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

    def input_tab_construction(self, tab):
        """
        Builds the input tab and its associated widgets

        tab:
            the input tab which points this function to the frame where it should build these widgets

        input_options_frame:
            more aesthetic packing of the widgets within the tab if they are nested in a frame within the tab. This only
            groups the different sliders/textboxes used in the user inputs; the plot window is separate

        input_shape_menu:
            a tk.OptionMenu() instance which builds a drop-down menu for the user to select the desired type of input curve

        self.x_limit_entry, self.nx_entry, self.t_limit_entry, and self.FPS_entry:
            tk.Entry() instances to allow for user entering of the domain length, number of discretizations in space,
            the length of simulation time, and output video FPS desired, respectively

        self.frequency_slider, self.amplitude_slider, and self.gaussian_shift_slider:
            tk.Scale() instances to create sliders for the user to adjust the frequency and phase of the sinusoids input,
            the amplitude of either curve, and the center of the Gaussian hump. The scales automatically update the plotting
            window when interacted with

        self.plot_window:
            a matplotlib Figure() instance that is converted to a Tkinter object using the FigureCanvasTkAgg library

        update_plot_button:
            a button which upon user interaction updates the plotting window; required when the domain/discretization/curve type is changed
        """
        ### Widgets for this tab
        # Group the inputs in their own frame
        input_options_frame = tk.Frame(tab)

        # Input curve shape dropdown menu
        input_curve_options = (
            "Sinusoid",
            "Gaussian",
        )
        self.selected_input_shape = tk.StringVar()
        self.selected_input_shape.set("Gaussian")
        input_shape_menu = tk.OptionMenu(
            input_options_frame, self.selected_input_shape, *input_curve_options
        )
        label_input_shape_menu = tk.Label(
            input_options_frame, text="Select the shape for the input wave:"
        )

        # Numerical text boxes for generic numerical parameters
        self.x_limit = tk.IntVar()
        self.nx = tk.IntVar()
        self.t_limit = tk.IntVar()
        self.FPS = tk.IntVar()
        self.totduration = tk.IntVar()

        self.x_limit.set(20)
        self.nx.set(100)
        self.t_limit.set(10)
        self.FPS.set(30)

        self.x_limit_entry = tk.Entry(input_options_frame, textvariable=self.x_limit)
        label_x_limit = tk.Label(input_options_frame, text="Domain Width (x) [m]")

        self.nx_entry = tk.Entry(input_options_frame, textvariable=self.nx)
        label_nx = tk.Label(input_options_frame, text="Number of Points in X")

        self.t_limit_entry = tk.Entry(input_options_frame, textvariable=self.t_limit)
        label_t_limit = tk.Label(
            input_options_frame, text="Length of Simulation (t) [s]"
        )

        self.FPS_entry = tk.Entry(input_options_frame, textvariable=self.FPS)
        label_FPS = tk.Label(input_options_frame, text="Frames per second")

        # Sliders for various curve parameters
        self.frequency_slider = tk.Scale(
            input_options_frame,
            label="Frequency",
            from_=1,
            to=9,
            digits=2,
            resolution=1,
            command=self.update_plot,
            orient=tk.HORIZONTAL,
            length=300,
        )
        self.frequency_slider.set(3)

        self.amplitude_slider = tk.Scale(
            input_options_frame,
            label="Amplitude",
            from_=-0.5,
            to=0.5,
            digits=2,
            resolution=0.1,
            command=self.update_plot,
            orient=tk.HORIZONTAL,
            length=300,
        )
        self.amplitude_slider.set(1)

        self.gaussian_shift_slider = tk.Scale(
            input_options_frame,
            label="Center of Gaussian",
            from_=-self.x_limit.get() / 2,
            to=self.x_limit.get() / 2,
            digits=3,
            resolution=0.1,
            command=self.update_plot,
            orient=tk.HORIZONTAL,
            length=300,
        )
        self.gaussian_shift_slider.set(5)

        # Button to update the plot for inputs
        update_plot_button = tk.Button(
            input_options_frame, text="Update Plot", command=self.pack_input_tab_plot
        )

        # Plot figure
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        x = np.linspace(-self.x_limit.get() / 2, self.x_limit.get() / 2, 100)
        (self.curve,) = self.ax.plot(x, x)
        self.curve.set_ydata(
            [(1 + np.sin(2 * np.pi * element / self.x_limit.get())) for element in x]
        )
        (self.baseline,) = self.ax.plot(
            [-self.x_limit.get() / 2, self.x_limit.get() / 2], [1, 1], "r:"
        )
        self.ax.set_xlim([-self.x_limit.get() / 2, self.x_limit.get() / 2])
        self.ax.set_ylim([-5, 5])
        self.ax.set_xlabel("Simulation Domain (x) [m]")
        self.ax.set_ylabel("Water Height (h) [m]")
        self.plot_window = FigureCanvasTkAgg(self.fig, master=tab)

        # Console logging
        self.input_console_logger = ScrolledText(
            input_options_frame, height=5, width=80, font=("Consolas", 12, "normal")
        )
        logging = PrintLogger(self.input_console_logger)
        sys.stdout = logging
        sys.stderr = logging

        # Button to clear the console
        clear_console_button = tk.Button(
            input_options_frame,
            text="Clear Console",
            # )
            command=self.clear_console_input,
        )

        # Packing, only packs the initial widgets used for the sinusoidal input (default)
        self.x_limit_entry.grid(row=0, column=1, padx=5)
        label_x_limit.grid(row=0, column=0)
        self.nx_entry.grid(row=1, column=1, padx=5)
        label_nx.grid(row=1, column=0)
        self.t_limit_entry.grid(row=2, column=1, padx=5)
        label_t_limit.grid(row=2, column=0)
        self.FPS_entry.grid(row=4, column=1, padx=5)
        label_FPS.grid(row=4, column=0)

        label_input_shape_menu.grid(row=6, column=0)
        input_shape_menu.grid(row=6, column=1, padx=10)
        self.gaussian_shift_slider.grid(row=7, column=0, padx=10, columnspan=2)
        self.amplitude_slider.grid(row=8, column=0, padx=10, columnspan=2)
        self.plot_window.get_tk_widget().grid(
            row=0, column=1, rowspan=15, sticky="ENWS"
        )
        update_plot_button.grid(row=14, column=0, columnspan=1)
        clear_console_button.grid(row=14, column=1)
        self.input_console_logger.grid(row=15, column=0, columnspan=2, rowspan=10)

        input_options_frame.grid(row=0, column=0, rowspan=15, sticky="NS")
        tab.grid_columnconfigure(1, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        # tab.grid_columnconfigure(0, weight=1)

    def numerical_simulation_tab_construction(self, tab):
        """
        Builds the numerical simulation tab and its associated widgets

        run_default_simulation_button:
            tk.Button() instance which calls the run_default_simulation() method

        run_custom_simulation_button:
            tk.Button() instance which calls the run_custom_simulation() method

        time_integration_menu and spatial_discretization_menu:
            drop-down menus for the user to select the desired methods for time integration and spatial discretization, respectively
        """
        # Widgets for this tab
        run_default_simulation_button = tk.Button(
            tab, text="Run default simulation", command=self.run_default_simulation
        )
        run_custom_simulation_buttom = tk.Button(
            tab, text="Run custom simulation", command=self.run_custom_simulation
        )

        # Numerical Schemes
        # Time integration
        time_integration_options = (
            "Euler Forward",
            "2nd-order Runge-Kutta",
            "3rd-order Runge-Kutta",
            "4th-order Runge-Kutta",
        )
        spatial_discretization_options = (
            "2nd-order Central Difference",
            "1st-order upwind method (flux splitting)",
            "5th-order WENO method (flux splitting)",
        )
        self.selected_time_integration = tk.StringVar()
        self.selected_time_integration.set("Euler Forward")
        self.selected_spatial_discretization = tk.StringVar()
        self.selected_spatial_discretization.set("2nd-order Central Difference")

        time_integration_menu = tk.OptionMenu(
            tab, self.selected_time_integration, *time_integration_options
        )
        label_integration_menu = tk.Label(
            tab, text="Select the method for time integration:"
        )

        spatial_discretization_menu = tk.OptionMenu(
            tab, self.selected_spatial_discretization, *spatial_discretization_options
        )
        label_discretization_menu = tk.Label(
            tab, text="Select the method for spatial discretization:"
        )

        # Console logging
        self.numerical_console_logger = ScrolledText(
            tab, height=20, width=50, font=("Consolas", 12, "normal")
        )
        logging = PrintLogger(self.numerical_console_logger)
        sys.stdout = logging
        sys.stderr = logging

        # Button to clear the console
        clear_console_button = tk.Button(
            tab,
            text="Clear Console",
            # )
            command=self.clear_console_numerical,
        )

        # Packing widgets
        run_default_simulation_button.grid(row=0, column=0, columnspan=2)
        run_custom_simulation_buttom.grid(row=1, column=0, columnspan=2)

        label_integration_menu.grid(row=2, column=0, columnspan=2)
        time_integration_menu.grid(row=3, column=0, columnspan=2)
        label_discretization_menu.grid(row=4, column=0, columnspan=2)
        spatial_discretization_menu.grid(row=5, column=0, columnspan=2)

        clear_console_button.grid(row=6, column=0, columnspan=2)
        self.numerical_console_logger.grid(row=7, column=0, columnspan=2)

    def output_tab_construction(self, tab):
        """
        This method constructs the output tab. The tab is mainly a video player.
        The main package of this method is TkinterVideo (along with tkinter)

        See https://pypi.org/project/tkvideoplayer/

        FPS:
            Frames per second of the movie

        label:
            tk.Label which contains information about the FPS (can be changed to add
            in more information)

        self.pp_btn:
            The button responsible for play and pause.

        self.videoplayer:
            Plays the video of the generated video using TkinterVideo

        self.currenttime:
            Keeps track of the current time of the movie being played

        self.slope_slider:
            Interactive slider which has two main features:
                1. As a progress bar
                2. Can change the time of the video to the dragged point

            The resolution is set to 1 since Tkvideoplayer only has an event which
            updates every second

        timefromstartlabel:
            The current time of the movie being played
            (appears to the left of progress bar)

        totdurationlabel:
            The total duration of the movie being played
            (appears to the right of progress bar)

        self.videoplayer.bind:
            Every second, the slider is updated

        The final section is just design

        """
        # bar with some text (maybe put in values of physical variables etc)
        FPS = self.FPS.get()
        label = tk.Label(tab, text=f"Output(FPS = {FPS}):", fg="white", bg="black")
        self.pp_btn = tk.Button(tab, text="play", command=self.play_pause, width=5)

        # video player
        self.videoplayer = TkinterVideo(master=tab, scaled=True)
        self.videoplayer.load(r"src/sample_movies/sample_generated.mp4")
        self.videoplayer.pause()

        # variable to store the current time of the video
        self.currenttime = tk.IntVar(tab)

        # slider
        self.slope_slider = tk.Scale(
            tab,
            variable=self.currenttime,
            from_=0,
            to=self.t_limit.get(),
            digits=1,
            resolution=1,
            orient=tk.HORIZONTAL,
            command=self.settime_slider,
            tickinterval=math.floor(self.t_limit.get() / 4),
            showvalue=0,
        )

        timefromstartlabel = tk.Label(tab, textvariable=self.currenttime)
        totdurationlabel = tk.Label(tab, text=str(self.t_limit.get()))

        self.videoplayer.bind("<<SecondChanged>>", self.update_slider)

        # Packing widgets
        tab.rowconfigure(2, minsize=100, weight=1)
        tab.columnconfigure([0, 1, 2], minsize=200, weight=1)
        label.grid(row=1, column=0, columnspan=3, sticky="ew")
        self.videoplayer.grid(row=2, column=0, rowspan=3, columnspan=3, sticky="nsew")
        timefromstartlabel.grid(row=17, column=0, padx=10, pady=10)
        self.slope_slider.grid(row=17, column=1, padx=10, pady=10)
        totdurationlabel.grid(row=17, column=2, padx=10, pady=10)
        self.pp_btn.grid(row=18, column=1)

    # updates current time, used to update slider
    def update_slider(self, event):
        """
        Method to update the slider. This will be called in the output_tab_construction
        method when we want to update the slider. Linked to events so
        that updates happen automatically.

        The duration is rounded for visual asthetics purposes.
        """
        self.currenttime.set(round(self.videoplayer.current_duration()))

    # change video player to the point at which the user specifies
    def settime_slider(self, event):
        """
        Get the current value of the slope_slider

        self.slope_slider.get():
            This command gets the value that the user has specified
            the time to

        self.videoplayer.seek():
            Skips the movie to the given time
        """
        a = self.slope_slider.get()
        self.videoplayer.seek(int(a))

    # play and pause the video
    def play_pause(self):
        """
        Sets up the play pause button. Very much follows documentation.

        If the video is paused, then the command will play the video and
        vice versa.

        See https://github.com/PaulleDemon/tkVideoPlayer/blob/master/examples/sample_player.py

        """
        if self.videoplayer.is_paused():
            self.videoplayer.play()
            self.pp_btn["text"] = "pause"

        else:
            self.videoplayer.pause()
            self.pp_btn["text"] = "play"

    def pack_input_tab_plot(self):
        """
        Redraws the plot figure in the input_tab_plot (used when domain/curve type changes)

        Gathers data from the input curve (self.curve) and "rebuilds" it using the values from the various user inputs

        The first if- statement performs a check to see if the array of x_points needs to be rebuilt.
        The second if- statement rebuilds the curve in a sinusoid if the drop-down menu is set to "Sinusoid."
        The elif- statement rebuilds the curve as a Gaussian curve if the drop-down menu is set to "Gaussian."

        The method closes by redrawing the dotted-red "baseline" (equilibrium water level) and redrawing the input curve
        """
        # Shared initialization
        curve_type = self.selected_input_shape.get()
        (x, y) = self.curve.get_data()

        # Error Catching
        try:
            self.x_limit.get()
        except:
            raise Exception(
                "Please input a floating point number for the 'Domain Width' field"
            )

        try:
            self.nx.get()
        except:
            raise Exception(
                "Please input a floating point number for the 'Number of Points in X' field"
            )

        try:
            self.t_limit.get()
        except:
            raise Exception(
                "Please input a floating point number for the 'Simulation Length' field"
            )

        try:
            self.FPS.get()
        except:
            raise Exception("Please input a floating point number for 'FPS' field")

        if len(x) != self.nx.get() or max(x) != self.x_limit.get() / 2:
            x = np.linspace(
                -self.x_limit.get() / 2, self.x_limit.get() / 2, np.round(self.nx.get())
            )
            self.curve.set_xdata(x)
            self.ax.set_xlim((-self.x_limit.get() / 2, self.x_limit.get() / 2))

        if curve_type == "Sinusoid":
            self.gaussian_shift_slider.grid_forget()
            self.frequency_slider.grid(row=7, column=0, padx=10, columnspan=2)

            amplitude = self.amplitude_slider.get()
            frequency = self.frequency_slider.get()
            self.curve.set_ydata(
                [
                    (
                        amplitude
                        * np.sin(frequency * 2 * np.pi * element / self.x_limit.get())
                    )
                    + 1
                    for element in x
                ]
            )

        elif curve_type == "Gaussian":
            self.frequency_slider.grid_forget()
            self.gaussian_shift_slider.grid(row=7, column=0, columnspan=2, padx=20)

            shift = self.gaussian_shift_slider.get()
            amplitude = self.amplitude_slider.get()
            self.curve.set_ydata(
                [amplitude * np.exp(-1.0 * (element - shift) ** 2) + 1 for element in x]
            )

        self.baseline.set_xdata([-self.x_limit.get() / 2, self.x_limit.get() / 2])
        self.plot_window.draw()

    # These are separate functions due to the inability to pass the tk.ScrolledText() objects as function parameters and achieve stable behavior here
    def clear_console_input(self):
        self.input_console_logger.configure(state="normal")
        self.input_console_logger.delete(1.0, tk.END)
        self.input_console_logger.configure(state="disabled")

    def clear_console_numerical(self):
        self.numerical_console_logger.configure(state="normal")
        self.numerical_console_logger.delete(1.0, tk.END)
        self.numerical_console_logger.configure(state="disabled")

    def update_plot(self, event):
        """
        Redraws the plot figure in the input_tab_plot (used when the sliders are adjusted)

        The if- statement rebuilds the curve in a sinusoid if the drop-down menu is set to "Sinusoid."
        The elif- statement rebuilds the curve as a Gaussian curve if the drop-down menu is set to "Gaussian."
        """
        x, y = self.curve.get_data()
        curve_type = self.selected_input_shape.get()

        if curve_type == "Sinusoid":
            x, y = self.curve.get_data()
            amplitude = self.amplitude_slider.get()
            frequency = self.frequency_slider.get()
            self.curve.set_ydata(
                [
                    (
                        1
                        + amplitude
                        * np.sin(2 * np.pi * i * frequency / self.x_limit.get())
                    )
                    for i in x
                ]
            )
            self.plot_window.draw()

        elif curve_type == "Gaussian":
            x, y = self.curve.get_data()
            amplitude = self.amplitude_slider.get()
            shift = self.gaussian_shift_slider.get()
            self.curve.set_ydata(
                [amplitude * np.exp(-1.0 * (element - shift) ** 2) + 1 for element in x]
            )

            self.plot_window.draw()

    def run_custom_simulation(self):
        """
        executes the SWE_1D() method from SWE_1D.py, and makemovie() class, using the user-defined inputs

        x:
            the array of points in x for the simulation domain

        h_i:
            the height of the water at a point in x

        hu_i:
            the velocity of the weight at a point in x

        dx:
            the spatial discretization step

        FPS:
            the number of frames to output per second

        time_integration_schemes and spatial discretization_schemes:
            dictionaries that connect the user-selected numerical schemes to the methods within SWE_1D.py
        """
        # Execute 1D shallow water wave equations
        x, h_i = self.curve.get_data()
        nx = self.nx.get()
        time_length = self.t_limit.get()
        self.totduration = time_length

        hu_i = np.zeros(np.shape(x))
        h_i = np.array(h_i)
        x = np.array(x)

        dx = self.x_limit.get() / nx
        FPS = self.FPS.get()

        time_integration_schemes = {
            "Euler Forward": eulerForward,
            "2nd-order Runge-Kutta": RK2,
            "3rd-order Runge-Kutta": RK3,
            "4th-order Runge-Kutta": RK4,
        }
        spatial_discretization_schemes = {
            "2nd-order Central Difference": centralDiff_Order2,
            "1st-order upwind method (flux splitting)": upwindDiff_Order1,
            "5th-order WENO method (flux splitting)": weno5,
        }

        fig = SWE_1D(
            dx,
            x,
            time_length,
            nx,
            FPS,
            time_integration_schemes[self.selected_time_integration.get()],
            spatial_discretization_schemes[self.selected_spatial_discretization.get()],
            1,
            h=h_i,
            hu=hu_i,
        )

        # make a movie
        moviemake = makemovie(
            Path("output.out"), nx, self.x_limit.get(), self.FPS.get()
        )
        moviemake.saveanimation()

        temp_window = FigureCanvasTkAgg(fig, master=self.numerical_simulation_tab)
        temp_window.get_tk_widget().grid(row=0, column=2, rowspan=15)
        close("all")

    def run_default_simulation(self):
        """
        executes the SWE_1D() method from SWE_1D.py, and makemovie() class, using pre-determined inputs (same as test-cases)

        domainLength:
            length of the domain in x

        xTotalNumber:
            the number of the discretizations in x

        timeLength:
            the length of time to simulate

        FPS:
            the number of frames per second to output

        dx:
            the spatial discretization step

        xArray:
            the spatial discretization

        h_i:
            the height of the water at a point in x

        hu_i:
            the velocity of the weight at a point in x
        """
        domainLength: float = 20.0  # meter
        xTotalNumber: int = 100
        timeLength: float = 10.0  # second
        FPS: int = 30

        dx: float = domainLength / xTotalNumber
        xArray = np.linspace(-domainLength / 2, domainLength / 2 - dx, xTotalNumber)
        h_i, hu_i = inputInitialValue(xArray, xTotalNumber, 1)

        fig = SWE_1D(
            dx,
            xArray,
            timeLength,
            xTotalNumber,
            FPS,
            eulerForward,
            centralDiff_Order2,
            1,
            h=h_i,
            hu=hu_i,
        )

        # make a movie
        moviemake = makemovie(r"output.out", xTotalNumber, domainLength / 2, FPS)
        moviemake.saveanimation()

        temp_window = FigureCanvasTkAgg(fig, master=self.numerical_simulation_tab)
        temp_window.get_tk_widget().grid(row=0, column=2, rowspan=15)
        close("all")


def initialize_window():
    """
    Initializes the simulation window with a title
    """
    window = tk.Tk()
    window.title("Shallow Water Wave Equations - Numerical Simulation")

    return window


def main():
    """
    creates an applet instance, builds the app according to the InteractiveUserInterface, and then enters the gui mainloop
    """
    root = initialize_window()
    app = InteractiveUserInterface(root)
    app.root.mainloop()


if __name__ == "__main__":
    main()
