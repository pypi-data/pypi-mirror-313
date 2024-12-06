"""
This example shows how a circle can be plotted to the terminal with nearly equal
axis scaling. See figures/eg_circle.png.
"""

import numpy as np
import itrm

t = np.linspace(0, 2*np.pi, 1000)
x = np.cos(t)
y = np.sin(t)

xd = [-2, 2, 2, -2]
yd = [-2, -2, 2, 2]

itrm.plot([x, xd], [y, yd], ea=True)
