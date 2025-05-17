# from tkinter import Toplevel, Frame, Button, Label, Entry
# import File_operations as fo
# import Conversion_operations as co
#
# def get_full_param_name(abbreviation, pool):
#     return next((name for name, abbr in pool.items() if abbr == abbreviation), abbreviation)
#
# def plot_signal(ax, time, signal, signal_type, title="Wykres sygnału"):
#     ax.clear()
#     if signal_type in ["S10", "S11"]:
#         ax.scatter(time, signal, label="Sygnał", color='blue')
#     else:
#         ax.plot(time, signal, label="Sygnał")
#     ax.set_xlabel("Czas [s]")
#     ax.set_ylabel("Amplituda")
#     ax.set_title(title)
#     ax.legend()
#     ax.grid()
#
# def create_conversion_window(root, title, signal_var, conversion_param_entries, on_save, on_load, param_names=[]):
#     new_window = Toplevel(root)
#     new_window.title(title)
#     new_window.geometry("1100x400")
#
#     frame_buttons = Frame(new_window)
#     frame_buttons.pack(side="top", anchor="nw", padx=10, pady=10)
#
#     def save_signal_window():
#         if hasattr(new_window, "signal_data"):
#             time, signal, signal_type = new_window.signal_data
#             params = {key: entry.get() for key, entry in conversion_param_entries.items()}
#             fo.save_signal(time, signal, params, signal_type)
#         else:
#             print("Brak danych sygnału do zapisania.")
#
#     def load_signal_window():
#         data = on_load()
#         if data is None:
#             return
#         time_l, signal_l, params_l, signal_type_l = data
#
#         new_window.signal_data = (time_l, signal_l, signal_type_l)
#
#         plot_signal(ax, time_l, signal_l, signal_type_l, f"Wczytany sygnał {signal_type_l}")
#         canvas.draw()
#
#     # Przyciski obok siebie
#     btn_save = Button(frame_buttons, text="Zapisz sygnał", command=save_signal_window)
#     btn_save.pack(side="left", padx=(0, 5))
#
#     btn_load = Button(frame_buttons, text="Wczytaj sygnał", command=load_signal_window)
#     btn_load.pack(side="left")
#
#     # Ramka na parametry konwersji i wykres
#     frame_main = Frame(new_window)
#     frame_main.pack(fill="both", expand=True, padx=10, pady=10)
#
#     # Lewa część - parametry konwersji
#     frame_params = Frame(frame_main)
#     frame_params.pack(side="left", fill="y")
#
#     # Tutaj tworzymy pola na parametry
#     label_width = 35
#     entry_width = 37
#
#     # Wyczyść słownik, by odświeżyć pola przy kolejnym otwarciu
#     conversion_param_entries.clear()
#
#     for param in param_names:
#         frame = Frame(frame_params)
#         frame.pack(anchor="w", pady=2)
#         Label(frame, text=param, width=label_width, anchor="w").pack(side="top", padx=(13,0))
#         entry = Entry(frame, width=entry_width)
#         entry.pack(side="left", padx=10)
#         conversion_param_entries[param] = entry
#
#     # Przycisk konwertuj pod parametrami
#     def on_convert():
#         if not hasattr(new_window, "signal_data"):
#             print("Brak danych sygnału do konwersji.")
#             return
#
#         # Pobierz wszystkie parametry jako słownik: {nazwa: wartość}
#         params = {key: entry.get() for key, entry in conversion_param_entries.items()}
#
#         if not params:
#             print("Brak wprowadzonych parametrów.")
#             return
#
#         # Pobierz pierwszy parametr (np. częstotliwość próbkowania)
#         param_name, raw_value = next(iter(params.items()))
#         raw_value = raw_value.strip()
#
#         try:
#             f = float(raw_value)
#             if f <= 0:
#                 print("Częstotliwość próbkowania musi być większa od zera.")
#                 return
#         except ValueError:
#             print(f"Nieprawidłowa wartość parametru '{param_name}': '{raw_value}'")
#             return
#
#         # Pobierz dane sygnału
#         time, signal, signal_type = new_window.signal_data
#
#         # Próbkowanie
#         t_sampled, y_sampled = co.probkowanie_rownomierne(time, signal, f)
#
#         # Aktualizacja wykresu
#         plot_signal(ax, t_sampled, y_sampled, signal_type, f"Sygnał po próbkowaniu ({f} Hz)")
#         canvas.draw()
#
#         # Zapis nowego sygnału do okna
#         new_window.signal_data = (t_sampled, y_sampled, signal_type)
#
#     btn_convert = Button(frame_params, text="Konwertuj", command=on_convert)
#     btn_convert.pack(side="top", pady=15)
#
#     # Prawa część - wykres
#     frame_plot = Frame(frame_main)
#     frame_plot.pack(side="right", fill="both", expand=True)
#
#     # Figure i canvas
#     import matplotlib.pyplot as plt
#     from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#     fig, ax = plt.subplots(figsize=(8, 6))
#     canvas = FigureCanvasTkAgg(fig, master=frame_plot)
#     canvas.get_tk_widget().pack(fill="both", expand=True)
#
#     return new_window, canvas, fig, ax

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
        plot_signal(ax, time_l, signal_l, signal_type_l, f"Wczytany sygnał {signal_type_l}")
        canvas.draw()

    btn_save = Button(frame_buttons, text="Zapisz sygnał", command=save_signal_window)
    btn_save.pack(side="left", padx=(0, 5))

    btn_load = Button(frame_buttons, text="Wczytaj sygnał", command=load_signal_window)
    btn_load.pack(side="left")

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
    OptionMenu(frame_params, conversion_type, "Próbkowanie", "Kwantyzacja", "Rekonstrukcja").pack()

    # === Checkbox: kwantyzacja – zaokrąglanie / obcięcie ===
    is_rounding = BooleanVar(value=True)
    check_kwantyzacja = Checkbutton(frame_params, text="Zaokrąglaj (odznacz = obcinaj)", variable=is_rounding)
    check_kwantyzacja.pack(pady=(5, 5))

    # === Dropdown: rekonstrukcja ===
    Label(frame_params, text="Metoda rekonstrukcji:", anchor="w").pack()
    reconstruction_method = StringVar(value="zerowy rząd")
    OptionMenu(frame_params, reconstruction_method, "zerowy rząd", "pierwszy rząd", "sinc").pack()

    # === Parametry konwersji ===
    for param in param_names:
        frame = Frame(frame_params)
        frame.pack(anchor="w", pady=2)
        Label(frame, text=param, width=label_width, anchor="w").pack(side="top", padx=(13,0))
        entry = Entry(frame, width=entry_width)
        entry.pack(side="left", padx=10)
        conversion_param_entries[param] = entry

    # === Przycisk konwersji ===
    def on_convert():
        if not hasattr(new_window, "signal_data"):
            print("Brak danych sygnału do konwersji.")
            return

        params = {key: entry.get() for key, entry in conversion_param_entries.items()}
        if not params:
            print("Brak parametrów.")
            return

        try:
            values = [float(val.strip()) for val in params.values()]
        except ValueError:
            print("Wprowadź prawidłowe wartości numeryczne.")
            return

        time, signal, signal_type = new_window.signal_data

        if conversion_type.get() == "Próbkowanie":
            f = values[0]
            if f <= 0:
                print("Częstotliwość musi być > 0.")
                return
            t_sampled, y_sampled = co.probkowanie_rownomierne(time, signal, f)
            label = f"Po próbkowaniu ({f} Hz)"
            new_data = (t_sampled, y_sampled, signal_type)

        elif conversion_type.get() == "Kwantyzacja":
            L = int(values[0])
            if L <= 0:
                print("Liczba poziomów musi być > 0.")
                return
            quant_func = co.kwantyzacja_rownomierna_zaokraglanie if is_rounding.get() else co.kwantyzacja_rownomierna_obciecie
            yq = quant_func(signal, L)
            label = f"Kwantyzacja ({'zaokrąglanie' if is_rounding.get() else 'obcinanie'}, L={L})"
            new_data = (time, yq, signal_type)

        elif conversion_type.get() == "Rekonstrukcja":
            if len(time) != len(signal):
                print("Sygnał musi być po próbkowaniu (różna długość od czasu).")
                return
            method = reconstruction_method.get()
            t_sampled = time
            y_sampled = signal
            t_full = np.linspace(t_sampled[0], t_sampled[-1], 1000)
            if method == "zerowy rząd":
                y_rec = co.rekonstrukcja_zerowego_rzedu(t_sampled, y_sampled, t_full)
            elif method == "pierwszy rząd":
                y_rec = co.rekonstrukcja_pierwszego_rzedu(t_sampled, y_sampled, t_full)
            else:
                y_rec = co.rekonstrukcja_sinc(t_sampled, y_sampled, t_full)
            label = f"Rekonstrukcja ({method})"
            new_data = (t_full, y_rec, signal_type)

        else:
            print("Nieznana operacja.")
            return

        plot_signal(ax, *new_data, title=label)
        canvas.draw()
        new_window.signal_data = new_data

    btn_convert = Button(frame_params, text="Konwertuj", command=on_convert)
    btn_convert.pack(side="top", pady=15)

    # Wykres
    frame_plot = Frame(frame_main)
    frame_plot.pack(side="right", fill="both", expand=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return new_window, canvas, fig, ax
