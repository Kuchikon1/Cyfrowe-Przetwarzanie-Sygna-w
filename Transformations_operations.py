import numpy as np
import Transformations_functions as tf
import Transformations_windows as tw
import File_operations as fo
import pickle
from tkinter import filedialog, messagebox
import time


# def load_and_transform_fourier(use_fft=True):
#     time, signal, params, signal_type = fo.load_signal()
#
#     if signal is None:
#         print("Nie wczytano sygnału.")
#         return None, None, None
#
#     # Konwersja sygnału na typ zespolony (w razie czego)
#     signal = np.asarray(signal, dtype=complex)
#
#     # Transformacja
#     if use_fft:
#         freq_domain = tf.fft_dit(signal)
#     else:
#         freq_domain = tf.dft(signal)
#
#     return freq_domain, time, signal_type


def save_complex_signal(freq_domain, time, signal_type, params=None):
    file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Plik Pickle", "*.pkl")])
    if file_path:
        real_part = np.real(freq_domain)
        imag_part = np.imag(freq_domain)
        with open(file_path, 'wb') as f:
            # Zapisujemy części jako osobne tablice
            pickle.dump((time, real_part, imag_part, params, signal_type), f)
        print(f"Części rzeczywiste i urojone zapisane do {file_path}")


def load_complex_signal():
    file_path = filedialog.askopenfilename(defaultextension=".pkl", filetypes=[("Plik Pickle", "*.pkl")])
    if file_path:
        with open(file_path, 'rb') as f:
            time, real_part, imag_part, params, signal_type = pickle.load(f)
        freq_domain = np.array(real_part) + 1j * np.array(imag_part)
        print(f"Sygnał zespolony zrekonstruowany z części rzeczywistej i urojonej z {file_path}")
        return time, freq_domain, params, signal_type
    else:
        return None, None, None, None


def update_plot_after_operation(time, freq_domain, params, operation_type, mode="W1"):
    import main
    import numpy as np

    real_part = np.real(freq_domain)
    imag_part = np.imag(freq_domain)
    magnitude = np.abs(freq_domain)
    phase = np.angle(freq_domain)

    # Parametry tylko dla modułu
    mean_value, mean_abs_value, rms_value, variance, mean_power = main.calculate_signal_parameters(
        time, magnitude, len(time), operation_type
    )

    params_text = (
        f"[Moduł sygnału zespolonego]\n"
        f"Wartość średnia: {mean_value:.4f}\n"
        f"Wartość średnia bezwzględna: {mean_abs_value:.4f}\n"
        f"Wartość skuteczna (RMS): {rms_value:.4f}\n"
        f"Wariancja: {variance:.4f}\n"
        f"Moc średnia: {mean_power:.4f}"
    )
    main.params_label.config(text=params_text)

    # Czyszczenie osi
    main.ax1.clear()
    main.ax2.clear()

    if mode == "W1":
        # W1: Część rzeczywista i urojona
        main.ax1.plot(time, real_part, color="blue")
        main.ax1.set_title(f"Część rzeczywista ({operation_type})")
        main.ax1.set_ylabel("Re")
        main.ax1.grid(True)

        main.ax2.plot(time, imag_part, color="red")
        main.ax2.set_title(f"Część urojona ({operation_type})")
        main.ax2.set_ylabel("Im")
        main.ax2.grid(True)

    elif mode == "W2":
        # W2: Moduł i faza
        main.ax1.plot(time, magnitude, color="green")
        main.ax1.set_title(f"Moduł sygnału ({operation_type})")
        main.ax1.set_ylabel("|Z|")
        main.ax1.grid(True)

        main.ax2.plot(time, phase, color="orange")
        main.ax2.set_title(f"Faza sygnału ({operation_type})")
        main.ax2.set_ylabel("arg(Z)")
        main.ax2.grid(True)

    main.canvas.draw()


