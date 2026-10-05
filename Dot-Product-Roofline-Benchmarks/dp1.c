#include <stdio.h>
#include <stdlib.h> 
#include <time.h>

float dp(long N, float *pA, float *pB) {
    float R = 0.0;
    int j;
    for (j=0;j<N;j++){
        R += pA[j]*pB[j];
    }
    return R;
}

int main(int argc, char **argv){

    char **endPtr = NULL;
    long N = strtoul(argv[1], endPtr, 10);
    long reps = strtoul(argv[2], endPtr, 10);
    double T = 0.0, B = 0.0, F = 0.0;
    float *pA = malloc(N * sizeof(float));
    float *pB = malloc(N * sizeof(float));
    volatile float dot_product = 0.0;
    struct timespec start, end;

    if (pA == NULL || pB == NULL) {
        fprintf(stderr, "Fatal: failed to allocate bytes.\n");
        return 1;
    }
    
    for (long idx=0; idx<N; idx++){
        pA[idx] = 1.0;
        pB[idx] = 1.0;
    }
    
    for (int idx=0; idx<reps; idx++){
        clock_gettime(CLOCK_MONOTONIC, &start);
        dot_product = dp(N, pA, pB);
        clock_gettime(CLOCK_MONOTONIC, &end);
        if (idx >= reps / 2){
            T += (end.tv_sec + end.tv_nsec / 1e9) - (start.tv_sec + start.tv_nsec / 1e9);
        }
    }
    T /= reps / 2;
    B = (8 * N) / T;
    B /= 1e9;
    F = (2 * N) / T;

    printf("N: %ld <T>: %.6f sec B: %.3f GB/sec F: %.3f FLOP/sec\n", N, T, B, F);
    printf("R: %.6f\n", (float)dot_product);
    
    free(pA);
    free(pB);
    return 0;
}