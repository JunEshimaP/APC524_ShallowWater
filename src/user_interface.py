import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.pylab import close
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from SWE_1D import SWE_1D, inputInitialValue
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import math
from tkVideoPlayer import *


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

    def __init__(self, filename, N: int, xlim: float, FPS: int):
        self.filename = filename
        self.N = N
        # set up matplotlib as in matplotlib.animation documentation
        self.plottedgraphfig, self.plottedgraphfigax = plt.subplots()
        (self.curve,) = self.plottedgraphfigax.plot([], [])
        self.xlim = xlim
        self.FPS = FPS

    # read out values from .txt file
    def readvalues(self):
        self.h, self.x, self.t = np.loadtxt(
            self.filename, delimiter=" ", usecols=(0, 1, 2), unpack=True
        )
        self.numberofvalues = self.h.size
        self.numberoftimesteps = int(self.numberofvalues / self.N)

    #   initialise the plot
    def initplot(self):
        # set axis
        self.plottedgraphfigax.set_xlim(0, self.xlim)
        self.plottedgraphfigax.set_ylim(0, 2)
        return (self.curve,)

    # update the plot every frame
    def update(self, frame):
        x_val = []
        y_val = []
        for i in range(self.N):
            x_val.append(self.x[i + frame * self.N])
            y_val.append(self.h[i + frame * self.N])
        self.curve.set_data(x_val, y_val)
        return (self.curve,)

    # create animation
    def createanimation(self):
        self.readvalues()

        self.ani = animation.FuncAnimation(
            self.plottedgraphfig,
            self.update,
            frames=range(self.numberoftimesteps),
            init_func=self.initplot,
            blit=True,
        )

    # save the animaton
    def saveanimation(self):
        self.createanimation()

        # set up the writer
        # note: need to have ffmpeg installed.
        writervideo = animation.FFMpegWriter(fps=self.FPS)
        self.ani.save(r"src/sample_movies/sample_generated.mp4", writer=writervideo)
        print("Movie Made")


