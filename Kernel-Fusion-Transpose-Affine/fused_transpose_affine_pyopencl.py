"""
Kernel fusion for a layout conversion + per-channel affine transform (PyOpenCL).

Same problem and the same three implementations as the PyCUDA version:

    X      : (C, N) float32, channel-major
    gamma  : (C,)   float32
    beta   : (C,)   float32
    Y      : (N, C) float32, batch-major

    Y[n, c] = gamma[c] * X[c, n] + beta[c]

    1. unfused_hostroundtrip()  two kernels; Xt round-trips through the host
    2. unfused()                two kernels; Xt stays on the device
    3. fused()                  one kernel; no intermediate

Work-group size is 32 x 32. The global size is rounded up to a multiple of
32 in each dimension, and every kernel discards out-of-range work-items.

Usage
-----
    python3 fused_transpose_affine_pyopencl.py -m test
    python3 fused_transpose_affine_pyopencl.py -m bench
    python3 fused_transpose_affine_pyopencl.py -m ratio
"""

import time
import argparse
import numpy as np
import pyopencl as cl

import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt


# ============================= OPENCL KERNELS ==============================
KERNEL_CODE = """
// Xt[n, c] = X[c, n]. Mapping: dim0 -> n, dim1 -> c.
__kernel void transpose_kernel(
    __global float* Xt, __global const float* X,
    const unsigned int C, const unsigned int N
) {
    const unsigned int c = get_group_id(1) * get_local_size(1) + get_local_id(1);
    const unsigned int n = get_group_id(0) * get_local_size(0) + get_local_id(0);
    if (n < N && c < C) {
        Xt[n * C + c] = X[c * N + n];
    }
}

// Y[n, c] = gamma[c] * Xt[n, c] + beta[c]. Mapping: dim0 -> c, dim1 -> n.
__kernel void affine_kernel(
    __global float* Y, __global const float* Xt,
    __global const float* gamma, __global const float* beta,
    const unsigned int C, const unsigned int N
) {
    const unsigned int n = get_group_id(1) * get_local_size(1) + get_local_id(1);
    const unsigned int c = get_group_id(0) * get_local_size(0) + get_local_id(0);
    if (n < N && c < C) {
        Y[n * C + c] = gamma[c] * Xt[n * C + c] + beta[c];
    }
}

// Y[n, c] = gamma[c] * X[c, n] + beta[c]. Mapping: dim0 -> n, dim1 -> c.
__kernel void fused_kernel(
    __global float* Y, __global const float* X,
    __global const float* gamma, __global const float* beta,
    const unsigned int C, const unsigned int N
) {
    const unsigned int c = get_group_id(1) * get_local_size(1) + get_local_id(1);
    const unsigned int n = get_group_id(0) * get_local_size(0) + get_local_id(0);
    if (n < N && c < C) {
        Y[n * C + c] = gamma[c] * X[c * N + n] + beta[c];
    }
}
"""

LOCAL = 32
MF = cl.mem_flags


