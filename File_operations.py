import pickle
import numpy as np
from tkinter import filedialog


def save_signal(time, signal, params, signal_type):
    file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Plik Pickle", "*.pkl")])
    if file_path:
        with open(file_path, 'wb') as f:
            pickle.dump((time, signal, params, signal_type), f)
        print(f"Sygnał zapisany do {file_path}")


def load_signal():
    file_path = filedialog.askopenfilename(defaultextension=".pkl", filetypes=[("Plik Pickle", "*.pkl")])
    if file_path:
        with open(file_path, 'rb') as f:
            time, signal, params, signal_type = pickle.load(f)
        print(f"Sygnał wczytany z {file_path}")
        return time, signal, params, signal_type
    else:
        return None, None, None, None


def add_signals(time1, signal1, params1, signal_type1, time2, signal2, params2, signal_type2):
    if len(time1) != len(time2):
        print("Błąd: Czas sygnałów musi być taki sam")
        return None, None, None, None
    result_signal = np.add(signal1, signal2)
    return time1, result_signal


def subtract_signals(time1, signal1, params1, signal_type1, time2, signal2, params2, signal_type2):
    if len(time1) != len(time2):
        print("Błąd: Czas sygnałów musi być taki sam")
        return None, None, None, None
    result_signal = np.subtract(signal1, signal2)
    return time1, result_signal


def multiply_signals(time1, signal1, params1, signal_type1, time2, signal2, params2, signal_type2):
    if len(time1) != len(time2):
        print("Błąd: Czas sygnałów musi być taki sam")
        return None, None, None, None
    result_signal = np.multiply(signal1, signal2)
    return time1, result_signal


def divide_signals(time1, signal1, params1, signal_type1, time2, signal2, params2, signal_type2):
    if len(time1) != len(time2):
        print("Błąd: Czas sygnałów musi być taki sam")
        return None, None, None, None
    if not np.allclose(time1, time2):
        print("Błąd: Czas sygnałów musi być dokładnie taki sam")
        return None, None, None, None

    result_signal = np.divide(signal1, signal2, where=signal2 != 0)
    result_signal[signal2 == 0] = 0
    return time1, result_signal