class InteractiveUserInterface:
    def __init__(self, master):
        self.root = master
        # Menu bar
        menu_bar = tk.Menu(master)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=master.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)

        self.moviefilename = r"src/sample_movies/sample_generated.mp4"

        master.config(menu=menu_bar)
        # Create the tabs for the plotting
        tab_control = ttk.Notebook(master)
        input_tab = ttk.Frame(tab_control)
        self.numerical_simulation_tab = ttk.Frame(tab_control)
        output_tab = ttk.Frame(tab_control)

        tab_control.add(input_tab, text="Input")
        tab_control.add(self.numerical_simulation_tab, text="Numerical Simulation")
        tab_control.add(output_tab, text="Output")

        self.input_tab_construction(input_tab)
        self.numerical_simulation_tab_construction(self.numerical_simulation_tab)
        self.output_tab_construction(output_tab)
        tab_control.pack(expand=1, fill="both")

    def input_tab_construction(self, tab):
        ### Widgets for this tab
        # Input curve shape dropdown menu
        input_curve_options = (
            "Sinusoid",
            "Gaussian",
        )
        self.selected_input_shape = tk.StringVar()
        self.selected_input_shape.set("Sinusoid")
        input_shape_menu = tk.OptionMenu(
            tab, self.selected_input_shape, *input_curve_options
        )
        label_input_shape_menu = tk.Label(
            tab, text="Select the shape for the input wave:"
        )

        # Numerical text boxes for generic numerical parameters
        self.x_limit = tk.IntVar()
        self.nx = tk.IntVar()
        self.t_limit = tk.IntVar()
        self.nt = tk.IntVar()
        self.FPS = tk.IntVar()
        self.totduration = tk.IntVar()

        self.x_limit.set(10)
        self.nx.set(100)
        self.t_limit.set(10)
        self.nt.set(100)
        self.FPS.set(30)

        self.x_limit_entry = tk.Entry(tab, textvariable=self.x_limit)
        label_x_limit = tk.Label(tab, text="X Limit")

        self.nx_entry = tk.Entry(tab, textvariable=self.nx)
        label_nx = tk.Label(tab, text="Number of Points in X")

        self.t_limit_entry = tk.Entry(tab, textvariable=self.t_limit)
        label_t_limit = tk.Label(tab, text="T Limit")

        self.nt_entry = tk.Entry(tab, textvariable=self.nt)
        label_nt = tk.Label(tab, text="Number of Points in T")

        self.FPS_entry = tk.Entry(tab, textvariable=self.FPS)
        label_FPS = tk.Label(tab, text="Frames per second")

        # Sliders for various curve parameters
        self.frequency_slider = tk.Scale(
            tab,
            label="Frequency",
            from_=0,
            to=9,
            digits=2,
            resolution=0.1,
            command=self.update_plot,
            orient=tk.HORIZONTAL,
            length=300,
        )
        self.frequency_slider.set(1)

        self.amplitude_slider = tk.Scale(
            tab,
            label="Amplitude",
            from_=-5,
            to=5,
            digits=2,
            resolution=0.1,
            command=self.update_plot,
            orient=tk.HORIZONTAL,
            length=300,
        )
        self.amplitude_slider.set(1)

        self.phase_slider = tk.Scale(
            tab,
            label="Phase",
            from_=0,
            to=2 * np.pi,
            digits=3,
            resolution=0.05,
            command=self.update_plot,
            orient=tk.HORIZONTAL,
            length=300,
        )
        self.phase_slider.set(0)

        self.gaussian_shift_slider = tk.Scale(
            tab,
            label="Center of Gaussian",
            from_=0,
            to=self.x_limit.get(),
            digits=3,
            resolution=0.1,
            command=self.update_plot,
            orient=tk.HORIZONTAL,
            length=300,
        )
        self.gaussian_shift_slider.set(5)

        # Button to update the plot for inputs
        update_plot_button = tk.Button(
            tab, text="Update Plot", command=self.pack_input_tab_plot
        )

        # Plot figure
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        i = np.linspace(0, 10, 100)
        (self.curve,) = self.ax.plot(i, [np.sin(x) for x in i])
        (self.baseline,) = self.ax.plot([0, self.x_limit.get()], [0, 0], "r:")
        self.ax.set_xlim([0, 10])
        self.ax.set_ylim([-5, 5])
        self.ax.set_xlabel("Simulation Domain (x) [m]")
        self.ax.set_ylabel("Water Height (h) [m]")
        self.plot_window = FigureCanvasTkAgg(self.fig, master=tab)

        # Packing, only packs the initial widgets used for the sinusoidal input (default)
        self.x_limit_entry.grid(row=0, column=1, padx=5)
        label_x_limit.grid(row=0, column=0)
        self.nx_entry.grid(row=1, column=1, padx=5)
        label_nx.grid(row=1, column=0)
        self.t_limit_entry.grid(row=2, column=1, padx=5)
        label_t_limit.grid(row=2, column=0)
        self.nt_entry.grid(row=3, column=1, padx=5)
        label_nt.grid(row=3, column=0)
        self.FPS_entry.grid(row=4, column=1, padx=5)
        label_FPS.grid(row=4, column=0)

        label_input_shape_menu.grid(row=6, column=0)
        input_shape_menu.grid(row=6, column=1, padx=10)
        self.frequency_slider.grid(row=7, column=0, padx=10, columnspan=2)
        self.amplitude_slider.grid(row=8, column=0, padx=10, columnspan=2)
        self.phase_slider.grid(row=9, column=0, padx=10, columnspan=2)
        self.plot_window.get_tk_widget().grid(row=0, column=2, rowspan=15)
        update_plot_button.grid(row=15, column=0, columnspan=2)

    def numerical_simulation_tab_construction(self, tab):
        # Widgets for this tab
        run_default_simulation_button = tk.Button(
            tab, text="Run default simulation", command=self.run_default_simulation
        )
        run_custom_simulation_buttom = tk.Button(
            tab, text="Run custom simulation", command=self.run_custom_simulation
        )

        # Packing widgets
        run_default_simulation_button.grid(row=0, column=0, columnspan=2)
        run_custom_simulation_buttom.grid(row=1, column=0, columnspan=2)

    def output_tab_construction(self, tab):

        # bar with some text (maybe put in values of physical variables etc)
        FPS = self.FPS.get()
        label = tk.Label(tab, text=f"Output(FPS = {FPS}):", fg="white", bg="black")
        self.pp_btn = tk.Button(tab, text="play", command=self.play_pause, width=5)

        # video player
        self.videoplayer = TkinterVideo(master=tab, scaled=True)
        self.videoplayer.load(self.moviefilename)
        self.videoplayer.pause()

        # variable to store the current time of the video
        self.currenttime = tk.DoubleVar(tab)

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
        tab.rowconfigure([0, 1, 2, 3, 4, 5], minsize=100)
        tab.columnconfigure([0, 1, 2], minsize=200)
        label.grid(row=1, column=0, columnspan=3, sticky="ew")
        self.videoplayer.grid(row=2, column=0, rowspan=3, columnspan=3, sticky="nsew")
        timefromstartlabel.grid(row=5, column=0, padx=10, pady=10)
        self.slope_slider.grid(row=5, column=1, padx=10, pady=10)
        totdurationlabel.grid(row=5, column=2, padx=10, pady=10)
        self.pp_btn.grid(row=6, column=1)

    # updates current time, used to update slider
    def update_slider(self, event):
        # the second is a bit glichy, so have the display in integer seconds
        self.currenttime.set(round(self.videoplayer.current_duration()))

    # change video player to the point at which the user specifies
    def settime_slider(self, event):
        a = self.slope_slider.get()
        self.videoplayer.seek(int(a))

    # play and pause the video
    def play_pause(self):
        if self.videoplayer.is_paused():
            self.videoplayer.play()
            self.pp_btn["text"] = "pause"

        else:
            self.videoplayer.pause()
            self.pp_btn["text"] = "play"

    def pack_input_tab_plot(self):
        # Shared initialization
        curve_type = self.selected_input_shape.get()
        (x, y) = self.curve.get_data()

        # self.nx.set(self.nx.get())
        # self.x_limit.set(self.x_limit.get())
        # self.nt.set(self.nt.get())
        # self.t_limit.set(self.t_limit.get())

        if len(x) != self.nx.get() or max(x) != self.x_limit.get():
            x = np.linspace(0, self.x_limit.get(), self.nx.get())
            self.curve.set_xdata(x)
            self.ax.set_xlim((0, self.x_limit.get()))

        if curve_type == "Sinusoid":
            self.gaussian_shift_slider.grid_forget()
            self.frequency_slider.grid(row=7, column=0, padx=10, columnspan=2)
            self.phase_slider.grid(row=9, column=0, padx=10, columnspan=2)

            amplitude = self.amplitude_slider.get()
            frequency = self.frequency_slider.get()
            phase = self.phase_slider.get()
            self.curve.set_ydata(
                [(amplitude * np.sin(frequency * element - phase)) for element in x]
            )

        elif curve_type == "Gaussian":
            self.frequency_slider.grid_forget()
            self.phase_slider.grid_forget()
            self.gaussian_shift_slider.grid(row=7, column=0, columnspan=2, padx=20)

            shift = self.gaussian_shift_slider.get()
            amplitude = self.amplitude_slider.get()
            self.curve.set_ydata(
                [amplitude * np.exp(-1.0 * (element - shift) ** 2) for element in x]
            )

        self.baseline.set_xdata([0, self.x_limit.get()])
        self.plot_window.draw()

    def update_plot(self, event):
        x, y = self.curve.get_data()
        curve_type = self.selected_input_shape.get()

        if curve_type == "Sinusoid":
            x, y = self.curve.get_data()
            amplitude = self.amplitude_slider.get()
            frequency = self.frequency_slider.get()
            phase = self.phase_slider.get()
            self.curve.set_ydata(
                [(amplitude * np.sin(frequency * i - phase)) for i in x]
            )
            self.plot_window.draw()

        elif curve_type == "Gaussian":
            x, y = self.curve.get_data()
            amplitude = self.amplitude_slider.get()
            shift = self.gaussian_shift_slider.get()
            self.curve.set_ydata(
                [amplitude * np.exp(-1.0 * (element - shift) ** 2) for element in x]
            )

            self.plot_window.draw()

    def run_custom_simulation(self):
        # Execute 1D shallow water wave equations
        x, h_i = self.curve.get_data()
        nx = self.nx.get()
        time_length = self.t_limit.get()
        self.totduration = time_length

        hu_i = np.zeros(np.shape(x))
        h_i = np.array(h_i) + 1
        x = np.array(x)

        dx = self.x_limit.get() / nx
        FPS = self.FPS.get()
        fig = SWE_1D(dx, x, time_length, nx, FPS, h=h_i, hu=hu_i)

        # make a movie
        moviemake = makemovie(r"output.out", nx, self.x_limit.get(), self.FPS.get())
        moviemake.saveanimation()

        temp_window = FigureCanvasTkAgg(fig, master=self.numerical_simulation_tab)
        temp_window.get_tk_widget().grid(row=0, column=2, rowspan=15)
        close("all")

    def run_default_simulation(self):

        domainLength: float = 20.0  # meter
        xTotalNumber: int = 100
        timeLength: float = 10.0  # second
        FPS: int = 30

        dx: float = domainLength / xTotalNumber
        xArray = np.linspace(-domainLength / 2, domainLength / 2 - dx, xTotalNumber)
        h_i, hu_i = inputInitialValue(xArray, xTotalNumber)

        fig = SWE_1D(dx, xArray, timeLength, xTotalNumber, FPS, h=h_i, hu=hu_i)

        # make a movie
        moviemake = makemovie(r"output.out", xTotalNumber, domainLength / 2, FPS)
        moviemake.saveanimation()

        temp_window = FigureCanvasTkAgg(fig, master=self.numerical_simulation_tab)
        temp_window.get_tk_widget().grid(row=0, column=2, rowspan=15)
        close("all")


def initialize_window():
    # Initializes a window with a title/window size/a button
    window = tk.Tk()
    window.title("Shallow Water Wave Equations - Numerical Simulation")

    return window


def main():
    root = initialize_window()
    app = InteractiveUserInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()
