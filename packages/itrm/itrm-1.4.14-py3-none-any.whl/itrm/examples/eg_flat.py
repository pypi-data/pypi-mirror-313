import numpy as np
import itrm

K = 100
x = np.linspace(0, 1, K)
y = np.outer(10.0**np.arange(-12, 13), np.ones(K))
itrm.iplot(x, y)
