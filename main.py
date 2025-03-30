import numpy as np
import matplotlib.pyplot as plt
import pickle
from tkinter import Tk, Frame, StringVar, ttk, Entry, Button, Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import File_operations as fo

signal_map = {
    "S1": "Szum o rozkładzie jednostajnym",
    "S2": "Szum Gaussowski",
    "S3": "Sygnał sinusoidalny",
    "S4": "Sygnał sin. wyprostowany jednopołówkowo",
    "S5": "Sygnał sin. wyprostowany dwupołówkowo",
    "S6": "Sygnał prostokątny",
    "S7": "Sygnał prostokątny symetryczny",
    "S8": "Sygnał trójkątny",
    "S9": "Skok jednostkowy",
    "S10": "Impuls jednostkowy",
    "S11": "Szum impulsowy"
}

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

def plot_signal(ax, time, signal, signal_type, title="Wykres sygnału"):
    ax.clear()
    if signal_type in ["S9", "S10", "S11"]:
        ax.scatter(time, signal, label="Sygnał", color='red', marker='o')
    else:
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

def calculate_signal_parameters(t, signal, frequency):
    mean_value = np.mean(signal)
    mean_abs_value = np.mean(np.abs(signal))
    rms_value = np.sqrt(np.mean(signal**2))
    variance = np.var(signal)
    mean_power = np.mean(signal**2)
    period = 1 / frequency
    full_periods_count = int(np.floor(t[-1] / period))

    if full_periods_count > 0:
        start_index = int((t[-1] - full_periods_count * period) * len(t) / t[-1])
        t_filtered = t[start_index:]
        signal_filtered = signal[start_index:]

        mean_value = np.mean(signal_filtered)
        mean_abs_value = np.mean(np.abs(signal_filtered))
        rms_value = np.sqrt(np.mean(signal_filtered**2))
        variance = np.var(signal_filtered)
        mean_power = np.mean(signal_filtered**2)

    return mean_value, mean_abs_value, rms_value, variance, mean_power

def update_plot():
    full_signal_name = signal_var.get()
    signal_type = [key for key, value in signal_map.items() if value == full_signal_name][0]

    frequency = float(freq_var.get())
    amplitude = float(amplitude_var.get())
    duration = float(duration_var.get())
    sampling_rate = int(sampling_var.get())
    bins = int(bins_var.get())

    time, signal = generate_signal(signal_type, frequency, amplitude, duration, sampling_rate)
    mean_value, mean_abs_value, rms_value, variance, mean_power = calculate_signal_parameters(time, signal, frequency)

    params_text = (
        f"Wartość średnia: {mean_value:.4f}\n"
        f"Wartość średnia bezwzględna: {mean_abs_value:.4f}\n"
        f"Wartość skuteczna (RMS): {rms_value:.4f}\n"
        f"Wariancja: {variance:.4f}\n"
        f"Moc średnia: {mean_power:.4f}"
    )
    params_label.config(text=params_text)

    plot_signal(ax1, time, signal, signal_type, f"Sygnał {signal_type}")
    plot_histogram(ax2, signal, f"Histogram {signal_type}", bins)
    canvas.draw()

def on_save():
    full_signal_name = signal_var.get()
    signal_type = [key for key, value in signal_map.items() if value == full_signal_name]

    if not signal_type:
        print(f"Błąd: Nieznany sygnał '{full_signal_name}'")
        return

    signal_type = signal_type[0]
    frequency = float(freq_var.get())
    amplitude = float(amplitude_var.get())
    duration = float(duration_var.get())
    sampling_rate = int(sampling_var.get())

    time, signal = generate_signal(signal_type, float(freq_var.get()), float(amplitude_var.get()),
                                   float(duration_var.get()), int(sampling_var.get()))
    fo.save_signal(time, signal, frequency, amplitude, duration, sampling_rate, signal_type)

def on_load():
    time, signal, frequency, amplitude, duration, sampling_rate, signal_type = fo.load_signal()
    if time is not None and signal is not None:
        freq_var.set(f"{frequency}")
        amplitude_var.set(f"{amplitude}")
        duration_var.set(f"{duration}")
        sampling_var.set(f"{sampling_rate}")
        bins_var.set("10")

        if signal_type in signal_map:
            signal_var.set(signal_map[signal_type])

        mean_value, mean_abs_value, rms_value, variance, mean_power = calculate_signal_parameters(time, signal,
                                                                                                  frequency)
        params_text = (
            f"Wartość średnia: {mean_value:.4f}\n"
            f"Wartość średnia bezwzględna: {mean_abs_value:.4f}\n"
            f"Wartość skuteczna (RMS): {rms_value:.4f}\n"
            f"Wariancja: {variance:.4f}\n"
            f"Moc średnia: {mean_power:.4f}"
        )
        params_label.config(text=params_text)

        plot_signal(ax1, time, signal, signal_type, "Wczytany sygnał")
        plot_histogram(ax2, signal, "Histogram wczytanego sygnału", 10)
        canvas.draw()


