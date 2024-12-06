# This script serves to show that searchsorted can be much faster than using a
# full array search. In this particular case, it was about 2400 times faster. In
# other cases it was much more.

# It would be nice to use the NumPy function "searchsorted" because it would in
# theory be more efficient given it relies on a binary search algorithm.
# However, it is not used because it does not correctly handle NaNs or
# infinities, unfortunately. There are at least two ways to overcome this
# limitation. The first is storing an additional pair of arrays for each data
# set: a copy of the x-axis without non-finite values and the corresponding
# indices of the original x-axis array. But, this could lead to effectively
# doubling the memory usage. The second way of overcoming the limitation is to
# simply remove all non-finite values from the x axis array and then remove the
# correspond y-axis values too. This would require no additional arrays except
# for no longer using the original data sets. Now, that right there would double
# the memory usage too. But, the whole operation would become much simpler. The
# downside to this approach is that the indices would no longer match the
# original data. But, that is basically the only limitation.

import numpy as np
import time
import itrm

# Build the x axis.
K = 10_000_000
T = 0.001
x = np.arange(K) * T

# Define constants.
xlg = False
x_cur_lin = 0.8 * K * T
k_a = 0
k_b = K - 1

pp = np.linspace(0.01, 0.99, 200)
rr = np.zeros(len(pp))

for j in range(len(pp)):
    dx = pp[j] * (x[-1] - x_cur_lin)
    x_new_lin = x_cur_lin + dx

    # Time using full array search.
    tic = time.perf_counter()
    is_fin = np.isfinite(x) if not xlg \
            else np.isfinite(x) & (x > 0)
    is_beyond = x > x_cur_lin if dx > 0 else x < x_cur_lin
    mm = (is_fin & is_beyond).nonzero()[0]
    if len(mm) == 0:
        k_cur = k_b if dx > 0 else k_a
    else:
        dst = np.abs(x[mm] - x_new_lin) if not xlg \
                else np.abs(np.log10(x[mm]) - x_new)
        n = dst.argmin()
        k_cur = mm[n] + k_a
    t1 = time.perf_counter() - tic


    # Time using search sorted.
    tic = time.perf_counter()
    k_cur = np.searchsorted(x, x_new_lin)
    t2 = time.perf_counter() - tic

    rr[j] = t1/t2

itrm.iplot(pp, rr)
