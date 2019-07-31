# vis1.py: An implementation of the "Perpetual Diamond" visual motion illusion.

This work was inspired by the
[paper](https://journals.sagepub.com/doi/full/10.1177/2041669518815708)
of Flynn and Shapiro.

## Introduction

The mechanics behind the illusion are clearly explained in the Flynn &
Shapiro paper, which is well worth reading.  The purpose of this
program (vis1.py) is to enable experimentation with all of the dynamic and
static display parameters.

To use this code, simply clone this repository or download vis1.py and
adjuster.py, make vis1.py executable, and run vis1.py.  The code
requires the Tkinter module and is written for Python 2.7, but could
be modified slightly to run with Python 3.

When vis1.py is started you should see two windows: a pulsating square
with a diamond in its center, and a control panel with several
horizontal parameter control sliders.  The diamond should appear to be
moving to the right.

## Display Controls

The top four sliders control the relative phases of the intensity
modulation of the four sides of the border pixels of the diamond.  The
sides are numbered 1 through 4 starting with the upper left side and
going clockwise around the diamond.  Phases may be adjusted from +90
to -90 degrees relative to the background sinusoidal intensity
modulation.  Positive phasing of a side tends to make the side appear
to move away from the diamond center and negative phasing tends to
make it appear to move toward the center.

Rate (Hz): Controls the rate of the background and border pixels
sinusoidal intensity modulation (cycles per second).

Contrast: Controls the depth of the intensity modulation.

Static Red, Green, Blue: Control the RGB color mix applied to the
non-pulsating center diamond.

Dynamic Red, Green, Blue: Control the RGB color mix of the modulated
background and of the phase shifted border pixels of the diamond.

Border Width: The width in pixels of the modulated, phase-shifted
sides of the diamond.  (The fractional part of this slider's numerical
display is ignored.)
