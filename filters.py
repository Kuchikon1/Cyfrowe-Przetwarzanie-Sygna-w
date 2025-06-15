import numpy as np
import matplotlib.pyplot as plt

# Globalne zmienne do przechowywania sygnału
last_signal = None
last_time = None
last_type = None

# ==============================================
# CZESC 1: SPLOT DYSKRETNY
# ==============================================
def convolve(x, h):
    N = len(x)
    M = len(h)
    y = np.zeros(N + M - 1)
    for n in range(len(y)):
        for k in range(M):
            if 0 <= n - k < N:
                y[n] += h[k] * x[n - k]
    return y

def convolution_on_last_signal():
    global last_signal
    if last_signal is None:
        print("Brak sygnału do przetworzenia.")
        return

    h = np.ones(5) / 5  # filtr uśredniający
    y = convolve(last_signal, h)

    plt.figure(figsize=(10, 6))
    plt.subplot(3, 1, 1)
    plt.plot(last_signal)
    plt.title("Oryginalny sygnał")
    plt.subplot(3, 1, 2)
    plt.stem(h)
    plt.title("Filtr h[n]")
    plt.subplot(3, 1, 3)
    plt.plot(y)
    plt.title("Splot sygnału z filtrem")
    plt.tight_layout()
    plt.show()

# ==============================================
# CZESC 2: FILTRACJA (pozostaje bez zmian)
# ==============================================

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

def design_filter(M, K, window_fn=hamming_window, band='low'):
    h = ideal_lowpass_response(M, K)
    window = window_fn(M)
    h *= window
    if band == 'high':
        h *= (-1) ** np.arange(M)
    return h

def apply_filter(x, h):
    return convolve(x, h)

# ==============================================
# CZESC 3: KORELACJA I SYMULACJA RADARU
# ==============================================

def correlate_signals(x, y):
    y_rev = y[::-1]
    return convolve(x, y_rev)

def radar_on_last_signal():
    global last_signal, last_time
    if last_signal is None:
        print("Brak sygnału do analizy radarowej.")
        return

    probe = last_signal
    fs = int(1 / (last_time[1] - last_time[0]))
    N = len(probe)
    t = np.arange(N) / fs
    delay_samples = 30
    echo = np.roll(probe, delay_samples)
    echo[:delay_samples] = 0
    echo += 0.4 * np.random.randn(N)

    corr = correlate_signals(echo, probe)
    max_idx = np.argmax(corr)
    estimated_delay = max_idx - len(probe) + 1

    plt.figure(figsize=(12, 6))
    plt.subplot(3, 1, 1)
    plt.plot(t, probe)
    plt.title("Sygnał sondujący (z GUI)")
    plt.subplot(3, 1, 2)
    plt.plot(t, echo)
    plt.title("Sygnał odbity (symulowany)")
    plt.subplot(3, 1, 3)
    plt.plot(corr)
    plt.axvline(max_idx, color='red', linestyle='--', label=f'Max @ {estimated_delay} próbek')
    plt.legend()
    plt.title("Korelacja – detekcja opóźnienia")
    plt.tight_layout()
    plt.show()

def set_last_signal(t, s, typ):
    global last_time, last_signal, last_type
    last_time = t
    last_signal = s
    last_type = typ
