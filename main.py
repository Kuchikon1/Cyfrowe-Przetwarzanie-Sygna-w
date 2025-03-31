import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Frame, StringVar, ttk, Entry, Button, Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import File_operations as fo
import Signal_operations as so
import Signal_functions as sf
from Dictionary import signal_map, param_entries, param_abbreviations, signal_params_map

def get_full_param_name(abbreviation):
    return next((name for name, abbr in param_abbreviations.items() if abbr == abbreviation), abbreviation)

def update_param_fields(*args):
    for widget in param_frame.winfo_children():
        widget.destroy()

    param_entries.clear()

    signal_type = [key for key, value in signal_map.items() if value == signal_var.get()]
    if not signal_type:
        return

    signal_type = signal_type[0]
    active_params = signal_params_map.get(signal_type, [])

    label_width = 32
    entry_width = 32

    for param in active_params:
        full_param_name = get_full_param_name(param)
        frame = Frame(param_frame)
        frame.pack(anchor="w")
        Label(frame, text=full_param_name, anchor="w", width=label_width).pack(fill="x")
        entry = Entry(frame, width=entry_width, justify="left")
        entry.pack(fill="x")
        param_entries[full_param_name] = entry

def generate_signal(signal_type):
    params = {full_name: float(param_entries[full_name].get()) for full_name in param_entries}

    par = {}
    for full_param, value in params.items():
        abbreviation = param_abbreviations.get(full_param, full_param)
        par[abbreviation] = value

    if signal_type == "S1":
        t, signal, d, t1 = sf.szum_o_rozkładzie_jednostajnym(par['A'], par['t1'], par['d'])
    elif signal_type == "S2":
        t, signal, d, t1 = sf.szum_gaussowski(par['A'], par['t1'], par['d'])
    elif signal_type == "S3":
        t, signal, d, t1 = sf.sygnal_sinusoidalny(par['A'], par['T'], par['t1'], par['d'])
    elif signal_type == "S4":
        t, signal, d, t1 = sf.sygnal_sinusoidalny_wyprosotowany_jednopolowkowo(par['A'], par['T'], par['t1'], par['d'])
    elif signal_type == "S5":
        t, signal, d, t1 = sf.sygnal_sinusoidalny_wyprosotowany_dwupolowkowo(par['A'], par['T'], par['t1'], par['d'])
    elif signal_type == "S6":
        t, signal, d, t1 = sf.sygnal_prostokatny(par['A'], par['T'], par['t1'], par['d'], par['kw'])
    elif signal_type == "S7":
        t, signal, d, t1 = sf.sygnal_prostokatny_symetryczny(par['A'], par['T'], par['t1'], par['d'], par['kw'])
    elif signal_type == "S8":
        t, signal, d, t1 = sf.sygnal_trojkatny(par['A'], par['T'], par['t1'], par['d'], par['kw'])
    elif signal_type == "S9":
        t, signal, d, t1 = sf.skok_jednostkowy(par['A'], par['t1'], par['d'], par['ts'])
    elif signal_type == "S10":
        t, signal, d = sf.impuls_jednostkowy(par['A'], par['ns'], par['n1'], par['d'], par['f'])
    elif signal_type == "S11":
        t, signal, d = sf.szum_impulsowy(par['A'], par['t1'], par['d'], par['f'], par['p'])
    else:
        raise ValueError("Nieznany typ sygnału")

    return t, signal, d


def plot_signal(ax, time, signal, signal_type, title="Wykres sygnału"):
    ax.clear()
    if signal_type in ["S10", "S11"]:
        ax.scatter(time, signal, label="Sygnał", color='blue')
    else:
        ax.plot(time, signal, label="Sygnał")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("Amplituda")
    ax.set_title(title)
    ax.legend()
    ax.grid()


def plot_histogram(ax, signal, title="Histogram sygnału", bins=10):
    ax.clear()

    A_min = np.min(signal)
    A_max = np.max(signal)

    bin_width = (A_max - A_min) / (bins - 1)
    bin_centers = np.linspace(A_min, A_max, bins)
    bin_edges = np.concatenate(([A_min - bin_width / 2], bin_centers + bin_width / 2))

    n, _, patches = ax.hist(signal, bins=bin_edges, alpha=0.75, color='blue', edgecolor='black', linewidth=1.2)

    ax.set_xticks(bin_centers)
    ax.set_xticklabels([f"{center:.2f}" for center in bin_centers], rotation=45)

    for i in range(len(n)):
        ax.text(bin_centers[i], n[i] + 0.5, f'{int(n[i])}', ha='center', va='bottom', fontsize=10)

    ax.set_xlabel("Amplituda")
    ax.set_ylabel("Liczność")
    ax.set_title(title)


