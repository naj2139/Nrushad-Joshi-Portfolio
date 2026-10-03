"""
ReLU on the GPU with PyCUDA.

Implements an element-wise ReLU kernel (out[i] = max(in[i], 0)) and compares
two host-side memory-management strategies:
    - relu_explicit : manual cuda.mem_alloc() / memcpy_htod() / memcpy_dtoh()
    - relu_gpuarray : PyCUDA's gpuarray abstraction (to_gpu() / .get())

Both are timed with CUDA events (kernel-only and end-to-end, in seconds) and
benchmarked against a NumPy CPU baseline across vector sizes from 10 to 1e8.

Run with:  python relu_pycuda.py
Outputs correctness results to stdout and saves 'relu_cuda_timing.png'.
"""

import time
import math
import numpy as np

import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
from pycuda import gpuarray

import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt


# ===================== CUDA KERNELS ====================
CUDA_CODE = """

// ============ ReLU ============
// Computes out[i] = max(in[i], 0.0f) for every 0 <= i < n.
// One thread handles one element.

__global__ void relu(float* out, const float* in, const unsigned int n){

    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    if (idx < n){
        out[idx] = fmaxf(in[idx], 0.0f);
    }
}

"""


class reluModule:
    def __init__(self):
        """
        Compile the kernel once at construction so it is not recompiled on
        every call. Uses a fixed 1D block size; the grid size is computed
        from N per call.
        """
        self.mod = SourceModule(CUDA_CODE)
        self.block_size = 256

    def relu_explicit(self, x):
        """
        Compute ReLU of vector x on the GPU with explicit memory management
        (cuda.mem_alloc, cuda.memcpy_htod, cuda.memcpy_dtoh).

        Timing (CUDA events):
          - kernel_time: kernel execution only.
          - total_time : allocation + host-to-device copy + kernel +
                         device-to-host copy.

        Arguments:
            x           :   1D numpy array of np.float32
        Returns:
            y           :   1D numpy array of np.float32, y = ReLU(x)
            kernel_time :   kernel-only execution time, in seconds
            total_time  :   total end-to-end execution time, in seconds
        """
        n = np.uint32(len(x))

        # Host output buffer
        y = np.empty(shape=n, dtype=np.float32)

        # Timing events
        total_start, total_end, kernel_start, kernel_end = cuda.Event(), cuda.Event(), cuda.Event(), cuda.Event()

        func = self.mod.get_function("relu")
        grid = math.ceil(n/self.block_size)

        total_start.record()

        # Device allocation and host-to-device transfer
        in_d = cuda.mem_alloc(x.nbytes)
        out_d = cuda.mem_alloc(x.nbytes)
        cuda.memcpy_htod(in_d, x)

        # Kernel launch
        kernel_start.record()
        func(out_d, in_d, n, grid=(grid,1,1), block=(self.block_size,1,1))
        kernel_end.record()

        # Device-to-host transfer
        cuda.memcpy_dtoh(y, out_d)

        total_end.record()
        total_end.synchronize()

        # time_till() returns milliseconds; convert to seconds
        kernel_time = kernel_start.time_till(kernel_end) / 1000
        total_time = total_start.time_till(total_end) / 1000

        in_d.free()
        out_d.free()

        return y, kernel_time, total_time

    def relu_gpuarray(self, x):
        """
        Compute ReLU of vector x on the GPU using the gpuarray class
        (gpuarray.to_gpu / .get), launching the same 'relu' kernel.

        Timing (CUDA events):
          - kernel_time: kernel execution only.
          - total_time : gpuarray allocation + transfer + kernel + .get().

        Arguments:
            x           :   1D numpy array of np.float32
        Returns:
            y           :   1D numpy array of np.float32, y = ReLU(x)
            kernel_time :   kernel-only execution time, in seconds
            total_time  :   total end-to-end execution time, in seconds
        """
        n = np.uint32(len(x))

        # Timing events
        total_start, total_end, kernel_start, kernel_end = cuda.Event(), cuda.Event(), cuda.Event(), cuda.Event()

        func = self.mod.get_function("relu")
        grid = math.ceil(n/self.block_size)

        total_start.record()

        # Device allocation and transfer via gpuarray
        in_d = gpuarray.to_gpu(x)
        out_d = gpuarray.empty(shape=n, dtype=np.float32)

        # Kernel launch
        kernel_start.record()
        func(out_d, in_d, n, grid=(grid,1,1), block=(self.block_size,1,1))
        kernel_end.record()

        # Device-to-host transfer
        y = out_d.get()

        total_end.record()
        total_end.synchronize()

        # time_till() returns milliseconds; convert to seconds
        kernel_time = kernel_start.time_till(kernel_end) / 1000
        total_time = total_start.time_till(total_end) / 1000

        return y, kernel_time, total_time

    def relu_cpu(self, x):
        """
        Serial ReLU on the host (CPU) - the reference implementation.

        Arguments:
            x       :   1D numpy array of np.float32
        Returns:
            y       :   ReLU(x)
            time    :   execution time in seconds
        """
        start = time.time()
        y = np.maximum(x, np.float32(0.0))
        end = time.time()
        return y, end - start


