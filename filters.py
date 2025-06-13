import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Do integracji z projektem (zaimportuj funkcje GUI)
import File_operations as fo
import Signal_operations as so
import Signal_functions as sf
from Dictionary import signal_map, signal_params_map, param_abbreviations, param_entries

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

def convolution_from_files():
    file_path1 = filedialog.askopenfilename(filetypes=[("Pliki Pickle", "*.pkl")], title="Wybierz pierwszy plik")
    if not file_path1:
        print("Nie wybrano pierwszego pliku.")
        return

    file_path2 = filedialog.askopenfilename(filetypes=[("Pliki Pickle", "*.pkl")], title="Wybierz drugi plik")
    if not file_path2:
        print("Nie wybrano drugiego pliku.")
        return

    try:
        with open(file_path1, 'rb') as f1, open(file_path2, 'rb') as f2:
            time1, signal1, _, _ = pickle.load(f1)
            time2, signal2, _, _ = pickle.load(f2)
    except Exception as e:
        print(f"Błąd podczas ładowania plików: {e}")
        return

    y = convolve(signal1, signal2)

    dt1 = time1[1] - time1[0] if len(time1) > 1 else 1
    dt2 = time2[1] - time2[0] if len(time2) > 1 else 1
    dt = min(dt1, dt2)
    t_y = np.arange(0, len(y)) * dt

    plt.figure(figsize=(10, 7))

    plt.subplot(3, 1, 1)
    plt.plot(time1, signal1)
    plt.title("Sygnał 1")

    plt.subplot(3, 1, 2)
    plt.plot(time2, signal2)
    plt.title("Sygnał 2")

    plt.subplot(3, 1, 3)
    plt.plot(t_y, y)
    plt.title("Splot sygnałów")

    plt.tight_layout()
    plt.show()

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
    return 0.53836 - 0.46164 * np.cos(2 * np.pi * np.arange(M) / M)

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

def correlate_via_convolution(x, h):
    h_rev = h[::-1]
    return convolve(x, h_rev)

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

    corr = correlate_via_convolution(echo, probe)
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

# ==============================================
# PROSTE UI DO WSTRZYKIWANIA AKTUALNEGO SYGNAŁU
# ==============================================

def set_last_signal(t, s, typ):
    global last_time, last_signal, last_type
    last_time = t
    last_signal = s
    last_type = typ

# Przykład użycia:
# set_last_signal(t, signal, signal_type) z poziomu głównego GUI projektu

# Funkcje convolution_on_last_signal() oraz radar_on_last_signal()
# można podpiąć do przycisków w głównym GUI jako dodatkowe akcje

if __name__ == "__main__":
    print("Moduł gotowy do integracji z GUI.")
