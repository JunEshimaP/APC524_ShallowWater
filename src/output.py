import tkinter as tk
from tkinter import ttk
from tkVideoPlayer import *
import datetime
import csv
import math

# sample_movies/sample.mp4
# infofile contains information on frame rate, duration etc.
class InteractiveOutput:
    """Sets up an interactive output

    Input
    -----
    master : tk window
        This is the window in which the output will be given

    moviefilename : string
        This is the location and name of the output movie (.mp4 file)

    infofilename : string
        This is the location and name of the information file with information
        on FPS and duration of the movie (.txt file)

    Methods
    -------
    __init__ :
        initialise values

    update_slider :
        update the time value of the slider

    settime_slider :
        change the progress of the movie based on input by the user

    play_pause :
        set up the play/pause button

    output_tab_construction :
        set up the tab by inserting labels, buttons, interactive sliders
        and play the move made in moviemaker.py
    """

    def __init__(self, master, moviefilename, infofilename):
        # Build a container for this plot
        frame = tk.Frame(master)
        self.moviefilename = moviefilename
        self.infofilename = infofilename

        # open the information file
        # information file will have:
        # FPS, duration
        with open(infofilename, "r") as datafile:
            information = csv.reader(datafile, delimiter=",")
            first_row_data = list(information)[0]
            self.FPS = int(first_row_data[0])
            self.totduration = float(first_row_data[1])

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
        label = tk.Label(tab, text=f"Output(FPS = {self.FPS}):", fg="white", bg="black")
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
            to=self.totduration,
            digits=1,
            resolution=1,
            orient=tk.HORIZONTAL,
            command=self.settime_slider,
            tickinterval=math.floor(self.totduration / 4),
            showvalue=0,
        )

        timefromstartlabel = tk.Label(tab, textvariable=self.currenttime)
        totdurationlabel = tk.Label(tab, text=str(self.totduration))

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


# Initializes a window with a title/window size/a button
def initialize_window():
    window = tk.Tk()
    window.title("Shallow Water Wave Equations - Numerical Simulation")

    return window


def main():
    root = initialize_window()
    app = InteractiveOutput(
        root, r"sample_movies/sample_generated.mp4", r"sample_movies/sampleinfo.txt"
    )
    root.mainloop()


if __name__ == "__main__":
    main()
