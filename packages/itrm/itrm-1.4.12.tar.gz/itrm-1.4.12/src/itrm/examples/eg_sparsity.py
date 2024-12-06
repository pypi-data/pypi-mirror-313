"""
This example shows how a sparsity plot looks with ASCII characters and then
again with Unicode characters. See figures/eg_sparsity.png.
"""

import numpy as np
import itrm

N = 50
M = np.random.randn(N, N)
M = M.T @ M
M = (M > 3)
itrm.spy(M, uni=False)
itrm.spy(M, uni=True)