def _global_size(fast_dim, slow_dim):
    """Global size rounded up to a multiple of the 32 x 32 work-group."""
    return ((fast_dim + LOCAL - 1) // LOCAL * LOCAL,
            (slow_dim + LOCAL - 1) // LOCAL * LOCAL)


def _kernel_seconds(evt):
    """OpenCL profiling timestamps are in nanoseconds."""
    return 1e-9 * (evt.profile.end - evt.profile.start)


class OpenCLFusion:
    def __init__(self, platform_name='NVIDIA CUDA'):
        devs = None
        for platform in cl.get_platforms():
            if platform.name == platform_name:
                devs = platform.get_devices()
        if devs is None:
            raise RuntimeError(f"OpenCL platform '{platform_name}' not found")

        self.ctx = cl.Context(devs)
        self.queue = cl.CommandQueue(
            self.ctx, properties=cl.command_queue_properties.PROFILING_ENABLE)
        self.prg = cl.Program(self.ctx, KERNEL_CODE).build()
        self.local = (LOCAL, LOCAL)

        # Retrieve each kernel once and reuse it.
        self.transpose_kernel = cl.Kernel(self.prg, "transpose_kernel")
        self.affine_kernel = cl.Kernel(self.prg, "affine_kernel")
        self.fused_kernel = cl.Kernel(self.prg, "fused_kernel")

    def _upload(self, arr):
        return cl.Buffer(self.ctx, MF.READ_ONLY | MF.COPY_HOST_PTR, hostbuf=arr)

    # ------------------------------------------------------------------
    # 1. Two kernels, intermediate round-trips through the host
    # ------------------------------------------------------------------
    def unfused_hostroundtrip(self, X, gamma, beta):
        """
        H2D X, gamma, beta -> transpose -> D2H Xt -> H2D Xt -> affine -> D2H Y

        Returns (Y, kernel_time_s, total_time_s). kernel_time comes from event
        profiling; total_time is wall clock around the whole sequence.
        """
        C, N = X.shape
        C_u, N_u = np.uint32(C), np.uint32(N)
        start_time = time.time()

        X_d = self._upload(X)
        gamma_d = self._upload(gamma)
        beta_d = self._upload(beta)
        Xt_d = cl.Buffer(self.ctx, MF.READ_WRITE, size=X.nbytes)

        evt_1 = self.transpose_kernel(self.queue, _global_size(N, C), self.local,
                                      Xt_d, X_d, C_u, N_u)
        evt_1.wait()

        # Bring Xt back to the host, then up again into a fresh buffer.
        Xt_h = np.empty((N, C), dtype=np.float32)
        cl.enqueue_copy(self.queue, Xt_h, Xt_d)
        Xt_d.release()

        Xt_d = self._upload(Xt_h)
        Y_d = cl.Buffer(self.ctx, MF.WRITE_ONLY, size=Xt_h.nbytes)
        evt_2 = self.affine_kernel(self.queue, _global_size(C, N), self.local,
                                   Y_d, Xt_d, gamma_d, beta_d, C_u, N_u)
        evt_2.wait()

        Y = np.empty((N, C), dtype=np.float32)
        cl.enqueue_copy(self.queue, Y, Y_d)

        for buf in (Y_d, gamma_d, beta_d, X_d, Xt_d):
            buf.release()

        total_time = time.time() - start_time
        kernel_time = _kernel_seconds(evt_1) + _kernel_seconds(evt_2)
        return Y, kernel_time, total_time

    # ------------------------------------------------------------------
    # 2. Two kernels, intermediate stays on the device
    # ------------------------------------------------------------------
    def unfused(self, X, gamma, beta):
        """H2D X, gamma, beta -> transpose -> affine -> D2H Y. Xt stays on device."""
        C, N = X.shape
        C_u, N_u = np.uint32(C), np.uint32(N)
        start_time = time.time()

        X_d = self._upload(X)
        gamma_d = self._upload(gamma)
        beta_d = self._upload(beta)
        Xt_d = cl.Buffer(self.ctx, MF.READ_WRITE, size=X.nbytes)

        evt_1 = self.transpose_kernel(self.queue, _global_size(N, C), self.local,
                                      Xt_d, X_d, C_u, N_u)
        evt_1.wait()

        Y_d = cl.Buffer(self.ctx, MF.WRITE_ONLY, size=X.nbytes)
        evt_2 = self.affine_kernel(self.queue, _global_size(C, N), self.local,
                                   Y_d, Xt_d, gamma_d, beta_d, C_u, N_u)
        evt_2.wait()
        Xt_d.release()

        Y = np.empty((N, C), dtype=np.float32)
        cl.enqueue_copy(self.queue, Y, Y_d)

        for buf in (Y_d, gamma_d, beta_d, X_d):
            buf.release()

        total_time = time.time() - start_time
        kernel_time = _kernel_seconds(evt_1) + _kernel_seconds(evt_2)
        return Y, kernel_time, total_time

    # ------------------------------------------------------------------
    # 3. One fused kernel
    # ------------------------------------------------------------------
    def fused(self, X, gamma, beta):
        """H2D X, gamma, beta -> fused -> D2H Y. No intermediate array."""
        C, N = X.shape
        C_u, N_u = np.uint32(C), np.uint32(N)
        start_time = time.time()

        X_d = self._upload(X)
        gamma_d = self._upload(gamma)
        beta_d = self._upload(beta)
        Y_d = cl.Buffer(self.ctx, MF.WRITE_ONLY, size=X.nbytes)

        evt = self.fused_kernel(self.queue, _global_size(N, C), self.local,
                                Y_d, X_d, gamma_d, beta_d, C_u, N_u)
        evt.wait()

        Y = np.empty((N, C), dtype=np.float32)
        cl.enqueue_copy(self.queue, Y, Y_d)

        for buf in (Y_d, gamma_d, beta_d, X_d):
            buf.release()

        total_time = time.time() - start_time
        return Y, _kernel_seconds(evt), total_time

    # ------------------------------------------------------------------
    # CPU reference
    # ------------------------------------------------------------------
    @staticmethod
    def cpu(X, gamma, beta):
        start = time.time()
        Y = gamma[None, :] * X.T + beta[None, :]
        return Y, time.time() - start


# ================================ HARNESS ==================================
RTOL = 1e-5
ATOL = 1e-6


def make_test_cases():
    """Degenerate shapes, non-multiples of 32, both aspect ratios."""
    rng = np.random.default_rng(4750)

    def rand(C, N):
        X = np.ascontiguousarray(rng.standard_normal((C, N)), dtype=np.float32)
        g = np.ascontiguousarray(rng.standard_normal(C), dtype=np.float32)
        b = np.ascontiguousarray(rng.standard_normal(C), dtype=np.float32)
        return X, g, b

    tests = [(
        "worked_example_C2_N3",
        np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32),
        np.array([2.0, 0.5], dtype=np.float32),
        np.array([0.0, 1.0], dtype=np.float32),
    )]
    tests.append(("C1_N1",         *rand(1, 1)))
    tests.append(("C1_N100003",    *rand(1, 100003)))
    tests.append(("C1024_N1",      *rand(1024, 1)))
    tests.append(("C37_N53",       *rand(37, 53)))
    tests.append(("C33_N1025",     *rand(33, 1025)))
    tests.append(("C512_N7_tall",  *rand(512, 7)))
    tests.append(("C7_N512_wide",  *rand(7, 512)))

    C, N = 64, 1000
    X = np.ascontiguousarray(rng.standard_normal((C, N)), dtype=np.float32)
    tests.append(("shift_only_gamma1", X, np.ones(C, dtype=np.float32),
                  np.ascontiguousarray(rng.standard_normal(C), dtype=np.float32)))
    tests.append(("scale_only_beta0", X,
                  np.ascontiguousarray(rng.standard_normal(C), dtype=np.float32),
                  np.zeros(C, dtype=np.float32)))
    tests.append(("C128_N100000", *rand(128, 100000)))
    return tests


