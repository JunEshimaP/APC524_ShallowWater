import tkinter as tk
from tkinter import ttk
from tkVideoPlayer import *
import datetime

# sample_movies/sample.mp4
class InteractiveOutput:
    def __init__(self, master, moviefilename):
        # Build a container for this plot
        frame = tk.Frame(master)
        self.moviefilename = moviefilename
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
        message_to_user = tk.Label(tab, text="Work in progress!")

        # Packing widgets
        message_to_user.grid(row=0, column=0)

    def mesh_preview_tab_construction(self, tab):
        # Widgets for this tab
        message_to_user = tk.Label(tab, text="Work in progress!")

        # Packing widgets
        message_to_user.grid(row=0, column=0)

    def output_tab_construction(self, tab):

        # bar with some text (maybe put in values of physical variables etc)
        label = tk.Label(tab, text="Output:", fg="white", bg="black")
        self.pp_btn = tk.Button(tab, text="play", command=self.play_pause, width=5)

        # video player
        self.videoplayer = TkinterVideo(master=tab, scaled=True)
        self.videoplayer.load(self.moviefilename)
        self.videoplayer.pause()

        self.videoplayer.bind("<<SecondChanged>>", self.time_update)

        # elapsed time
        self.elapsed_time = tk.Label(
            tab, text=f"elapsed = {datetime.timedelta(seconds = 0)}s", width=15
        )

        # Packing widgets
        tab.rowconfigure([0, 1, 2, 3, 4, 5], minsize=50)
        tab.columnconfigure([0, 1, 2], minsize=50)
        label.grid(row=1, column=0, columnspan=3, sticky="ew")
        self.videoplayer.grid(row=2, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.pp_btn.grid(row=5, column=0)
        self.elapsed_time.grid(row=5, column=2)

    def time_update(self, event):
        self.elapsed_time[
            "text"
        ] = f"elapsed = {str(datetime.timedelta(seconds = self.videoplayer.current_duration()))}s"

    def play_pause(self):
        # play and pause button working
        if self.videoplayer.is_paused():
            self.videoplayer.play()
            self.pp_btn["text"] = "pause"

        else:
            self.videoplayer.pause()
            self.pp_btn["text"] = "play"


def initialize_window():
    # Initializes a window with a title/window size/a button
    window = tk.Tk()
    window.title("Shallow Water Wave Equations - Numerical Simulation")

    return window


def main():
    root = initialize_window()
    app = InteractiveOutput(root, r"sample_movies/sample.mp4")
    root.mainloop()


if __name__ == "__main__":
    main()
