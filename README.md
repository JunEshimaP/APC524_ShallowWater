# APC524_ShallowWater
This document is an overview document. Each program has more detailed in-program documentation.
Overall, the program has four main components. The user interface, the numerical solver, the movie maker and the output.

## User Interface
+ Allows the user to choose the numerical scheme
+ Allows the user to choose the FPS
+ Allows the user to choose the initial condition
+ Has some sample initial conditions
+ Uses tkinter mainly

## 1D shallow water solver
+ Time: Euler forward
+ Space: 2nd order central difference
+ Initial shape: gaussian hump
+ Boundary contion: periodic
+ Sample results:
![1Dwaves](https://user-images.githubusercontent.com/112533493/199803223-45be82d2-bd81-461a-851e-1a0bfc35f79d.png)

## Movie Maker
+ Takes in the output of the 1D shallow water solver to make a mp4 file
+ Note: ffmpeg needs to be installed in order for this to run

## Output
+ Plays the output movie
+ Includes interactive progress bar, play/pause button and more
+ Uses tkinter and tkVideoPlayer mainly

## Automated Testing
We did not include tests for certain parts of the code such as output.py since this was about configuring the set up (i.e. TKinter things) rather than computing anything.

## Miscellaneous files
### Pre-Commit
.pre-commit-config.yaml file is responsible for configuring the pre-commit.
The pre-commit runs some standard stylistic changes from https://github.com/pre-commit/pre-commit-hooks and black.

### Requirements
requirements.txt contains all the python packages that are required to run the program.

### Actions
.github/workflows/ci.yml does continuous integration. pyproject.toml has the project information.
requirements.txt installs the python files and then the pytests are run automatically. The tests are run for macOS and windows (the two types used by the authors).