def run_tests(module):
    print("=" * 100)
    print("Correctness tests (PyOpenCL)")
    print(f"        tolerance: np.allclose(rtol={RTOL}, atol={ATOL})")
    print("=" * 100)

    all_passed = True
    for name, X, gamma, beta in make_test_cases():
        C, N = X.shape
        expected, _ = module.cpu(X, gamma, beta)

        def check(y):
            return y.shape == expected.shape and np.allclose(
                y, expected, rtol=RTOL, atol=ATOL)

        ok_hrt = check(module.unfused_hostroundtrip(X, gamma, beta)[0])
        ok_unf = check(module.unfused(X, gamma, beta)[0])
        ok_fus = check(module.fused(X, gamma, beta)[0])
        ok = ok_hrt and ok_unf and ok_fus
        all_passed &= ok

        print(f"[{'PASS' if ok else 'FAIL'}] {name:<22} C={C:>6,} N={N:>9,}   "
              f"hostroundtrip: {'PASS' if ok_hrt else 'FAIL'}   "
              f"unfused: {'PASS' if ok_unf else 'FAIL'}   "
              f"fused: {'PASS' if ok_fus else 'FAIL'}")

    print("-" * 100)
    print("All correctness tests PASSED." if all_passed
          else "Some correctness tests FAILED.")
    print()
    return all_passed


