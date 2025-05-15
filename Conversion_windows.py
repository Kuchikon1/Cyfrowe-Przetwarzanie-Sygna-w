from tkinter import Toplevel, Frame, Button, Label, Entry

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
    new_window.geometry("1100x400")

    frame_buttons = Frame(new_window)
    frame_buttons.pack(side="top", anchor="nw", padx=10, pady=10)

    def save_signal_window():
        pass

    def load_signal_window():
        data = on_load()
        if data is None:
            return
        time_l, signal_l, params_l, signal_type_l = data

        new_window.signal_data = (time_l, signal_l, signal_type_l)

        plot_signal(ax, time_l, signal_l, signal_type_l, f"Wczytany sygnał {signal_type_l}")
        canvas.draw()

    # Przyciski obok siebie
    btn_save = Button(frame_buttons, text="Zapisz sygnał", command=save_signal_window)
    btn_save.pack(side="left", padx=(0, 5))

    btn_load = Button(frame_buttons, text="Wczytaj sygnał", command=load_signal_window)
    btn_load.pack(side="left")

    # Ramka na parametry konwersji i wykres
    frame_main = Frame(new_window)
    frame_main.pack(fill="both", expand=True, padx=10, pady=10)

    # Lewa część - parametry konwersji
    frame_params = Frame(frame_main)
    frame_params.pack(side="left", fill="y")

    # Tutaj tworzymy pola na parametry
    label_width = 35
    entry_width = 37

    # Wyczyść słownik, by odświeżyć pola przy kolejnym otwarciu
    conversion_param_entries.clear()

    for param in param_names:
        frame = Frame(frame_params)
        frame.pack(anchor="w", pady=2)
        Label(frame, text=param, width=label_width, anchor="w").pack(side="top", padx=(13,0))
        entry = Entry(frame, width=entry_width)
        entry.pack(side="left", padx=10)
        conversion_param_entries[param] = entry

    # Przycisk konwertuj pod parametrami
    def on_convert():
        # tutaj możesz podłączyć swoją funkcję konwersji,
        # np. pobrać parametry i wykonać operację
        params = {key: entry.get() for key, entry in conversion_param_entries.items()}
        print("Parametry do konwersji:", params)
        # dalej - logika konwersji, aktualizacja wykresu itp.

    btn_convert = Button(frame_params, text="Konwertuj", command=on_convert)
    btn_convert.pack(side="top", pady=15)

    # Prawa część - wykres
    frame_plot = Frame(frame_main)
    frame_plot.pack(side="right", fill="both", expand=True)

    # Figure i canvas
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    fig, ax = plt.subplots(figsize=(8, 6))
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return new_window, canvas, fig, ax
