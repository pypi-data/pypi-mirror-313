"""
This example illustrates how to create an animated plot within a for loop. Each
new frame plots over the previous plot (see figures/eg_animation_midway.png),
thereby avoiding filling the terminal history with all of the previous plots.
After the loop is done, a final interactive plot is generated on top of the
previous plot (see figures/eg_animation_final.png).
"""

import numpy as np
import itrm

# Define time.
T = 0.01
t_dur = 15.0
K = round(t_dur/T) + 1
t = np.arange(K)*T

# Define the first-order, Gauss-Markov
# time constants and variances.
tau = np.array([0.1, 0.2, 0.4])
v = np.array([1.0, 0.5, 0.25])

# Get the discrete-domain constants.
ka = np.exp(-T/tau)
kb = np.sqrt(v*(1 - np.exp(-2*T/tau)))

# Get all the random inputs.
N = len(v)
eta = kb[:, None]*np.random.randn(N, K)

# Initialize the state and allocate memory.
x = np.zeros(N) # state
x_t = np.zeros((N, K))

labels = ["axes", "x-axis", "y-axis", "z-axis"]

for k in range(K):
    # Store the state.
    x_t[:, k] = x

    # Propagate the state.
    x = ka*x + eta[:, k]

    # Plot the history up to this moment.
    itrm.plot(t[:k+1], x_t[:, :k+1], labels, overlay=True, rows=0.8)

# Create an interactive plot.
itrm.iplot(t, x_t, labels, overlay=True, rows=0.8)
