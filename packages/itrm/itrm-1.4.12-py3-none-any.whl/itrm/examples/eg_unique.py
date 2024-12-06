"""
This example provides the opportunity for testing the isolation of unique points
with the `fu` command in the interactive plot. See the following images in the
figures folder for expected results:
    eg_unique_initial.png
    eg_unique_fu.png            "fu" to isolate the unique points among the sets
"""

import numpy as np
import itrm

K = 100_000
x = np.linspace(0, 1, K)
y = np.zeros((3, K))
for j in range(3):
    y[j] = 0.3*np.sin(2*np.pi*3*x) \
            + 0.1*np.sin(2*np.pi*50*x) \
            + 0.01*np.sin(2*np.pi*310*x)
y += 0.05*np.random.randn(K)

na = K//5
nb = na + 100
y[1, na:nb] = np.nan
y[2, na:nb] = np.nan

nb = 4*K//5
na = nb - 100
y[0, na:nb] = np.nan
y[2, na:nb] = np.nan

itrm.iplot(x, y)
