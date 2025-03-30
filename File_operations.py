import pickle
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