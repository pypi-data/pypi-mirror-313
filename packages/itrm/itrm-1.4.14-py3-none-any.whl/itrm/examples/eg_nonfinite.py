"""
This example shows how non-finite values (i.e., NaN and inf) are handled by
interactive plots. See figures/eg_nonfinite.png.
"""

import numpy as np
import itrm

# Constants
K = 200000
J = 6

# x axis
x = np.linspace(0, 1, K)

# y axis data
Y = np.zeros((J, len(x)), dtype=complex)
for j in range(J):
    Y[j] = np.cos(2*np.pi*2*x + (j/J)*np.pi)

x[100000:150000] = np.nan
Y[3, 100000:150000] = np.nan
Y[4, 50000:70000] = np.inf
Y[5] += 1e-3 * 1j

# plot
itrm.iplot(x, Y,
        label=["Non-finite values", "A", "B", "C", "D", "E", "F"])
