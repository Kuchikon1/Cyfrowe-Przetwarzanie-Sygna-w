from tkinter import Toplevel, Frame, Button

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

def create_conversion_window(root, title, signal_var, option_var, conversion_param_entries, on_save, on_load):
    new_window = Toplevel(root)
    new_window.title(title)
    new_window.geometry("1000x700")

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
    frame_params.pack(side="left", fill="y", padx=(0, 10))

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
