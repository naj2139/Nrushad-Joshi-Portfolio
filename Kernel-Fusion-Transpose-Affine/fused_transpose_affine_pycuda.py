"""
Kernel fusion for a layout conversion + per-channel affine transform (PyCUDA).

Problem
-------
Inference pipelines often convert tensors between channel-major and
batch-major layouts between stages. At inference time a BatchNorm layer
reduces to a per-channel affine transform (the running statistics are frozen,
so they fold into two per-channel constants, gamma and beta). The combined op:

    X      : (C, N) float32, channel-major
    gamma  : (C,)   float32
    beta   : (C,)   float32
    Y      : (N, C) float32, batch-major

    Y[n, c] = gamma[c] * X[c, n] + beta[c]

Three implementations are compared:

    1. unfused_hostroundtrip()  two kernels; the intermediate Xt is copied
                                back to the host and up again in between
    2. unfused()                two kernels; Xt stays resident on the device
    3. fused()                  one kernel; Xt is never materialized

(1) vs (2) isolates the cost of a host round trip. (2) vs (3) isolates the
cost of materializing the intermediate in device global memory plus one
extra kernel launch.

Thread mapping (32 x 32 blocks)
-------------------------------
    transpose_kernel, fused_kernel : x -> n, y -> c  (coalesced read of X)
    affine_kernel                  : x -> c, y -> n  (coalesced read and write)

Usage
-----
    python3 fused_transpose_affine_pycuda.py -m test
    python3 fused_transpose_affine_pycuda.py -m bench
    python3 fused_transpose_affine_pycuda.py -m ratio
    nsys profile --trace=cuda --stats=true -o nsys_report \\
        python3 fused_transpose_affine_pycuda.py -m profile-nsys
    ncu --set full -o ncu_report \\
        python3 fused_transpose_affine_pycuda.py -m profile-ncu
"""

import time
import argparse
import numpy as np

import pycuda.autoinit  # noqa: F401  (creates the CUDA context)
import pycuda.driver as cuda
from pycuda.compiler import SourceModule

import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt


# ============================== CUDA KERNELS ===============================
CUDA_CODE = """
// Xt[n, c] = X[c, n]
// Pure data movement. Mapping: x -> n, y -> c.
__global__ void transpose_kernel(
    float* Xt, const float* X,
    const unsigned int C, const unsigned int N
) {
    const unsigned int c = blockDim.y * blockIdx.y + threadIdx.y;
    const unsigned int n = blockDim.x * blockIdx.x + threadIdx.x;
    if (n < N && c < C) {
        Xt[n * C + c] = X[c * N + n];
    }
}

// Y[n, c] = gamma[c] * Xt[n, c] + beta[c]
// Element-wise on the already-transposed (N, C) array. Mapping: x -> c, y -> n.
__global__ void affine_kernel(
    float* Y, const float* Xt,
    const float* gamma, const float* beta,
    const unsigned int C, const unsigned int N
) {
    const unsigned int n = blockDim.y * blockIdx.y + threadIdx.y;
    const unsigned int c = blockDim.x * blockIdx.x + threadIdx.x;
    if (n < N && c < C) {
        Y[n * C + c] = gamma[c] * Xt[n * C + c] + beta[c];
    }
}

// Y[n, c] = gamma[c] * X[c, n] + beta[c]
// Transpose and affine in a single pass; no intermediate. Mapping: x -> n, y -> c.
__global__ void fused_kernel(
    float* Y, const float* X,
    const float* gamma, const float* beta,
    const unsigned int C, const unsigned int N
) {
    const unsigned int c = blockDim.y * blockIdx.y + threadIdx.y;
    const unsigned int n = blockDim.x * blockIdx.x + threadIdx.x;
    if (n < N && c < C) {
        Y[n * C + c] = gamma[c] * X[c * N + n] + beta[c];
    }
}
"""

BLOCK = 32