# Funkcje do operacji na sygnałach
def on_add():
    time1, signal1 = fo.load_signal()
    time2, signal2 = fo.load_signal()
    if time1 is not None and time2 is not None:
        time, result_signal = fo.add_signals(time1, signal1, time2, signal2)
        if time is not None:
            fo.save_signal(time, result_signal)

def on_subtract():
    time1, signal1 = fo.load_signal()
    time2, signal2 = fo.load_signal()
    if time1 is not None and time2 is not None:
        time, result_signal = fo.subtract_signals(time1, signal1, time2, signal2)
        if time is not None:
            fo.save_signal(time, result_signal)

def on_multiply():
    time1, signal1 = fo.load_signal()
    time2, signal2 = fo.load_signal()
    if time1 is not None and time2 is not None:
        time, result_signal = fo.multiply_signals(time1, signal1, time2, signal2)
        if time is not None:
            fo.save_signal(time, result_signal)

def on_divide():
    time1, signal1 = fo.load_signal()
    time2, signal2 = fo.load_signal()
    if time1 is not None and time2 is not None:
        time, result_signal = fo.divide_signals(time1, signal1, time2, signal2)
        if time is not None:
            fo.save_signal(time, result_signal)


# Tworzenie GUI
root = Tk()
root.title("Generator Sygnałów")

frame_buttons = Frame(root)
frame_buttons.pack(side="top", anchor="w", padx=10, pady=10)

frame_controls = Frame(root)
frame_controls.pack(side="left", padx=10, pady=10)

frame_plot = Frame(root)
frame_plot.pack(side="right", padx=10, pady=10)

# Wybór sygnału
signal_var = StringVar(value="")
Label(frame_controls, text="Wybierz sygnał").pack()
signal_names = list(signal_map.values())
signal_menu = ttk.Combobox(frame_controls, textvariable=signal_var, values=signal_names, width=40)
signal_menu.pack()

# Parametry sygnału
freq_var = StringVar(value="0")
amplitude_var = StringVar(value="0")
duration_var = StringVar(value="0")
sampling_var = StringVar(value="0")
bins_var = StringVar(value="0")

Label(frame_controls, text="Częstotliwość (Hz)").pack()
Entry(frame_controls, textvariable=freq_var, width=40).pack()

Label(frame_controls, text="Amplituda").pack()
Entry(frame_controls, textvariable=amplitude_var, width=40).pack()

Label(frame_controls, text="Czas trwania (s)").pack()
Entry(frame_controls, textvariable=duration_var, width=40).pack()

Label(frame_controls, text="Próbkowanie (Hz)").pack()
Entry(frame_controls, textvariable=sampling_var, width=40).pack()

Label(frame_controls, text="Liczba przedziałów histogramu").pack()
Entry(frame_controls, textvariable=bins_var, width=40).pack()

Button(frame_controls, text="Generuj", command=update_plot, font=("Arial", 10), width=15, height=2).pack(pady=10)

# Dodanie przycisków "Zapisz" i "Wczytaj"
Button(frame_buttons, text="Zapisz sygnał", command=on_save).pack(side="left", padx=5)
Button(frame_buttons, text="Wczytaj sygnał", command=on_load).pack(side="left", padx=5)

Button(frame_buttons, text="Dodaj sygnały", command=on_add).pack(side="left", padx=5)
Button(frame_buttons, text="Odejmij sygnały", command=on_subtract).pack(side="left", padx=5)
Button(frame_buttons, text="Pomnóż sygnały", command=on_multiply).pack(side="left", padx=5)
Button(frame_buttons, text="Podziel sygnały", command=on_divide).pack(side="left", padx=5)

# Wykresy
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
plt.subplots_adjust(hspace=0.4)
canvas = FigureCanvasTkAgg(fig, master=frame_plot)
canvas.get_tk_widget().pack()

params_label = Label(frame_controls, text="Wartość średnia: 0.0000\n"
                                              "Wartość średnia bezwzględna: 0.0000\n"
                                              "Wartość skuteczna (RMS): 0.0000\n"
                                              "Wariancja: 0.0000\n"
                                              "Moc średnia: 0.0000")
params_label.pack(padx=10, pady=10)

root.mainloop()