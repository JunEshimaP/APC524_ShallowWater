"""
Create a movie from textfiles
File format is h, x, t
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


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

    def __init__(self, filename, N):
        self.filename = filename
        self.N = N
        # set up matplotlib as in matplotlib.animation documentation
        self.plottedgraphfig, self.plottedgraphfigax = plt.subplots()
        (self.curve,) = self.plottedgraphfigax.plot([], [])

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
        self.plottedgraphfigax.set_xlim(0, self.N - 1)
        self.plottedgraphfigax.set_ylim(0, 10)
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
        writervideo = animation.FFMpegWriter(fps=30)
        self.ani.save(r"sample_movies/sample_generated.mp4", writer=writervideo)


def main():
    app = makemovie(r"sample_movies/samplegraph.txt", 3)
    app.saveanimation()


if __name__ == "__main__":
    main()
