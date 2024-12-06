import time
import numpy as np
import itrm

#K = 1000
#bar = itrm.progress(K, uni=False)
#for k in range(K):
#    time.sleep(0.01)
#    bar.update(k)
#bar = itrm.progress(K)
#for k in range(K):
#    time.sleep(0.01)
#    bar.update(k)

bar_A = itrm.progress(10, cols=0.5, msg="Progress A")
bar_B = itrm.progress(10, cols=0.5, msg="Progress B")
bar_C = itrm.progress(10, cols=0.5, msg="Progress C")
a = 0
b = 0
c = 0

while (a < 10) or (b < 10) or (c < 10):
    time.sleep(0.05) #Replace this with a real computation
    a += 0.1*np.random.uniform()
    b += 0.2*np.random.uniform()
    c += 0.1*np.random.uniform()
    if b > 5:
        bar_B.msg = None
    bar_A.update(a)
    bar_B.update(b)
    bar_C.update(c)
