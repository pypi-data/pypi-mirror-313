"""
This example shows an interactive plot with 6 different sine waves, each out of
phase from the other. See the following images in the figures folder for
expected results:
    eg_iplot_initial.png
    eg_iplot_ni.png             after "ni" to select and isolate blue
    eg_iplot_j.png              after "j"*10 times to zoom in
    eg_iplot_vl.png             after "v" then "l"*10 to select range
    eg_iplot_m.png              after "m" to change what shows in info bar
"""

import numpy as np
import itrm

# Constants
K = 200000
J = 6

# x axis
x = np.linspace(0, 1, K)

# y axis data
Y = np.zeros((J, len(x)))
for j in range(J):
    Y[j] = np.cos(2*np.pi*2*x + (j/J)*np.pi)

# plot
labels = ["Fruit", "Plum", "Grape", "Apple", "Banana", "Orange", "Cherry"]
itrm.iplot(x, Y, label=labels)