# def on_generate_complex_and_transform(transform_function):
#     print("Wybierz sygnał dla części rzeczywistej:")
#     time1, signal1, params1, signal_type1 = fo.load_signal()
#     print("Wybierz sygnał dla części urojonej:")
#     time2, signal2, params2, signal_type2 = fo.load_signal()
#
#     if time1 is None or time2 is None:
#         print("Nie udało się wczytać obu sygnałów.")
#         return
#
#     if len(time1) != len(time2) or not np.allclose(time1, time2):
#         print("Błąd: sygnały muszą mieć taki sam czas.")
#         return
#
#     # Budujemy sygnał zespolony
#     complex_signal = np.array(signal1) + 1j * np.array(signal2)
#
#     # Pobierz długość FFT wybraną przez użytkownika
#     fft_len = int(tw.fourier_param_entries["fft_len"].get())
#
#     # Przytnij lub dopaduj sygnał do wybranej długości
#     if len(complex_signal) > fft_len:
#         signal_to_transform = complex_signal[:fft_len]
#     elif len(complex_signal) < fft_len:
#         padding = np.zeros(fft_len - len(complex_signal), dtype=complex)
#         signal_to_transform = np.concatenate((complex_signal, padding))
#     else:
#         signal_to_transform = complex_signal
#
#     # Mierzenie czasu transformacji
#     start_time = time.perf_counter()
#     transformed_signal = transform_function(complex_signal)
#     end_time = time.perf_counter()
#
#     elapsed_time = end_time - start_time
#     print(f"Czas wykonania transformacji {transform_function.__name__}: {elapsed_time:.6f} s")
#
#     # Zapis sygnału
#     combined_signal_type = f"Zespolony + {transform_function.__name__}"
#     save_complex_signal(transformed_signal, time1, combined_signal_type, params1)
#
#     # Wyświetlenie wyniku w oknie
#     messagebox.showinfo(
#         title="Czas transformacji",
#         message=f"Transformacja {transform_function.__name__} zakończona.\n\n"
#                 f"Czas wykonania: {elapsed_time:.6f} sekund"
#     )
#
#     print("Transformacja zakończona i wynik zapisany.")

def on_generate_complex_and_transform(fft_len, selected_transform):
    print("Wybierz sygnał dla części rzeczywistej:")
    time1, signal1, params1, signal_type1 = fo.load_signal()
    print("Wybierz sygnał dla części urojonej:")
    time2, signal2, params2, signal_type2 = fo.load_signal()

    if time1 is None or time2 is None:
        print("Nie udało się wczytać obu sygnałów.")
        return

    if len(time1) != len(time2) or not np.allclose(time1, time2):
        print("Błąd: sygnały muszą mieć taki sam czas.")
        return

    # Budujemy sygnał zespolony
    complex_signal = np.array(signal1) + 1j * np.array(signal2)
    combined_signal_type = f"Zespolony: {signal_type1} + i{signal_type2}"

    # Wykonujemy transformację na sygnale zespolonym
    start_time = time.time()

    if selected_transform == "DFT":
        transformed = tf.dft(complex_signal[:fft_len])
    elif selected_transform == "FFT_DIT":
        transformed = tf.fft_dit(complex_signal[:fft_len])
    elif selected_transform == "FFT_DIF":
        transformed = tf.fft_dif(complex_signal[:fft_len])
    elif selected_transform == "DCT":
        transformed = tf.dct2(np.real(complex_signal[:fft_len]))
    elif selected_transform == "WHT":
        transformed = tf.wht(np.real(complex_signal[:fft_len]))
    elif selected_transform == "FWHT":
        transformed = tf.fwht(np.real(complex_signal[:fft_len]))
    elif selected_transform == "Wavelet":
        a, d = tf.wavelet_transform(np.real(complex_signal[:fft_len]))
        transformed = (a, d)
    elif selected_transform == "FastWavelet":
        transformed = tf.wavelet_fast_transform(np.real(complex_signal[:fft_len]))
    else:
        messagebox.showerror("Błąd", "Nieobsługiwany typ transformacji.")
        return

    duration = time.time() - start_time
    messagebox.showinfo("Czas operacji", f"Czas wykonania transformacji: {duration:.4f} sekund")

    should_save = messagebox.askyesno("Zapis transformacji", "Czy chcesz zapisać wynik transformacji?")
    if should_save:
        if isinstance(transformed, tuple):
            transformed = np.concatenate(transformed)

        transform_type = f"Transformacja: {selected_transform}"
        dummy_time = time1[:len(transformed)] if len(time1) >= len(transformed) else np.linspace(0, 1, len(transformed))
        save_complex_signal(transformed, dummy_time, transform_type, params1)

    print("Transformacja zakończona.")

