"""
This example generates an interactive plot with 3 noisy curves. This can be used
to test the builtin filtering functions. See the following images in the figures
folder to see expected results:
    eg_noisy_initial.png
    eg_noisy_Ff100s.png         "Ff100s" to apply simple moving average
    eg_noisy_Ff100a.png         "Ff100a" to apply weighted moving average
    eg_noisy_Ff100l.png         "Ff100l" to apply low-pass filter at 100 Hz
"""

import numpy as np
import itrm

x = np.linspace(0, 1, 100_000)
y = np.zeros((3, len(x)))
for j in range(3):
    phi = 2*np.pi*j/3
    y[j] = 0.3*np.sin(2*np.pi*3*x + phi) \
            + 0.1*np.sin(2*np.pi*50*x + phi) \
            + 0.01*np.sin(2*np.pi*310*x + phi)
    y[j] += 0.05*np.random.randn(len(x))

itrm.iplot(x, y)
