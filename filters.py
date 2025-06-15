import numpy as np

def convolve(x, h):
    N = len(x)
    M = len(h)
    y = np.zeros(N + M - 1)
    for n in range(len(y)):
        for k in range(M):
            if 0 <= n - k < N:
                y[n] += h[k] * x[n - k]
    return y

def hamming_window(M):
    return 0.53836 - 0.46164 * np.cos(2 * np.pi * np.arange(M) / (M - 1))

def hanning_window(M):
    return 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(M) / (M - 1))

def blackman_window(M):
    n = np.arange(M)
    return 0.42 - 0.5 * np.cos(2 * np.pi * n / (M - 1)) + 0.08 * np.cos(4 * np.pi * n / (M - 1))

def ideal_lowpass_response(M, K):
    h = np.zeros(M)
    for n in range(M):
        if n == (M - 1) // 2:
            h[n] = 2 / K
        else:
            h[n] = np.sin(2 * np.pi * (n - (M - 1) // 2) / K) / (np.pi * (n - (M - 1) // 2))
    return h

def design_filter(M, K, window_fn, band):
    h = ideal_lowpass_response(M, K)
    window = window_fn(M)
    h *= window
    if band == 'High':
        h *= (-1) ** np.arange(M)
    return h

def apply_filter(x, h):
    return convolve(x, h)

def correlate_signals(x, y):
    y_rev = y[::-1]
    return convolve(x, y_rev)
