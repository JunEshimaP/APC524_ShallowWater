import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class InteractiveUserInterface:
    def __init__(self, master):
        # Build a container for this plot
        frame = tk.Frame(master)

        # Create the tabs for the plotting
        tab_control = ttk.Notebook(master)
        input_tab = ttk.Frame(tab_control)
        mesh_preview_tab = ttk.Frame(tab_control)
        output_tab = ttk.Frame(tab_control)

        tab_control.add(input_tab, text="Input")
        tab_control.add(mesh_preview_tab, text="Mesh Preview")
        tab_control.add(output_tab, text="Output")

        self.input_tab_construction(input_tab)
        self.mesh_preview_tab_construction(mesh_preview_tab)
        self.output_tab_construction(output_tab)
        tab_control.pack(expand=1, fill="both")

    def input_tab_construction(self, tab):
        # Widgets for this tab
        increase_button = tk.Button(tab, text="Increase Slope", command=self.increase)
        decrease_button = tk.Button(tab, text="Decrease Slope", command=self.decrease)
        self.slope_slider = tk.Scale(
            tab,
            label="Line Slope",
            from_=-1,
            to=1,
            digits=2,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            command=self.update,
        )
        self.slope_slider.set(1)

        fig = Figure()
        ax = fig.add_subplot(111)
        (self.line,) = ax.plot(range(10))
        ax.set_xlim([0, 10])
        ax.set_ylim([-10, 10])
        self.canvas = FigureCanvasTkAgg(fig, master=tab)

        # Packing widgets
        increase_button.grid(row=1, column=0, padx=0, pady=0)
        decrease_button.grid(row=2, column=0, padx=0, pady=0)
        self.slope_slider.grid(row=3, column=0, padx=10, pady=10)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=10)

    def mesh_preview_tab_construction(self, tab):
        # Widgets for this tab
        message_to_user = tk.Label(tab, text="Work in progress!")

        # Packing widgets
        message_to_user.grid(row=0, column=0)

    def output_tab_construction(self, tab):
        # Widgets for this tab
        message_to_user = tk.Label(tab, text="Work in progress!")

        # Packing widgets
        message_to_user.grid(row=0, column=0)

    def decrease(self):
        # Decrease the slope of the line at the push of the button
        x, y = self.line.get_data()
        self.line.set_ydata(y - 0.2 * x)
        self.canvas.draw()

    def increase(self):
        # increase the slope of the line at the push of the button
        x, y = self.line.get_data()
        self.line.set_ydata(y + 0.2 * x)
        self.canvas.draw()

    def update(self, event):
        x, y = self.line.get_data()
        a = self.slope_slider.get()
        self.line.set_ydata(a * x)
        self.canvas.draw()


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
