"""
This example illustrates the automatic color differentiation. Because white on
black or black on white is the easiest to see, a single curve will not have
color (see figures/eg_plot_single.png). When multiple curves are plotted
together, they will have different colors automatically (see
figures/eg_plot_multiple.png).
"""

import numpy as np
import itrm

# Constants
K = 2000
J = 3

# x axis
x = np.linspace(0, 1, K)

# y axis data
y = np.cos(2*np.pi*2*x)
Y = np.zeros((J, len(x)))
for j in range(J):
    Y[j] = np.cos(2*np.pi*2*x + (j/J)*np.pi)

# plots
itrm.plot(x, y, "Single curve")
itrm.plot(x, Y, "Multiple curves")
