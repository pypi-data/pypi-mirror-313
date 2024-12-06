"""
This example shows a heat map first with ASCII characters and then again with
Unicode characters. See figures/eg_heat.png.
"""

import numpy as np
import itrm

N = 50
M = np.random.randn(N, N)
M = M.T @ M
itrm.heat(M, uni=False)
itrm.heat(M, uni=True)
