import sys
import numpy as np
from time import perf_counter

argv = sys.argv[1:]
N = int(argv[0])
reps = int(argv[1])

A = np.ones(N, dtype=np.float32)
B = np.ones(N, dtype=np.float32)

T = 0
for idx in range(reps):
    start = perf_counter()
    dot_product = np.dot(A,B)
    end = perf_counter()
    if idx >= reps // 2:
        T += end - start
T /= reps/2
B = (8 * N) / T
B /= 1e9
F = (2 * N) / T

print(f"N: {N} <T>: {T:.6f} sec B: {B:.3f} GB/sec F: {F:.3f} FLOP/sec")
print(f"R: {float(dot_product):.6f}")