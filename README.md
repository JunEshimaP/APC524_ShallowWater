# APC524_ShallowWater
This document is an overview document. Each program has more detailed in-program documentation.
The app has three tabs (and an introduction tab). The user interface, the numerical solver and the output.
To run the app, simply execute the user_interface.py file:

`python src/user_interface.py`

## Input
+ Allows the user to choose the domain
+ Allows the user to choose the FPS
+ Allows the user to choose the initial condition
+ Has some sample initial conditions
+ Uses tkinter mainly

## Numerical Simulation
+ Solves the shallow water wave equations using user specified numerical schemes
+ User can choose the time integration method and the spatial integration method
+ Sample results:
![1Dwaves](https://user-images.githubusercontent.com/112533493/199803223-45be82d2-bd81-461a-851e-1a0bfc35f79d.png)

## Output
+ Takes in the output of the 1D shallow water solver to make a mp4 file
+ Note: ffmpeg needs to be installed in order for this to run
+ Plays the output movie
+ Includes interactive progress bar, play/pause button and more
+ Uses tkinter and tkVideoPlayer mainly

## Automated Testing
There are two test files: test_SWE_1D_cpp.py and test_SWE_1D.py. Checks for standard things such as correct output format etc. In addition, checks against benchmarks created via a working previous version and a separate c++ version. 

## Miscellaneous files
### Pre-Commit
.pre-commit-config.yaml file is responsible for configuring the pre-commit.
The pre-commit runs some standard stylistic changes from https://github.com/pre-commit/pre-commit-hooks and black.

### Requirements
requirements.txt contains all the python packages that are required to run the program.

### Actions
.github/workflows/ci.yml does continuous integration. pyproject.toml has the project information.
requirements.txt installs the python files and then the pytests are run automatically. The tests are run for macOS and windows (the two types used by the authors).
