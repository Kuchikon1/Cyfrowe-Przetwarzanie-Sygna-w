import pickle
import numpy as np
from tkinter import filedialog


def save_signal(time, signal):
    file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Plik Pickle", "*.pkl")])
    if file_path:
        with open(file_path, 'wb') as f:
            pickle.dump((time, signal), f)
        print(f"Sygnał zapisany do {file_path}")


def load_signal():
    file_path = filedialog.askopenfilename(defaultextension=".pkl", filetypes=[("Plik Pickle", "*.pkl")])
    if file_path:
        with open(file_path, 'rb') as f:
            time, signal = pickle.load(f)
        print(f"Sygnał wczytany z {file_path}")
        return time, signal
    else:
        return None, None


def add_signals(time1, signal1, time2, signal2):
    if len(time1) != len(time2):
        print("Błąd: Czas sygnałów musi być taki sam")
        return None, None
    result_signal = signal1 + signal2
    return time1, result_signal

def subtract_signals(time1, signal1, time2, signal2):
    if len(time1) != len(time2):
        print("Błąd: Czas sygnałów musi być taki sam")
        return None, None
    result_signal = signal1 - signal2
    return time1, result_signal

def multiply_signals(time1, signal1, time2, signal2):
    if len(time1) != len(time2):
        print("Błąd: Czas sygnałów musi być taki sam")
        return None, None
    result_signal = signal1 * signal2
    return time1, result_signal

def divide_signals(time1, signal1, time2, signal2):
    if len(time1) != len(time2):
        print("Błąd: Czas sygnałów musi być taki sam")
        return None, None
    # Unikamy dzielenia przez zero
    result_signal = np.divide(signal1, signal2, where=signal2 != 0)
    return time1, result_signal