###############################################################################
#                               TEST HARNESS                                  #
###############################################################################

def make_test_cases():
    """Build the correctness test suite: (name, input_vector) pairs."""
    rng = np.random.default_rng(4750)
    tests = [
        ("example_1",             np.array([-2.0, -1.0, 0.0, 1.0, 2.0], dtype=np.float32)),
        ("example_2",             np.array([-3.5, 0.0, 4.2], dtype=np.float32)),
        ("single_element",        np.array([-7.5], dtype=np.float32)),
        ("all_negative",          -rng.random(4096, dtype=np.float32) - np.float32(0.5)),
        ("all_positive",          rng.random(4096, dtype=np.float32) + np.float32(0.5)),
        ("non_multiple_of_block", rng.standard_normal(1_000_003).astype(np.float32)),
        ("large_25M",             rng.standard_normal(25_000_000).astype(np.float32)),
    ]
    return tests


if __name__ == "__main__":
    module = reluModule()

    # ------------------------------------------------------------------
    # Part 1: Correctness tests
    # ------------------------------------------------------------------
    print("=" * 78)
    print("Part 1: Correctness tests (PyCUDA)")
    print("=" * 78)

    all_passed = True
    for name, x in make_test_cases():
        expected = np.maximum(x, np.float32(0.0))

        y_exp, _, _ = module.relu_explicit(x)
        y_gpu, _, _ = module.relu_gpuarray(x)

        ok_exp = (y_exp.shape == expected.shape) and np.array_equal(y_exp, expected)
        ok_gpu = (y_gpu.shape == expected.shape) and np.array_equal(y_gpu, expected)
        ok = ok_exp and ok_gpu
        all_passed = all_passed and ok

        print(f"[{'PASS' if ok else 'FAIL'}] {name:<24} N={len(x):>12,}   "
              f"relu_explicit: {'PASS' if ok_exp else 'FAIL'}   "
              f"relu_gpuarray: {'PASS' if ok_gpu else 'FAIL'}")

    print("-" * 78)
    if all_passed:
        print("All correctness tests PASSED.")
    else:
        print("Some correctness tests FAILED.")
    print()

    # ------------------------------------------------------------------
    # Part 2: Benchmark sweep
    # ------------------------------------------------------------------
    print("=" * 78)
    print("Part 2: Benchmark sweep (PyCUDA)")
    print("=" * 78)

    REPS = 10
    sizes = [10 ** k for k in range(1, 9)]  # 10, 100, ..., 100,000,000

    avg_explicit_kernel, avg_explicit_total = [], []
    avg_gpuarray_kernel, avg_gpuarray_total = [], []
    avg_cpu = []

    rng = np.random.default_rng(2026)
    for N in sizes:
        x = rng.standard_normal(N).astype(np.float32)

        t_ek, t_et, t_gk, t_gt, t_c = [], [], [], [], []
        for _ in range(REPS):
            _, kt, tt = module.relu_explicit(x)
            t_ek.append(kt); t_et.append(tt)
            _, kt, tt = module.relu_gpuarray(x)
            t_gk.append(kt); t_gt.append(tt)
            _, ct = module.relu_cpu(x)
            t_c.append(ct)

        avg_explicit_kernel.append(np.average(t_ek))
        avg_explicit_total.append(np.average(t_et))
        avg_gpuarray_kernel.append(np.average(t_gk))
        avg_gpuarray_total.append(np.average(t_gt))
        avg_cpu.append(np.average(t_c))

        print(f"N={N:>12,} | explicit kernel {avg_explicit_kernel[-1]:.3e}s "
              f"| explicit total {avg_explicit_total[-1]:.3e}s "
              f"| gpuarray kernel {avg_gpuarray_kernel[-1]:.3e}s "
              f"| gpuarray total {avg_gpuarray_total[-1]:.3e}s "
              f"| cpu {avg_cpu[-1]:.3e}s")

    plt.figure()
    plt.title('ReLU average execution time (PyCUDA)')
    plt.loglog(sizes, avg_explicit_kernel, 'o-', label='Explicit (kernel only)')
    plt.loglog(sizes, avg_explicit_total, 'o--', label='Explicit (total)')
    plt.loglog(sizes, avg_gpuarray_kernel, 's-', label='gpuarray (kernel only)')
    plt.loglog(sizes, avg_gpuarray_total, 's--', label='gpuarray (total)')
    plt.loglog(sizes, avg_cpu, '^-', label='CPU (numpy)')
    plt.xlabel('Vector length N')
    plt.ylabel('Average runtime over %d runs (seconds)' % REPS)
    plt.legend(loc='upper left')
    plt.grid(True, which='both', alpha=0.3)
    plt.savefig('relu_cuda_timing.png', dpi=300)
    print("\nTiming plot saved as 'relu_cuda_timing.png'.")
