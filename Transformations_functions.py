import numpy as np

# ===================== F1: DFT z definicji + DIT FFT =====================

def dft(x):
    x = np.asarray(x, dtype=complex)
    N = len(x)
    X = np.zeros(N, dtype=complex)
    for k in range(N):
        for n in range(N):
            X[k] += x[n] * np.exp(-2j * np.pi * k * n / N)
    return X

def fft_dit(x):
    x = np.asarray(x, dtype=complex)
    N = x.shape[0]
    if N <= 1:
        return x
    even = fft_dit(x[::2])
    odd = fft_dit(x[1::2])
    factor = np.exp(-2j * np.pi * np.arange(N) / N)
    return np.concatenate([even + factor[:N // 2] * odd,
                           even - factor[:N // 2] * odd])

# ===================== F2: DIF FFT =====================

def fft_dif(x):
    x = np.asarray(x, dtype=complex)
    N = len(x)

    stages = int(np.log2(N))
    X = np.copy(x)

    for s in range(stages):
        m = 2 ** (stages - s)
        half_m = m // 2
        for k in range(0, N, m):
            for j in range(half_m):
                index1 = k + j
                index2 = k + j + half_m
                t = X[index1] + X[index2]
                u = (X[index1] - X[index2]) * np.exp(-2j * np.pi * j / m)
                X[index1] = t
                X[index2] = u
    bit_rev = np.arange(N).reshape(-1, 1)
    bits = np.arange(stages)
    reversed_indices = ((bit_rev >> bits) & 1).dot(1 << (stages - 1 - bits))
    return X[reversed_indices.flatten()]

# ===================== T1: DCT-II =====================

def dct(x):
    x = np.asarray(x, dtype=float)
    N = len(x)
    result = np.zeros(N)
    for k in range(N):
        sum_val = 0
        for n in range(N):
            sum_val += x[n] * np.cos(np.pi * k * (2 * n + 1) / (2 * N))
        result[k] = sum_val
    result[0] *= 1 / np.sqrt(N)
    result[1:] *= np.sqrt(2 / N)
    return result

def fct(x):
    def fast_dct2_recursive(x):
        N = len(x)
        if N == 1:
            return np.sqrt(2) * x.copy()


        # Podział sygnału na parzyste i nieparzyste elementy
        even = x[::2]
        odd = x[1::2][::-1]  # odwrotna kolejność!

        # Rekurencja
        X_even = fast_dct2_recursive(even)
        X_odd = fast_dct2_recursive(odd)

        # Obliczanie współczynników
        result = np.zeros(N)
        for k in range(N // 2):
            cos_term = np.cos(np.pi * (2 * k + 1) / (2 * N))
            result[k] = X_even[k] + cos_term * X_odd[k]
            result[N - 1 - k] = X_even[k] - cos_term * X_odd[k]

        return result

    x = np.asarray(x, dtype=float)
    N = len(x)

    result = fast_dct2_recursive(x)

    # Normalizacja (opcjonalna, jak w zwykłej DCT-II)
    result[0] *= 1 / np.sqrt(N)
    result[1:] *= np.sqrt(2 / N)
    return result

# ===================== T2: Walsh-Hadamard Transform =====================

def wht(x):
    x = np.asarray(x, dtype=float)
    N = len(x)

    X = np.copy(x)
    h = 1
    while h < N:
        for i in range(0, N, h * 2):
            for j in range(i, i + h):
                a = X[j]
                b = X[j + h]
                X[j] = a + b
                X[j + h] = a - b
        h *= 2
    return X


def fwht(x):
    h = 1
    x = x.copy()
    n = len(x)
    while h < n:
        for i in range(0, n, h * 2):
            for j in range(i, i + h):
                a = x[j]
                b = x[j + h]
                x[j] = a + b
                x[j + h] = a - b
        h *= 2
    return x

# ===================== T3: Falkowa (Wavelet, np. DB4, DB6, DB8 – 1 poziom) =====================

# Filtrowanie: db4, db6, db8 (współczynniki Daubechies znormalizowane)

db_filters = {
    "db4": np.array([
        0.4829629131445341, 0.8365163037378079,
        0.2241438680420134, -0.1294095225512604
    ]),
    "db6": np.array([
        0.332670552950, 0.806891509311, 0.459877502118,
        -0.135011020010, -0.085441273882, 0.035226291882
    ]),
    "db8": np.array([
        0.230377813309, 0.714846570553, 0.630880767930,
        -0.027983769417, -0.187034811719, 0.030841381836,
        0.032883011667, -0.010597401785
    ])
}

def wavelet_transform(signal, wavelet='db4'):
    signal = np.asarray(signal, dtype=float)
    h = db_filters[wavelet]  # Low-pass (approximation)
    l = len(h)

    # High-pass (detail) - quadrature mirror filter
    g = h[::-1].copy()
    g[::2] *= -1

    # Padding signal symetrycznie
    padded = np.pad(signal, (l//2, l//2), mode='symmetric')

    approx = []
    detail = []

    for i in range(0, len(signal), 2):
        a = np.dot(padded[i:i + l], h)
        d = np.dot(padded[i:i + l], g)
        approx.append(a)
        detail.append(d)

    return np.array(approx), np.array(detail)

def wavelet_fast_transform(signal):
    signal = np.array(signal, dtype=float)
    n = len(signal)


    output = []
    current = signal.copy()

    while len(current) > 1:
        approx = (current[::2] + current[1::2]) / np.sqrt(2)
        detail = (current[::2] - current[1::2]) / np.sqrt(2)
        output.insert(0, detail)  # szczegóły w odwrotnej kolejności
        current = approx

    output.insert(0, current)  # ostatnie przybliżenie na początek
    return np.concatenate(output)


# def fourier_fft(time, signal, N=None):
#     signal = np.asarray(signal, dtype=float)
#     dt = time[1] - time[0]
#     if N is None:
#         N = len(signal)
#     spectrum = np.fft.fft(signal, n=N)
#     freq = np.fft.fftfreq(N, d=dt)
#     magnitude = np.abs(spectrum)
#     phase = np.angle(spectrum)
#     return freq, magnitude, phase
#
#
# def fourier_ifft(spectrum_complex, N=None):
#     return np.fft.ifft(spectrum_complex, n=N)

