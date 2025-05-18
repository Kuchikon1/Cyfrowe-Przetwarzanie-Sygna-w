from tkinter import Toplevel, Frame, Button, Label, Entry, StringVar, OptionMenu, Checkbutton, BooleanVar
import File_operations as fo
import Conversion_operations as co
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def get_full_param_name(abbreviation, pool):
    return next((name for name, abbr in pool.items() if abbr == abbreviation), abbreviation)


def plot_signal(ax, time, signal, signal_type, title="Wykres sygnału"):
    ax.clear()

    if signal_type in ["S10", "S11"]:
        ax.scatter(time, signal, label="Sygnał", color='blue')
    else:
        # Rysuj punkty dla próbkowania i kwantyzacji
        if "Po próbkowaniu" in title or "Kwantyzacja" in title:
            ax.scatter(time, signal, label="Sygnał", color='blue')

            # Jeśli to kwantyzacja, dodaj poziome linie
            if "Kwantyzacja" in title:
                import re
                # Wyciągnij L z tytułu
                match = re.search(r"L=(\d+)", title)
                if match:
                    L = int(match.group(1))
                    ymin = np.min(signal)
                    ymax = np.max(signal)
                    levels = np.linspace(ymin, ymax, L)
                    for level in levels:
                        ax.axhline(level, color='red', linestyle='--', alpha=0.5)

        else:
            ax.plot(time, signal, label="Sygnał")

    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("Amplituda")
    ax.set_title(title)
    ax.legend()
    ax.grid()