def calculate_signal_parameters(t, signal, d, signal_type):
    if signal_type in ["S10", "S11"]:
        mean_value = np.mean(signal)
        mean_abs_value = np.mean(np.abs(signal))
        mean_power = np.mean(signal ** 2)
        variance = np.var(signal)

        effective_signal = np.sqrt(mean_power)
    else:
        mean_value = np.trapz(signal, t) / d
        mean_abs_value = np.trapz(np.abs(signal), t) / d
        mean_power = np.trapz(signal**2, t) / d
        variance = np.trapz((signal - np.mean(signal))**2, t) / d

        effective_signal = np.sqrt(mean_power)

        full_periods_count = int(np.floor(t[-1]))

        if full_periods_count > 0:
            start_index = int((t[-1] - full_periods_count) * len(t) / t[-1])
            t_filtered = t[start_index:]
            signal_filtered = signal[start_index:]

            mean_value = np.trapz(signal_filtered, t_filtered) / d
            mean_abs_value = np.trapz(np.abs(signal_filtered), t_filtered) / d
            mean_power = np.trapz(signal_filtered**2, t_filtered) / d
            variance = np.trapz((signal_filtered - np.mean(signal_filtered))**2, t_filtered) / d
            effective_signal = np.sqrt(mean_power)

    return mean_value, mean_abs_value, effective_signal, variance, mean_power


def update_plot():
    full_signal_name = signal_var.get()
    signal_type = [key for key, value in signal_map.items() if value == full_signal_name][0]
    bins = int(bins_var.get())

    time, signal, d = generate_signal(signal_type)
    mean_value, mean_abs_value, rms_value, variance, mean_power = calculate_signal_parameters(time, signal, d, signal_type)

    params_text = (
        f"Wartość średnia: {mean_value:.4f}\n"
        f"Wartość średnia bezwzględna: {mean_abs_value:.4f}\n"
        f"Wartość skuteczna (RMS): {rms_value:.4f}\n"
        f"Wariancja: {variance:.4f}\n"
        f"Moc średnia: {mean_power:.4f}"
    )
    params_label.config(text=params_text)

    if signal_type in ["S10", "S11"]:
        plot_signal(ax1, time, signal, signal_type, f"Wykres {signal_type} - Sygnał")
        plot_histogram(ax2, signal, f"Histogram {signal_type}", bins)
    else:
        plot_signal(ax1, time, signal, signal_type, f"Sygnał {signal_type}")
        plot_histogram(ax2, signal, f"Histogram {signal_type}", bins)
    canvas.draw()


def on_save():
    full_signal_name = signal_var.get()
    signal_type = next((key for key, value in signal_map.items() if value == full_signal_name), None)

    if not signal_type:
        print(f"Błąd: Nieznany sygnał '{full_signal_name}'")
        return

    time, signal, d = generate_signal(signal_type)
    params = {abbr: float(entry.get()) for abbr, entry in param_entries.items()}

    fo.save_signal(time, signal, params, signal_type)


def on_load():
    time, signal, params, signal_type = fo.load_signal()

    if time is not None and signal is not None:
        signal_var.set(signal_map.get(signal_type, "Nieznany sygnał"))

        for abbr, value in params.items():
            if abbr in param_entries:
                param_entries[abbr].delete(0, "end")
                param_entries[abbr].insert(0, str(value))

        mean_value, mean_abs_value, rms_value, variance, mean_power = calculate_signal_parameters(time, signal, len(time), signal_type)

        params_text = (
            f"Wartość średnia: {mean_value:.4f}\n"
            f"Wartość średnia bezwzględna: {mean_abs_value:.4f}\n"
            f"Wartość skuteczna (RMS): {rms_value:.4f}\n"
            f"Wariancja: {variance:.4f}\n"
            f"Moc średnia: {mean_power:.4f}"
        )
        params_label.config(text=params_text)

        if signal_type in ["S10", "S11"]:
            plot_signal(ax1, time, signal, signal_type, f"Wczytany sygnał {signal_type} - Sygnał")
            plot_histogram(ax2, signal, f"Histogram wczytanego wykresu {signal_type}", 10)
        else:
            plot_signal(ax1, time, signal, signal_type, f"Wczytany sygnał {signal_type}")
            plot_histogram(ax2, signal, f"Histogram wczytanego sygnału {signal_type}", 10)
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

Label(frame_bottom, text="Liczba słupków na histogramie:").pack(side="top", padx=10)
bins_var = StringVar(value="10")
bins_entry = Entry(frame_bottom, textvariable=bins_var, width=35)
bins_entry.pack(side="top", padx=10, pady=5)

Button(frame_bottom, text="Generuj", command=update_plot, font=("Arial", 12)).pack(side="top", padx=5, pady=10)

params_label = Label(frame_bottom, text="Wartość średnia: 0.0000\n"
                                           "Wartość średnia bezwzględna: 0.0000\n"
                                           "Wartość skuteczna (RMS): 0.0000\n"
                                           "Wariancja: 0.0000\n"
                                           "Moc średnia: 0.0000", font=("Arial", 10))
params_label.pack(side="top", padx=10)

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