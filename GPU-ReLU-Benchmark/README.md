# Kernel Fusion on the GPU: Layout Conversion + Per-Channel Affine

## Abstract

This project implements a fused layout conversion and per-channel affine transform (`Y[n, c] = gamma[c] * X[c, n] + beta[c]`) in both CUDA (via PyCUDA) and OpenCL (via PyOpenCL). It converts a channel-major `(C, N)` tensor to batch-major `(N, C)` while applying a folded BatchNorm scale and shift. Three implementations are compared against a NumPy CPU baseline:

- **Host round trip:** two kernels (transpose, then affine), with the intermediate copied back to the host and up again in between
- **Unfused:** the same two kernels, with the intermediate kept in device global memory
- **Fused:** one kernel, with no intermediate array

Kernel-only and end-to-end times are measured separately, and the PyCUDA versions are profiled with Nsight Systems and Nsight Compute. Fusion cuts kernel time by 1.62× at large N and halves DRAM traffic (138 MB vs. 264 MB measured, against 134 MB vs. 268 MB predicted). End-to-end, though, host transfers dominate: they account for over 95% of the total, so the fused and unfused versions finish within about 1% of each other, and only the PyCUDA versions catch up with NumPy at N = 10⁶. Profiling also shows that fusion does not fix the transpose's strided store, which runs at 12.5% global store efficiency in both the transpose and fused kernels.

The full analysis is in the [report](report.pdf). It covers launch structure, the launch-overhead crossover, predicted vs. measured DRAM bytes, warp-level coalescing, and the aspect-ratio sweep.

## Experimental setup

| Item | Value |
|---|---|
| GPU | 1× NVIDIA L4 (Ada Lovelace, 24 GB GDDR6, 300 GB/s peak) |
| Machine type | GCP g2-standard-4 (4 vCPUs, 16 GB RAM) |
| OS | Ubuntu 22.04 LTS |
| Disk | 50 GB persistent |
| Zone | us-central1-c |

### Software stack

| Component | Version / details |
|---|---|
| CUDA Toolkit | 12.6.1 (includes `nvcc`) |
| NVIDIA driver | 560.35.03 (bundled with the CUDA 12.6.1 runfile installer) |
| Profilers | Nsight Systems 2024.4.2.133, Nsight Compute 2024.3.1.0 |
| Python | Python 3.10 in an isolated `venv` |
| GPU libraries | `pycuda`, `pyopencl` (OpenCL via the NVIDIA CUDA platform) |
| Python packages | `numpy`, `matplotlib` |

### Environment setup

1. Install build essentials (`build-essential`, `dkms`). Make sure the system GCC matches the kernel's GCC (check with `cat /proc/version`).
2. Install CUDA Toolkit 12.6.1 with NVIDIA's runfile installer. Verify the driver with `nvidia-smi`.
3. Add `/usr/local/cuda-12.6/bin` to `PATH` and the CUDA `lib` directory to `LD_LIBRARY_PATH`. Confirm with `nvcc --version`.
4. Enable profiler access to the GPU performance counters. Either set `NVreg_RestrictProfilingToAdminUsers=0` in `/etc/modprobe.d/` and reboot, or run Nsight Compute through `sudo env "PATH=$PATH" "LD_LIBRARY_PATH=$LD_LIBRARY_PATH" ncu ...`.
5. Create and activate a virtual environment, then install the dependencies:
   ```bash
   python3 -m venv cuda_cl && source cuda_cl/bin/activate
   pip install numpy matplotlib pycuda pyopencl
   ```
6. Confirm both runtimes can see the GPU. Query `cuda.Device(0).name()` in PyCUDA and list the devices under `cl.get_platforms()` in PyOpenCL.

Nsight Compute 2024.3 supports Volta and newer GPUs only, so Pascal cards such as the Tesla P4 cannot be profiled with it.

### Benchmark methodology