def run_bench(module):
    """C fixed at 128, N swept from 10 to 1e6."""
    print("=" * 100)
    print("Benchmark sweep (PyOpenCL), C fixed at 128")
    print("=" * 100)

    REPS = 5
    C = 128
    sizes = [10 ** k for k in range(1, 7)]

    hrt_k, hrt_t, unf_k, unf_t, fus_k, fus_t, cpu_t = ([] for _ in range(7))

    rng = np.random.default_rng(2026)
    for N in sizes:
        X = np.ascontiguousarray(rng.standard_normal((C, N)), dtype=np.float32)
        gamma = np.ascontiguousarray(rng.standard_normal(C), dtype=np.float32)
        beta = np.ascontiguousarray(rng.standard_normal(C), dtype=np.float32)

        a, b, c_, d, e, f, g = ([] for _ in range(7))
        for _ in range(REPS):
            _, kt, tt = module.unfused_hostroundtrip(X, gamma, beta)
            a.append(kt); b.append(tt)
            _, kt, tt = module.unfused(X, gamma, beta)
            c_.append(kt); d.append(tt)
            _, kt, tt = module.fused(X, gamma, beta)
            e.append(kt); f.append(tt)
            g.append(module.cpu(X, gamma, beta)[1])

        hrt_k.append(np.mean(a)); hrt_t.append(np.mean(b))
        unf_k.append(np.mean(c_)); unf_t.append(np.mean(d))
        fus_k.append(np.mean(e)); fus_t.append(np.mean(f))
        cpu_t.append(np.mean(g))

        print(f"N={N:>10,} | hostroundtrip {hrt_k[-1]:.3e}/{hrt_t[-1]:.3e}s "
              f"| unfused {unf_k[-1]:.3e}/{unf_t[-1]:.3e}s "
              f"| fused {fus_k[-1]:.3e}/{fus_t[-1]:.3e}s "
              f"| cpu {cpu_t[-1]:.3e}s      (kernel/total)")

    plt.figure(figsize=(8, 6))
    plt.title('Transpose + per-channel affine, C=128 (PyOpenCL)')
    plt.loglog(sizes, hrt_k, 'o-', label='host round trip (kernel only)')
    plt.loglog(sizes, hrt_t, 'o--', label='host round trip (total)')
    plt.loglog(sizes, unf_k, 's-', label='unfused, device-only (kernel only)')
    plt.loglog(sizes, unf_t, 's--', label='unfused, device-only (total)')
    plt.loglog(sizes, fus_k, 'd-', label='fused (kernel only)')
    plt.loglog(sizes, fus_t, 'd--', label='fused (total)')
    plt.loglog(sizes, cpu_t, '^-', label='CPU (numpy)')
    plt.xlabel('N  (C fixed at 128)')
    plt.ylabel(f'Average runtime over {REPS} runs (seconds)')
    plt.legend(loc='upper left', fontsize=8)
    plt.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    plt.savefig('bench_opencl.png', dpi=300)
    print("\nPlot saved as 'bench_opencl.png'.\n")


def run_ratio(module):
    """C*N fixed at 2^24; only the aspect ratio changes."""
    print("=" * 100)
    print("Aspect-ratio sweep (PyOpenCL), C*N held fixed at 2^24")
    print("=" * 100)

    REPS = 5
    TOTAL = 2 ** 24
    c_values = [32, 128, 512, 2048, 8192, 32768]
    unf_k, fus_k, unf_t, fus_t = [], [], [], []

    rng = np.random.default_rng(2026)
    for C in c_values:
        N = TOTAL // C
        X = np.ascontiguousarray(rng.standard_normal((C, N)), dtype=np.float32)
        gamma = np.ascontiguousarray(rng.standard_normal(C), dtype=np.float32)
        beta = np.ascontiguousarray(rng.standard_normal(C), dtype=np.float32)

        a, b, c_, d = [], [], [], []
        for _ in range(REPS):
            _, kt, tt = module.unfused(X, gamma, beta)
            a.append(kt); b.append(tt)
            _, kt, tt = module.fused(X, gamma, beta)
            c_.append(kt); d.append(tt)

        unf_k.append(np.mean(a)); unf_t.append(np.mean(b))
        fus_k.append(np.mean(c_)); fus_t.append(np.mean(d))

        print(f"C={C:>7,} N={N:>10,} | unfused kernel {unf_k[-1]:.3e}s "
              f"| fused kernel {fus_k[-1]:.3e}s "
              f"| unfused total {unf_t[-1]:.3e}s "
              f"| fused total {fus_t[-1]:.3e}s")

    plt.figure(figsize=(8, 6))
    plt.title('Same total elements (C*N = 2^24), varying aspect ratio (PyOpenCL)')
    plt.loglog(c_values, unf_k, 's-', label='unfused (kernel only)')
    plt.loglog(c_values, unf_t, 's--', label='unfused (total)')
    plt.loglog(c_values, fus_k, 'd-', label='fused (kernel only)')
    plt.loglog(c_values, fus_t, 'd--', label='fused (total)')
    plt.xlabel('C  (N = 2^24 / C)')
    plt.ylabel(f'Average runtime over {REPS} runs (seconds)')
    plt.legend(loc='upper left', fontsize=8)
    plt.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    plt.savefig('ratio_opencl.png', dpi=300)
    print("\nPlot saved as 'ratio_opencl.png'.\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Kernel fusion: layout conversion + per-channel affine (PyOpenCL)")
    parser.add_argument('-m', '--mode', required=True,
                        choices=['test', 'bench', 'ratio'])
    args = parser.parse_args()

    module = OpenCLFusion()
    {'test': run_tests, 'bench': run_bench, 'ratio': run_ratio}[args.mode](module)
