# output


import tkinter as tk
from tkVideoPlayer import TkinterVideo


window = tk.Tk()
label = tk.Label(text="Output:", fg="white", bg="black", width=100, height=10)
label.pack()

window.geometry("700x700")

videoplayer = TkinterVideo(master=window, scaled=True)
videoplayer.load(r"sample_movies/sample.mp4")
videoplayer.pack(expand=True, fill="both")


def play_pause():
    """Plays and pauses videos
    This piece of code is taken from https://github.com/PaulleDemon/tkVideoPlayer/blob/master/examples/sample_player.py
    """
    if videoplayer.is_paused():
        videoplayer.play()
        pp_btn["image"] = pause_image

    else:
        videoplayer.pause()
        pp_btn["image"] = play_image


play_image = tk.PhotoImage(file=r"designs/play_button.png")
pause_image = tk.PhotoImage(file=r"designs/pause_button.png")
pp_btn = tk.Button(window, image=pause_image, command=play_pause)
pp_btn.pack()

videoplayer.play()  # play the video

window.mainloop()
