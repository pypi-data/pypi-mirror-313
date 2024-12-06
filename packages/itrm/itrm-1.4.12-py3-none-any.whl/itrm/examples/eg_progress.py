"""
This example shows how progress bars look with ASCII characters and then again
with Unicode characters. See figures/eg_progress.png.
"""

import time
import itrm

K = 1000
bar = itrm.Progress(K, uni=False)
for k in range(K):
    time.sleep(0.01)
    bar.update(k)
bar = itrm.Progress(K)
for k in range(K):
    time.sleep(0.01)
    bar.update(k)
