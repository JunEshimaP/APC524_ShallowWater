import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.pylab import close
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from SWE_1D import SWE_1D, inputInitialValue


class InteractiveUserInterface:
    def __init__(self, master):
        self.root = master
        # Menu bar
        menu_bar = tk.Menu(master)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command = master.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)

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
        input_curve_options = ("Sinusoid", "Gaussian",)
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

        self.x_limit.set(10)
        self.nx.set(100)
        self.t_limit.set(10)
        self.nt.set(100)

        self.x_limit_entry = tk.Entry(tab, textvariable=self.x_limit)
        label_x_limit = tk.Label(tab, text="X Limit")

        self.nx_entry = tk.Entry(tab, textvariable=self.nx)
        label_nx = tk.Label(tab, text="Number of Points in X")

        self.t_limit_entry = tk.Entry(tab, textvariable=self.t_limit)
        label_t_limit = tk.Label(tab, text="T Limit")

        self.nt_entry = tk.Entry(tab, textvariable=self.nt)
        label_nt = tk.Label(tab, text="Number of Points in T")

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

        label_input_shape_menu.grid(row=5, column=0)
        input_shape_menu.grid(row=5, column=1, padx=10)
        self.frequency_slider.grid(row=6, column=0, padx=10, columnspan=2)
        self.amplitude_slider.grid(row=7, column=0, padx=10, columnspan=2)
        self.phase_slider.grid(row=8, column=0, padx=10, columnspan=2)
        self.plot_window.get_tk_widget().grid(row=0, column=2, rowspan=15)
        update_plot_button.grid(row=14, column=0, columnspan=2)

    def numerical_simulation_tab_construction(self, tab):
        # Widgets for this tab
        run_default_simulation_button = tk.Button(tab, text="Run default simulation", command = self.run_default_simulation)
        run_custom_simulation_buttom = tk.Button(tab, text="Run custom simulation", command = self.run_custom_simulation)


        # Packing widgets
        run_default_simulation_button.grid(row=0,column=0, columnspan=2)
        run_custom_simulation_buttom.grid(row=1, column=0, columnspan=2)

    def output_tab_construction(self, tab):
        # Widgets for this tab
        message_to_user = tk.Label(tab, text="Work in progress!")

        # Packing widgets
        message_to_user.grid(row=0, column=0)

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
            self.frequency_slider.grid(row=6, column=0, padx=10, columnspan=2)
            self.phase_slider.grid(row=8, column=0, padx=10, columnspan=2)

            amplitude = self.amplitude_slider.get()
            frequency = self.frequency_slider.get()
            phase = self.phase_slider.get()
            self.curve.set_ydata(
                [(amplitude * np.sin(frequency * element - phase)) for element in x]
            )

        elif curve_type == "Gaussian":
            self.frequency_slider.grid_forget()
            self.phase_slider.grid_forget()
            self.gaussian_shift_slider.grid(row=6, column=0, columnspan=2, padx=20)

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
        timeOutput = np.array([0.5, 1, 2, 1e8])

        hu_i = np.zeros(np.shape(x))
        h_i = np.array(h_i) + 2
        x = np.array(x)

        dx = self.x_limit.get() / nx

        fig = SWE_1D(
        dx, x, time_length, nx, h=h_i, hu=hu_i, time_output=timeOutput
        )

        temp_window = FigureCanvasTkAgg(fig, master = self.numerical_simulation_tab)
        temp_window.get_tk_widget().grid(row=0, column = 2, rowspan=15)
        close('all')

    def run_default_simulation(self):
        timeOutput=np.array([0.5, 1, 2, 1e8])

        domainLength: float = 20.0  # meter
        xTotalNumber: int = 100
        timeLength: float = 4.0  # second
        timeOutput = np.array([0.5, 1, 2, 1e8])

        dx: float = domainLength / xTotalNumber
        xArray = np.linspace(-domainLength / 2, domainLength / 2 - dx, xTotalNumber)
        h_i, hu_i = inputInitialValue(xArray, xTotalNumber)


        fig = SWE_1D(
        dx, xArray, timeLength, xTotalNumber, h=h_i, hu=hu_i, time_output=timeOutput
        )

        temp_window = FigureCanvasTkAgg(fig, master = self.numerical_simulation_tab)
        temp_window.get_tk_widget().grid(row=0, column = 2, rowspan=15)
        close('all')



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