- **Benchmark sweep:** C = 128, N = 10¹ to 10⁶, float32, each time averaged over 5 runs.
- **Aspect-ratio sweep:** C·N fixed at 2²⁴ (64 MiB per array), C = 32 to 32,768, averaged over 5 runs.
- **Block size:** 32 × 32 for every kernel. The transpose and fused kernels map `n` to `threadIdx.x`; the affine kernel maps `c` to `threadIdx.x`.
- **PyCUDA timing:** CUDA events for both kernel-only and end-to-end time.
- **PyOpenCL timing:** OpenCL event profiling for kernel time and `time.time()` for end-to-end time.
- **End-to-end** includes device allocation, the host-to-device copies, the kernel(s), and the device-to-host copy.
- **Profiling:** Nsight Systems over C = 256 with N = 256, 4,096, 65,536 and 1,048,576 in one capture; Nsight Compute on the three kernels at C = 256, N = 65,536.
- **Correctness:** checked against NumPy with `np.allclose(rtol=1e-5, atol=1e-6)` for edge cases, including C or N = 1, dimensions that are not multiples of 32 (37 × 53, 33 × 1,025), both extreme aspect ratios, scale-only and shift-only parameters, and a 128 × 100,000 input.

## Results

### Benchmark sweep, PyCUDA (seconds, C = 128)

| N | Host round trip kernel | Host round trip total | Unfused kernel | Unfused total | Fused kernel | Fused total | CPU |
|---|---|---|---|---|---|---|---|
| 10¹ | 1.200e-04 | 5.049e-04 | 4.813e-05 | 3.007e-04 | 2.888e-05 | 2.460e-04 | 3.371e-05 |
| 10² | 6.614e-05 | 4.364e-04 | 5.448e-05 | 3.217e-04 | 3.092e-05 | 2.897e-04 | 5.050e-05 |
| 10³ | 5.342e-05 | 9.070e-04 | 5.714e-05 | 5.395e-04 | 4.137e-05 | 5.598e-04 | 2.440e-04 |
| 10⁴ | 1.261e-04 | 6.403e-03 | 1.468e-04 | 3.249e-03 | 1.028e-04 | 2.867e-03 | 1.487e-03 |
| 10⁵ | 1.053e-03 | 7.061e-02 | 1.078e-03 | 3.575e-02 | 6.930e-04 | 3.582e-02 | 3.579e-02 |
| 10⁶ | 1.028e-02 | 6.610e-01 | 1.029e-02 | 3.406e-01 | 6.349e-03 | 3.370e-01 | 3.547e-01 |

![PyCUDA benchmark](results/bench_cuda.png)

### Benchmark sweep, PyOpenCL (seconds, C = 128)

| N | Host round trip kernel | Host round trip total | Unfused kernel | Unfused total | Fused kernel | Fused total | CPU |
|---|---|---|---|---|---|---|---|
| 10¹ | 2.024e-05 | 1.872e-03 | 1.619e-05 | 9.901e-04 | 8.192e-06 | 5.939e-04 | 2.704e-05 |
| 10² | 1.659e-05 | 1.033e-03 | 1.696e-05 | 9.436e-04 | 8.806e-06 | 5.805e-04 | 4.973e-05 |
| 10³ | 2.007e-05 | 1.656e-03 | 2.028e-05 | 1.215e-03 | 1.534e-05 | 9.113e-04 | 2.433e-04 |
| 10⁴ | 8.786e-05 | 8.208e-03 | 8.600e-05 | 4.139e-03 | 7.558e-05 | 3.611e-03 | 1.878e-03 |
| 10⁵ | 1.032e-03 | 1.516e-01 | 1.033e-03 | 7.630e-02 | 6.427e-04 | 7.599e-02 | 3.707e-02 |
| 10⁶ | 1.022e-02 | 1.432e+00 | 1.023e-02 | 7.200e-01 | 6.303e-03 | 7.179e-01 | 3.553e-01 |

![PyOpenCL benchmark](results/bench_opencl.png)

### Aspect-ratio sweep (seconds, C·N = 2²⁴)