def create_conversion_window(root, title, signal_var, conversion_param_entries, on_save, on_load, param_names=[]):
    new_window = Toplevel(root)
    new_window.title(title)
    new_window.geometry("1200x500")

    frame_buttons = Frame(new_window)
    frame_buttons.pack(side="top", anchor="nw", padx=10, pady=10)

    def save_signal_window():
        if hasattr(new_window, "signal_data"):
            time, signal, signal_type = new_window.signal_data
            params = {key: entry.get() for key, entry in conversion_param_entries.items()}
            fo.save_signal(time, signal, params, signal_type)
        else:
            print("Brak danych sygnału do zapisania.")

    def load_signal_window():
        data = on_load()
        if data is None:
            return
        time_l, signal_l, params_l, signal_type_l = data
        new_window.signal_data = (time_l, signal_l, signal_type_l)
        new_window.original_data = (time_l, signal_l)  # DODAJ TO
        plot_signal(ax, time_l, signal_l, signal_type_l, f"Wczytany sygnał {signal_type_l}")
        canvas.draw()

    Button(frame_buttons, text="Zapisz sygnał", command=save_signal_window).pack(side="left", padx=(0, 5))
    Button(frame_buttons, text="Wczytaj sygnał", command=load_signal_window).pack(side="left")

    frame_main = Frame(new_window)
    frame_main.pack(fill="both", expand=True, padx=10, pady=10)

    frame_params = Frame(frame_main)
    frame_params.pack(side="left", fill="y")

    label_width = 35
    entry_width = 37
    conversion_param_entries.clear()

    # === Wybór typu konwersji ===
    Label(frame_params, text="Typ konwersji:", anchor="w").pack()
    conversion_type = StringVar(value="Próbkowanie")

    # === Checkbox: kwantyzacja – zaokrąglanie / obcięcie ===
    is_rounding = BooleanVar(value=True)
    check_kwantyzacja = Checkbutton(frame_params, text="Zaokrąglaj (odznacz = obcinaj)", variable=is_rounding)

    # === Dropdown: rekonstrukcja ===
    frame_reconstruction_dropdown = Frame(frame_params)
    Label(frame_reconstruction_dropdown, text="Metoda rekonstrukcji:", anchor="w").pack()
    reconstruction_method = StringVar(value="zerowy rząd")
    OptionMenu(frame_reconstruction_dropdown, reconstruction_method, "zerowy rząd", "pierwszy rząd", "sinc").pack()

    # === Parametry konwersji ===
    param_frames = {}
    param_labels = {}

    # Jeden parametr dynamicznie zmieniany
    frame1 = Frame(frame_params)
    lbl1_text = StringVar(value="Częstotliwość próbkowania [Hz]:")
    param_labels[0] = lbl1_text
    Label(frame1, textvariable=lbl1_text, width=label_width, anchor="w").pack(side="top", padx=(13, 0))
    entry1 = Entry(frame1, width=entry_width)
    entry1.pack(side="left", padx=10)
    param_frames["param1"] = frame1
    conversion_param_entries["param1"] = entry1

    def update_visibility(*args):
        selected = conversion_type.get()

        check_kwantyzacja.pack_forget()
        frame_reconstruction_dropdown.pack_forget()
        for frame in param_frames.values():
            frame.pack_forget()

        error_metrics_label.config(text="")

        if selected == "Próbkowanie":
            param_labels[0].set("Częstotliwość próbkowania [Hz]:")
            param_frames["param1"].pack(anchor="w", pady=2)
        elif selected == "Kwantyzacja":
            param_labels[0].set("Liczba poziomów dyskretnych:")
            param_frames["param1"].pack(anchor="w", pady=2)
            check_kwantyzacja.pack(pady=(5, 5))
        elif selected == "Rekonstrukcja":
            param_labels[0].set("Częstotliwość próbkowania [Hz]:")
            param_frames["param1"].pack(anchor="w", pady=2)
            frame_reconstruction_dropdown.pack(pady=(5, 5))

    conversion_type.trace_add("write", update_visibility)
    OptionMenu(frame_params, conversion_type, "Próbkowanie", "Kwantyzacja", "Rekonstrukcja").pack()

    # === Etykieta do wyświetlania metryk błędów ===
    error_metrics_label = Label(frame_params, text="", fg="red", justify="left")
    error_metrics_label.pack()

    # === Przycisk konwertuj ===
    def on_convert():
        if not hasattr(new_window, "signal_data"):
            print("Brak danych sygnału do konwersji.")
            return

        raw_value = conversion_param_entries["param1"].get().strip()
        if not raw_value:
            print("Brak wartości parametru.")
            return

        try:
            value = float(raw_value)
        except ValueError:
            print("Nieprawidłowa wartość parametru.")
            return

        time, signal, signal_type = new_window.signal_data

        if conversion_type.get() == "Próbkowanie":
            if value <= 0:
                print("Częstotliwość musi być > 0.")
                return
            t_sampled, y_sampled = co.probkowanie_rownomierne(time, signal, value)
            label = f"Po próbkowaniu ({value} Hz)"
            new_data = (t_sampled, y_sampled, signal_type)

        elif conversion_type.get() == "Kwantyzacja":
            L = int(value)
            if L <= 0:
                print("Liczba poziomów musi być > 0.")
                return
            quant_func = co.kwantyzacja_rownomierna_zaokraglanie if is_rounding.get() else co.kwantyzacja_rownomierna_obciecie
            yq = quant_func(signal, L)
            label = f"Kwantyzacja ({'zaokrąglanie' if is_rounding.get() else 'obcinanie'}, L={L})"
            new_data = (time, yq, signal_type)

        elif conversion_type.get() == "Rekonstrukcja":
            if value <= 0:
                print("Częstotliwość musi być > 0.")
                return
            t_sampled = time
            y_sampled = signal
            t_full = new_window.original_data[0]
            method = reconstruction_method.get()
            if method == "zerowy rząd":
                y_rec = co.rekonstrukcja_zerowego_rzedu(t_sampled, y_sampled, t_full)
            elif method == "pierwszy rząd":
                y_rec = co.rekonstrukcja_pierwszego_rzedu(t_sampled, y_sampled, t_full)
            else:
                y_rec = co.rekonstrukcja_sinc(t_sampled, y_sampled, t_full)
            label = f"Rekonstrukcja ({method}, {value} Hz)"
            new_data = (t_full, y_rec, signal_type)
        else:
            print("Nieznana operacja.")
            return

        plot_signal(ax, *new_data, title=label)

        if conversion_type.get() == "Rekonstrukcja":
            if hasattr(new_window, "original_data"):
                original_time, original_signal = new_window.original_data
                if len(y_rec) == len(original_signal):
                    mse_val = co.mse(original_signal, y_rec)
                    snr_val = co.snr(original_signal, y_rec)
                    psnr_val = co.psnr(original_signal, y_rec)
                    maxdiff_val = co.max_diff(original_signal, y_rec)
                    error_text = (
                        f"MSE: {mse_val:.4f}\n"
                        f"SNR: {snr_val:.2f} dB\n"
                        f"PSNR: {psnr_val:.2f} dB\n"
                        f"MaxDiff: {maxdiff_val:.4f}"
                    )
                    print("Obliczono miary błędów:")
                    print(error_text)
                    error_metrics_label.config(text=error_text)
                else:
                    error_metrics_label.config(text="Błąd: długości sygnałów się nie zgadzają.")
            else:
                error_metrics_label.config(text="Brak danych odniesienia do obliczeń.")
        else:
            error_metrics_label.config(text="")

        new_window.original_data = (time, signal)
        canvas.draw()
        new_window.signal_data = new_data

    Button(frame_params, text="Konwertuj", command=on_convert).pack(side="top", pady=15)

    frame_plot = Frame(frame_main)
    frame_plot.pack(side="right", fill="both", expand=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    update_visibility()

    return new_window, canvas, fig, ax