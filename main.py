import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Frame, StringVar, ttk, Entry, Button, Label, NORMAL
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import File_operations as fo
import Signal_operations as so
from Dictionary import signal_map, param_entries, param_abbreviations, signal_params, signal_params_map

# Zaktualizowana funkcja do wyświetlania pełnych nazw parametrów
def get_full_param_name(abbreviation):
    return next((name for name, abbr in param_abbreviations.items() if abbr == abbreviation), abbreviation)

def update_param_fields(*args):
    # Usuwamy stare pola
    for widget in param_frame.winfo_children():
        widget.destroy()

    # Pobieramy wybrany typ sygnału
    signal_type = [key for key, value in signal_map.items() if value == signal_var.get()]
    if not signal_type:
        return

    signal_type = signal_type[0]
    active_params = signal_params_map.get(signal_type, [])

    # Ustalmy stałą szerokość dla pól
    label_width = 32
    entry_width = 32

    # Tworzymy nowe pola tylko dla aktywnych parametrów
    for param in active_params:
        full_param_name = get_full_param_name(param)
        frame = Frame(param_frame)
        frame.pack(anchor="w")
        Label(frame, text=full_param_name, anchor="w", width=label_width).pack(fill="x")
        entry = Entry(frame, width=entry_width, justify="left")
        entry.pack(fill="x")
        param_entries[full_param_name] = entry

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

    plot_signal(ax1, time, signal, f"Sygnał {signal_type}")
    plot_histogram(ax2, signal, f"Histogram {signal_type}", bins)
    canvas.draw()


def on_save():
    full_signal_name = signal_var.get()
    signal_type = [key for key, value in signal_map.items() if value == full_signal_name]

    if not signal_type:
        print(f"Błąd: Nieznany sygnał '{full_signal_name}'")
        return

    signal_type = signal_type[0]
    time, signal = generate_signal(signal_type, int(freq_var.get()), int(amplitude_var.get()),
                                   int(duration_var.get()), int(sampling_var.get()))
    fo.save_signal(time, signal, float(freq_var.get()), float(amplitude_var.get()), float(duration_var.get()), int(sampling_var.get()))


def on_load():
    time, signal, frequency, amplitude, duration, sampling_rate, signal_type = fo.load_signal()
    if time is not None and signal is not None:
        freq_var.set(f"{frequency:.0f}")
        amplitude_var.set(f"{amplitude:.0f}")
        duration_var.set(f"{duration:.0f}")
        sampling_var.set(f"{sampling_rate:.0f}")
        bins_var.set("10")

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

        plot_signal(ax1, time, signal, "Wczytany sygnał")
        plot_histogram(ax2, signal, "Histogram wczytanego sygnału", 10)
        canvas.draw()

# Tworzenie GUI
root = Tk()
root.title("Generator Sygnałów")

frame_buttons = Frame(root)
frame_buttons.pack(side="top", anchor="w", padx=10, pady=10)

frame_plot = Frame(root)
frame_plot.pack(side="right", padx=10, pady=10)

signal_var = StringVar(value="")
signal_var.trace("w", update_param_fields)

frame_controls = Frame(root)
frame_controls.pack(side="top", padx=13, pady=10)

signal_var = StringVar(value="")
signal_var.trace("w", update_param_fields)
Label(frame_controls, text="Wybierz sygnał:").pack()
signal_combo = ttk.Combobox(frame_controls, textvariable=signal_var, values=list(signal_map.values()), width=35)
signal_combo.pack()

param_frame = Frame(root)
param_frame.pack(padx=0, pady=0)

frame_bottom = Frame(root)
frame_bottom.pack(side="bottom", fill="x", padx=10, pady=10)

# Przycisk Generuj
Button(frame_bottom, text="Generuj", command=update_plot, font=("Arial", 12)).pack(side="top", padx=5, pady=10)

# Frame na wartości (średnia, RMS itd.)
params_label = Label(frame_bottom, text="Wartość średnia: 0.0000\n"
                                           "Wartość średnia bezwzględna: 0.0000\n"
                                           "Wartość skuteczna (RMS): 0.0000\n"
                                           "Wariancja: 0.0000\n"
                                           "Moc średnia: 0.0000", font=("Arial", 10))
params_label.pack(side="top", padx=10)

# Parametry sygnału
freq_var = StringVar(value="0")
amplitude_var = StringVar(value="0")
duration_var = StringVar(value="0")
sampling_var = StringVar(value="0")
bins_var = StringVar(value="0")

# Przyciski Górne
Button(frame_buttons, text="Zapisz sygnał", command=on_save).pack(side="left", padx=5)
Button(frame_buttons, text="Wczytaj sygnał", command=on_load).pack(side="left", padx=5)

Button(frame_buttons, text="Dodaj sygnały", command=so.on_add).pack(side="left", padx=(76,5))
Button(frame_buttons, text="Odejmij sygnały", command=so.on_subtract).pack(side="left", padx=5)
Button(frame_buttons, text="Pomnóż sygnały", command=so.on_multiply).pack(side="left", padx=5)
Button(frame_buttons, text="Podziel sygnały", command=so.on_divide).pack(side="left", padx=5)

# Wykresy
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
plt.subplots_adjust(hspace=0.4)
canvas = FigureCanvasTkAgg(fig, master=frame_plot)
canvas.get_tk_widget().pack()

root.mainloop()