| C | N | PyCUDA unfused kernel | PyCUDA fused kernel | PyCUDA unfused total | PyCUDA fused total | PyOpenCL unfused kernel | PyOpenCL fused kernel | PyOpenCL unfused total | PyOpenCL fused total |
|---|---|---|---|---|---|---|---|---|---|
| 32 | 524,288 | 1.486e-03 | 8.757e-04 | 4.712e-02 | 4.512e-02 | 1.343e-03 | 8.200e-04 | 1.017e-01 | 9.835e-02 |
| 128 | 131,072 | 1.401e-03 | 8.933e-04 | 4.605e-02 | 4.628e-02 | 1.356e-03 | 8.379e-04 | 9.938e-02 | 9.881e-02 |
| 512 | 32,768 | 1.397e-03 | 8.827e-04 | 4.642e-02 | 4.540e-02 | 1.349e-03 | 8.303e-04 | 9.919e-02 | 9.781e-02 |
| 2,048 | 8,192 | 1.411e-03 | 8.987e-04 | 4.580e-02 | 4.620e-02 | 1.359e-03 | 8.407e-04 | 9.831e-02 | 9.763e-02 |
| 8,192 | 2,048 | 1.424e-03 | 9.314e-04 | 4.701e-02 | 4.521e-02 | 1.381e-03 | 8.653e-04 | 9.938e-02 | 9.836e-02 |
| 32,768 | 512 | 1.467e-03 | 9.468e-04 | 4.616e-02 | 4.631e-02 | 1.402e-03 | 8.860e-04 | 9.974e-02 | 9.902e-02 |

| PyCUDA | PyOpenCL |
|---|---|
| ![PyCUDA aspect-ratio sweep](results/ratio_cuda.png) | ![PyOpenCL aspect-ratio sweep](results/ratio_opencl.png) |

### Profiling, PyCUDA (C = 256, N = 65,536)

Nsight Systems:

| Version | Kernel launches | Total memcpy (ms) | Kernel time (ms) |
|---|---|---|---|
| Host round trip | 2 | 81.89 | 1.244 |
| Unfused | 2 | 41.39 | 1.333 |
| Fused | 1 | 42.22 | 0.818 |

The dispatch gap between the two kernels in `unfused()` is 5.7 µs.

Nsight Compute (SM clock locked at base frequency during profiling):

| Metric | Transpose | Affine | Fused |
|---|---|---|---|
| Duration (ms) | 1.71 | 0.50 | 1.72 |
| DRAM read (bytes) | 80,685,312 | 73,943,808 | 80,753,152 |
| DRAM write (bytes) | 57,306,112 | 52,368,384 | 57,339,776 |
| Global store efficiency | 12.5% | 100% | 12.5% |
| Global load efficiency | – | – | 70.8% |
| Memory throughput (GB/s) | – | – | 80.48 |

Global load and store efficiency come from `smsp__sass_average_data_bytes_per_sector_mem_global_op_{ld,st}`. Nsight Compute reports the average number of useful bytes per 32-byte sector (`.ratio`) and the maximum possible (`.max_rate` = 32), so efficiency = `.ratio` / `.max_rate`:

| Kernel | Store `.ratio` | Store efficiency | Load `.ratio` | Load efficiency |
|---|---|---|---|---|
| Transpose | 4 | 4 / 32 = 12.5% | 32 | 100% |
| Affine | 32 | 32 / 32 = 100% | 32 | 100% |
| Fused | 4 | 4 / 32 = 12.5% | 22.67 | 22.67 / 32 = 70.8% |

The fused kernel's load ratio of 22.67 is a weighted average over all its global loads. Per warp, the read from `X` moves 128 bytes in 4 sectors, while `gamma[c]` and `beta[c]` each move 4 bytes in a full sector: 136 bytes / 6 sectors = 22.67 bytes per sector.

## Attribution

This work was completed as a homework assignment for EECS E4750: Heterogeneous Computing for Signal and Data Processing at Columbia University, taught by Prof. Zoran Kostić. The assignment template, test harness, and benchmarking code were provided by the course. The CUDA and OpenCL kernels and all host code were developed by the author. This report was written with the assistance of AI; all experimental results were produced and verified by the author.

---

*Nrushad Joshi, Columbia University*
