import numpy as np
import matplotlib.pyplot as plt
import pickle
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def generate_signal(signal_type, frequency=1, amplitude=1, duration=1, sampling_rate=1000):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

    if signal_type == "S1":
        signal = np.random.uniform(-amplitude, amplitude, len(t))
    elif signal_type == "S2":
        signal = np.random.normal(0, amplitude, len(t))
    elif signal_type == "S3":
        signal = amplitude * np.sin(2 * np.pi * frequency * t)
    elif signal_type == "S4":
        signal = np.maximum(0, amplitude * np.sin(2 * np.pi * frequency * t))
    elif signal_type == "S5":
        signal = np.abs(amplitude * np.sin(2 * np.pi * frequency * t))
    elif signal_type == "S6":
        signal = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
    elif signal_type == "S7":
        signal = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
    elif signal_type == "S8":
        signal = 2 * amplitude * np.abs(t % (1 / frequency) - (1 / (2 * frequency))) - amplitude
    elif signal_type == "S9":
        signal = np.where(t >= duration / 2, amplitude, 0)
    elif signal_type == "S10":
        signal = np.zeros_like(t)
        signal[len(t) // 2] = amplitude
    elif signal_type == "S11":
        signal = np.random.choice([0, amplitude], size=len(t), p=[0.9, 0.1])
    else:
        raise ValueError("Nieznany typ sygnału")

    return t, signal


def plot_signal(ax, time, signal, title="Wykres sygnału"):
    ax.clear()
    ax.plot(time, signal, label="Sygnał")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("Amplituda")
    ax.set_title(title)
    ax.legend()
    ax.grid()


def plot_histogram(ax, signal, title="Histogram sygnału", bins=10):
    ax.clear()
    ax.hist(signal, bins=bins, alpha=0.75, color='blue', edgecolor='black')
    ax.set_xlabel("Amplituda")
    ax.set_ylabel("Liczność")
    ax.set_title(title)
    ax.grid()


def update_plot():
    signal_type = signal_var.get()
    frequency = float(freq_var.get())
    amplitude = float(amplitude_var.get())
    duration = float(duration_var.get())
    sampling_rate = int(sampling_var.get())
    bins = int(bins_var.get())

    time, signal = generate_signal(signal_type, frequency, amplitude, duration, sampling_rate)
    plot_signal(ax1, time, signal, f"Sygnał {signal_type}")
    plot_histogram(ax2, signal, f"Histogram {signal_type}", bins)
    canvas.draw()


# Tworzenie GUI
root = tk.Tk()
root.title("Generator Sygnałów")

frame_controls = tk.Frame(root)
frame_controls.pack(side=tk.LEFT, padx=10, pady=10)

frame_plot = tk.Frame(root)
frame_plot.pack(side=tk.RIGHT, padx=10, pady=10)

# Wybór sygnału
signal_var = tk.StringVar(value="")
tk.Label(frame_controls, text="Wybierz sygnał").pack()
signals = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "S11"]
signal_menu = ttk.Combobox(frame_controls, textvariable=signal_var, values=signals)
signal_menu.pack()

# Parametry sygnału
freq_var = tk.StringVar(value="0")
amplitude_var = tk.StringVar(value="0")
duration_var = tk.StringVar(value="0")
sampling_var = tk.StringVar(value="0")
bins_var = tk.StringVar(value="0")

tk.Label(frame_controls, text="Częstotliwość (Hz)").pack()
tk.Entry(frame_controls, textvariable=freq_var).pack()

tk.Label(frame_controls, text="Amplituda").pack()
tk.Entry(frame_controls, textvariable=amplitude_var).pack()

tk.Label(frame_controls, text="Czas trwania (s)").pack()
tk.Entry(frame_controls, textvariable=duration_var).pack()

tk.Label(frame_controls, text="Próbkowanie (Hz)").pack()
tk.Entry(frame_controls, textvariable=sampling_var).pack()

tk.Label(frame_controls, text="Liczba przedziałów histogramu").pack()
tk.Entry(frame_controls, textvariable=bins_var).pack()

tk.Button(frame_controls, text="Generuj", command=update_plot).pack()

# Wykresy
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=frame_plot)
canvas.get_tk_widget().pack()

root.mainloop()