def _grid(fast_dim, slow_dim):
    """Grid that covers (fast_dim, slow_dim) with BLOCK x BLOCK blocks."""
    return ((fast_dim + BLOCK - 1) // BLOCK, (slow_dim + BLOCK - 1) // BLOCK)


class CudaFusion:
    def __init__(self):
        self.mod = SourceModule(CUDA_CODE)
        self.block = (BLOCK, BLOCK, 1)
        self.transpose_kernel = self.mod.get_function("transpose_kernel")
        self.affine_kernel = self.mod.get_function("affine_kernel")
        self.fused_kernel = self.mod.get_function("fused_kernel")

    # ------------------------------------------------------------------
    # 1. Two kernels, intermediate round-trips through the host
    # ------------------------------------------------------------------
    def unfused_hostroundtrip(self, X, gamma, beta):
        """
        H2D X, gamma, beta -> transpose -> D2H Xt -> H2D Xt -> affine -> D2H Y

        Returns (Y, kernel_time_s, total_time_s). kernel_time is the sum of
        the two kernel durations; total_time covers every allocation and copy.
        """
        C, N = X.shape
        C_u, N_u = np.uint32(C), np.uint32(N)

        total_start, total_end = cuda.Event(), cuda.Event()
        k1_start, k1_end = cuda.Event(), cuda.Event()
        k2_start, k2_end = cuda.Event(), cuda.Event()
        total_start.record()

        X_d = cuda.mem_alloc(X.nbytes)
        Xt_d = cuda.mem_alloc(X.nbytes)
        gamma_d = cuda.mem_alloc(gamma.nbytes)
        beta_d = cuda.mem_alloc(beta.nbytes)

        cuda.memcpy_htod(X_d, X)
        cuda.memcpy_htod(gamma_d, gamma)
        cuda.memcpy_htod(beta_d, beta)

        k1_start.record()
        self.transpose_kernel(Xt_d, X_d, C_u, N_u,
                              grid=_grid(N, C), block=self.block)
        k1_end.record()

        # Bring Xt back to the host, then up again into a fresh buffer.
        Xt_h = np.empty((N, C), dtype=np.float32)
        cuda.memcpy_dtoh(Xt_h, Xt_d)
        X_d.free()
        Xt_d.free()

        Xt_d = cuda.mem_alloc(Xt_h.nbytes)
        Y_d = cuda.mem_alloc(Xt_h.nbytes)
        cuda.memcpy_htod(Xt_d, Xt_h)

        k2_start.record()
        self.affine_kernel(Y_d, Xt_d, gamma_d, beta_d, C_u, N_u,
                           grid=_grid(C, N), block=self.block)
        k2_end.record()

        Y = np.empty((N, C), dtype=np.float32)
        cuda.memcpy_dtoh(Y, Y_d)

        Xt_d.free()
        Y_d.free()
        gamma_d.free()
        beta_d.free()

        total_end.record()
        total_end.synchronize()

        kernel_time = (k1_start.time_till(k1_end)
                       + k2_start.time_till(k2_end)) / 1000
        total_time = total_start.time_till(total_end) / 1000
        return Y, kernel_time, total_time

    # ------------------------------------------------------------------
    # 2. Two kernels, intermediate stays on the device
    # ------------------------------------------------------------------
    def unfused(self, X, gamma, beta):
        """
        H2D X, gamma, beta -> transpose -> affine -> D2H Y

        Xt never touches the host. Host transfers are identical to fused(),
        so the difference between the two is device-side traffic only.
        """
        C, N = X.shape
        C_u, N_u = np.uint32(C), np.uint32(N)

        total_start, total_end = cuda.Event(), cuda.Event()
        k1_start, k1_end = cuda.Event(), cuda.Event()
        k2_start, k2_end = cuda.Event(), cuda.Event()
        total_start.record()

        X_d = cuda.mem_alloc(X.nbytes)
        Xt_d = cuda.mem_alloc(X.nbytes)
        gamma_d = cuda.mem_alloc(gamma.nbytes)
        beta_d = cuda.mem_alloc(beta.nbytes)

        cuda.memcpy_htod(X_d, X)
        cuda.memcpy_htod(gamma_d, gamma)
        cuda.memcpy_htod(beta_d, beta)

        k1_start.record()
        self.transpose_kernel(Xt_d, X_d, C_u, N_u,
                              grid=_grid(N, C), block=self.block)
        k1_end.record()

        Y_d = cuda.mem_alloc(X.nbytes)
        k2_start.record()
        self.affine_kernel(Y_d, Xt_d, gamma_d, beta_d, C_u, N_u,
                           grid=_grid(C, N), block=self.block)
        k2_end.record()

        Xt_d.free()

        Y = np.empty((N, C), dtype=np.float32)
        cuda.memcpy_dtoh(Y, Y_d)

        X_d.free()
        Y_d.free()
        gamma_d.free()
        beta_d.free()

        total_end.record()
        total_end.synchronize()

        kernel_time = (k1_start.time_till(k1_end)
                       + k2_start.time_till(k2_end)) / 1000
        total_time = total_start.time_till(total_end) / 1000
        return Y, kernel_time, total_time

    # ------------------------------------------------------------------
    # 3. One fused kernel
    # ------------------------------------------------------------------
    def fused(self, X, gamma, beta):
        """H2D X, gamma, beta -> fused -> D2H Y. No intermediate array."""
        C, N = X.shape
        C_u, N_u = np.uint32(C), np.uint32(N)

        total_start, total_end = cuda.Event(), cuda.Event()
        k_start, k_end = cuda.Event(), cuda.Event()
        total_start.record()

        Y_d = cuda.mem_alloc(X.nbytes)
        X_d = cuda.mem_alloc(X.nbytes)
        gamma_d = cuda.mem_alloc(gamma.nbytes)
        beta_d = cuda.mem_alloc(beta.nbytes)

        cuda.memcpy_htod(X_d, X)
        cuda.memcpy_htod(gamma_d, gamma)
        cuda.memcpy_htod(beta_d, beta)

        k_start.record()
        self.fused_kernel(Y_d, X_d, gamma_d, beta_d, C_u, N_u,
                          grid=_grid(N, C), block=self.block)
        k_end.record()

        Y = np.empty((N, C), dtype=np.float32)
        cuda.memcpy_dtoh(Y, Y_d)

        X_d.free()
        Y_d.free()
        gamma_d.free()
        beta_d.free()

        total_end.record()
        total_end.synchronize()

        kernel_time = k_start.time_till(k_end) / 1000
        total_time = total_start.time_till(total_end) / 1000
        return Y, kernel_time, total_time

    # ------------------------------------------------------------------
    # CPU reference
    # ------------------------------------------------------------------
    @staticmethod
    def cpu(X, gamma, beta):
        start = time.time()
        Y = gamma[None, :] * X.T + beta[None, :]
        return Y, time.time() - start


# ================================ HARNESS ==================================
# float32 FMA contraction on the GPU can differ from numpy's two separately
# rounded ops in the last bit, so compare with a tolerance.
RTOL = 1e-5
ATOL = 1e-6

PROFILE_C = 256
PROFILE_N = 65536                       # 64 MiB per array
NSYS_N_LADDER = [256, 4096, 65536, 1048576]


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
    print("Correctness tests (PyCUDA)")
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
    print("Benchmark sweep (PyCUDA), C fixed at 128")
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
    plt.title('Transpose + per-channel affine, C=128 (PyCUDA)')
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
    plt.savefig('bench_cuda.png', dpi=300)
    print("\nPlot saved as 'bench_cuda.png'.\n")


def run_ratio(module):
    """C*N fixed at 2^24; only the aspect ratio changes."""
    print("=" * 100)
    print("Aspect-ratio sweep (PyCUDA), C*N held fixed at 2^24")
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
    plt.title('Same total elements (C*N = 2^24), varying aspect ratio (PyCUDA)')
    plt.loglog(c_values, unf_k, 's-', label='unfused (kernel only)')
    plt.loglog(c_values, unf_t, 's--', label='unfused (total)')
    plt.loglog(c_values, fus_k, 'd-', label='fused (kernel only)')
    plt.loglog(c_values, fus_t, 'd--', label='fused (total)')
    plt.xlabel('C  (N = 2^24 / C)')
    plt.ylabel(f'Average runtime over {REPS} runs (seconds)')
    plt.legend(loc='upper left', fontsize=8)
    plt.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    plt.savefig('ratio_cuda.png', dpi=300)
    print("\nPlot saved as 'ratio_cuda.png'.\n")


def run_profile_nsys(module):
    """
    One pass of each version at every N in NSYS_N_LADDER (C = 256), so a single
    NSight Systems capture covers both the launch-overhead-dominated and the
    bandwidth-dominated regime.
    """
    print("=" * 100)
    print(f"NSight Systems run: C={PROFILE_C}, N ladder = {NSYS_N_LADDER}")
    print("=" * 100)

    rng = np.random.default_rng(2026)
    gamma = np.ascontiguousarray(rng.standard_normal(PROFILE_C), dtype=np.float32)
    beta = np.ascontiguousarray(rng.standard_normal(PROFILE_C), dtype=np.float32)

    print(f"{'N':>10} {'version':<16} {'kernel(s)':>13} {'total(s)':>13} "
          f"{'total-kernel(s)':>16} {'launches':>9}")
    print("-" * 100)

    for N in NSYS_N_LADDER:
        X = np.ascontiguousarray(
            rng.standard_normal((PROFILE_C, N)), dtype=np.float32)
        _, k1, t1 = module.unfused_hostroundtrip(X, gamma, beta)
        _, k2, t2 = module.unfused(X, gamma, beta)
        _, k3, t3 = module.fused(X, gamma, beta)

        print(f"{N:>10,} {'[1] hostroundtrip':<16} {k1:>13.6e} {t1:>13.6e} "
              f"{t1 - k1:>16.6e} {2:>9}")
        print(f"{'':>10} {'[2] unfused':<16} {k2:>13.6e} {t2:>13.6e} "
              f"{t2 - k2:>16.6e} {2:>9}")
        print(f"{'':>10} {'[3] fused':<16} {k3:>13.6e} {t3:>13.6e} "
              f"{t3 - k3:>16.6e} {1:>9}")
        print()


def run_profile_ncu(module):
    """
    unfused() and fused() once each at C=256, N=65536: exactly three kernel
    launches (transpose, affine, fused) for NSight Compute.
    """
    print("=" * 100)
    print(f"NSight Compute run: C={PROFILE_C}, N={PROFILE_N}")
    print(f"        elements = {PROFILE_C * PROFILE_N:,}"
          f"   bytes per array = {PROFILE_C * PROFILE_N * 4:,}")
    print("=" * 100)

    rng = np.random.default_rng(2026)
    X = np.ascontiguousarray(
        rng.standard_normal((PROFILE_C, PROFILE_N)), dtype=np.float32)
    gamma = np.ascontiguousarray(rng.standard_normal(PROFILE_C), dtype=np.float32)
    beta = np.ascontiguousarray(rng.standard_normal(PROFILE_C), dtype=np.float32)

    _, k2, t2 = module.unfused(X, gamma, beta)
    print(f"unfused (transpose_kernel + affine_kernel): "
          f"kernel {k2:.6e}s   total {t2:.6e}s")
    _, k3, t3 = module.fused(X, gamma, beta)
    print(f"fused   (fused_kernel)                    : "
          f"kernel {k3:.6e}s   total {t3:.6e}s")
    print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Kernel fusion: layout conversion + per-channel affine (PyCUDA)")
    parser.add_argument(
        '-m', '--mode', required=True,
        choices=['test', 'bench', 'ratio', 'profile-nsys', 'profile-ncu'])
    args = parser.parse_args()

    module = CudaFusion()
    {
        'test': run_tests,
        'bench': run_bench,
        'ratio': run_ratio,
        'profile-nsys': run_profile_nsys,
        'profile-ncu': run_profile_ncu,
    }[args.mode](module)
