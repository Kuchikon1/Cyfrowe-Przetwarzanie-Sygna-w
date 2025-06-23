from tkinter import Toplevel, Frame, Button, Label, Entry, StringVar, OptionMenu, Tk, ttk
import Transformations_functions as tf
import Transformations_operations as to
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np


def plot_fourier(ax, freq, magnitude, title="FFT sygnału"):
    ax.clear()
    ax.plot(freq, magnitude, color="blue")
    ax.set_title(title)
    ax.set_xlabel("Częstotliwość [Hz]")
    ax.set_ylabel("Amplituda")
    ax.grid()

def create_fourier_window(root, title="Transformacja Fouriera"):
    new_window = Toplevel(root)
    new_window.title(title)
    new_window.geometry("1200x700")

    frame_buttons = Frame(new_window)
    frame_buttons.pack(side="top", anchor="nw", padx=10, pady=10)

    fourier_param_entries = {}
    analysis_type = StringVar(value="Moduł")

    def update_plot(time, signal_complex, mode="W1", operation_type="FFT"):
        real_part = np.real(signal_complex)
        imag_part = np.imag(signal_complex)
        magnitude = np.abs(signal_complex)
        phase = np.angle(signal_complex)

        ax1.clear()
        ax2.clear()

        if mode == "W1":
            ax1.plot(time, real_part, color="blue")
            ax1.set_title(f"Część rzeczywista ({operation_type})")
            ax1.set_ylabel("Re")
            ax1.grid(True)

            ax2.plot(time, imag_part, color="red")
            ax2.set_title(f"Część urojona ({operation_type})")
            ax2.set_ylabel("Im")
            ax2.grid(True)
        elif mode == "W2":
            ax1.plot(time, magnitude, color="green")
            ax1.set_title(f"Moduł ({operation_type})")
            ax1.set_ylabel("|Z|")
            ax1.grid(True)

            ax2.plot(time, phase, color="orange")
            ax2.set_title(f"Faza ({operation_type})")
            ax2.set_ylabel("arg(Z)")
            ax2.grid(True)

        canvas.draw()

    def on_load_complex_signal():
        result = to.load_complex_signal()
        if result is None or result[1] is None:
            print("Nie udało się wczytać sygnału zespolonego.")
            return

        time, signal, params, signal_type = result

        # Przechowaj dane w oknie
        new_window.signal_data = (time, signal, signal_type)
        new_window.original_data = (time, signal, signal_type)

        # Automatycznie wyświetl wykres po wczytaniu
        update_plot(time, signal, mode=mode_var.get(), operation_type="Wczytany sygnał zespolony")

    fft_len_var = StringVar()
    transform_choice = StringVar()

    Button(frame_buttons, text="Wczytaj sygnał", command=on_load_complex_signal).pack(side="left", padx=(0, 5))

    frame_main = Frame(new_window)
    frame_main.pack(fill="both", expand=True, padx=10, pady=10)

    frame_params = Frame(frame_main)
    frame_params.pack(side="left", fill="y")

    # Label(frame_params, text="Typ analizy FFT:", anchor="w").pack(pady=(0, 5))
    # OptionMenu(frame_params, analysis_type, "Moduł", "Faza").pack(pady=(0, 15))

    # # Lista wartości: potęgi 2 od 2 do 1024
    # fft_lengths = [2 ** i for i in range(1, 11)]  # [2, 4, 8, ..., 1024]
    #
    # Label(frame_params, text="Długość FFT:", anchor="w").pack()
    #
    # # Zmienna kontrolująca wybór
    # fft_len_var = StringVar()
    # fft_len_var.set("1024")  # domyślna wartość
    #
    # # Tworzenie listy rozwijanej
    # fft_len_menu = OptionMenu(frame_params, fft_len_var, *fft_lengths)
    # fft_len_menu.config(width=28)
    # fft_len_menu.pack(pady=(0, 10))
    #
    # # Przypisanie do słownika parametrów (jeśli później odczytujesz z niego)
    # fourier_param_entries["fft_len"] = fft_len_var

    mode_var = StringVar(value="W2")  # domyślnie moduł/faza

    Label(frame_params, text="Tryb wyświetlania:", anchor="w").pack()
    OptionMenu(frame_params, mode_var, "W1", "W2").pack(pady=(0, 10))

    Label(frame_params, text="Wybierz transformację:", font=("Arial", 14)).pack(pady=10)

    # Fouriera
    # Button(frame_params, text="DFT", command=lambda: to.on_generate_complex_and_transform(tf.dft)).pack(pady=3)
    # Button(frame_params, text="FFT", command=lambda: to.on_generate_complex_and_transform(tf.fft_dif)).pack(pady=3)
    # Button(frame_params, text="FFT", command=lambda: to.on_generate_complex_and_transform(tf.fft_dit)).pack(pady=3)
    #
    # # Walsh-Hadamard
    # Button(frame_params, text="WHT", command=lambda: to.on_generate_complex_and_transform(tf.wht)).pack(pady=3)
    # Button(frame_params, text="FWHT", command=lambda: to.on_generate_complex_and_transform(tf.fwht)).pack(pady=3)
    #
    # # Kosinusowa
    # Button(frame_params, text="DCT", command=lambda: to.on_generate_complex_and_transform(tf.dct2)).pack(pady=3)
    # Button(frame_params, text="FDCT", command=lambda: to.on_generate_complex_and_transform(tf.dft)).pack(pady=3)
    #
    # # Falkowa
    # Button(frame_params, text="DWT", command=lambda: to.on_generate_complex_and_transform(tf.wavelet_transform)).pack(pady=3)
    # Button(frame_params, text="FWT", command=lambda: to.on_generate_complex_and_transform(tf.wavelet_fast_transform)).pack(pady=3)

    # Lista możliwych długości FFT
    Label(frame_params, text="Długość FFT:", anchor="w").pack()
    fft_len_combo = ttk.Combobox(frame_params, textvariable=fft_len_var, values=[2 ** i for i in range(1, 11)],
                                 state="readonly")
    fft_len_combo.set("1024")  # wartość domyślna
    fft_len_combo.pack(pady=(0, 10))

    # Lista dostępnych transformacji
    Label(frame_params, text="Rodzaj transformacji:", anchor="w").pack()
    transform_box = ttk.Combobox(frame_params, textvariable=transform_choice, values=[
        "DFT", "FFT_DIT", "FFT_DIF", "DCT", "FCT", "WHT", "FWHT", "Wavelet", "FastWavelet"
    ], state="readonly")
    transform_box.set("DFT")  # wartość domyślna
    transform_box.pack(pady=(0, 10))

    Button(
        frame_buttons,
        text="Generuj i przekształć",
        command=lambda: to.on_generate_complex_and_transform(
            int(fft_len_var.get()), transform_choice.get()
        )
    ).pack()

    frame_plot = Frame(frame_main)
    frame_plot.pack(side="right", fill="both", expand=True)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), sharex=False)
    fig.tight_layout(pad=4.0)

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return new_window, canvas, fig, ax1, ax2
