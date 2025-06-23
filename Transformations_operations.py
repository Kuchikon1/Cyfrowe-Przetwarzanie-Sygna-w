import numpy as np
import Transformations_functions as tf
import Transformations_windows as tw
import File_operations as fo
import pickle
from tkinter import filedialog, messagebox, simpledialog
import time

def save_complex_signal(signal, params, signal_type):
    file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle", "*.pkl")])
    if not file_path:
        return

    fs = None
    if params and isinstance(params, dict):
        fs = params.get("fs", None)

    if fs is None:
        fs = simpledialog.askfloat("Brak fs", "Podaj częstotliwość próbkowania (fs):")
        if fs is None:
            messagebox.showwarning("Anulowano", "Nie podano częstotliwości próbkowania.")
            return
        params = params or {}
        params["fs"] = fs

    time = np.arange(len(signal)) / fs
    real_part = np.real(signal)
    imag_part = np.imag(signal)

    with open(file_path, 'wb') as f:
        pickle.dump((time, real_part, imag_part, params, signal_type), f)

    print(f"Sygnał zespolony zapisany do {file_path}")

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

def nearest_lower_power_of_two(n):
    return 2 ** (n.bit_length() - 1)

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

    complex_signal = np.array(signal1) + 1j * np.array(signal2)
    combined_signal_type = f"Zespolony: {signal_type1} + i{signal_type2}"

    # Upewnij się, że długość sygnału nie przekracza fft_len
    max_len = min(len(complex_signal), fft_len)

    # Dla FFT/FCT: znajdź najbliższą potęgę 2
    if selected_transform in ["FFT_DIT", "FFT_DIF", "FCT", "FWHT"]:
        fft_len_adjusted = nearest_lower_power_of_two(max_len)
        print(f"Dostosowano długość do {fft_len_adjusted} (najbliższa potęga 2)")
    else:
        fft_len_adjusted = max_len

    signal_for_transform = complex_signal[:fft_len_adjusted]

    # Wykonaj transformację
    start_time = time.time()

    if selected_transform == "DFT":
        transformed = tf.dft(signal_for_transform)
    elif selected_transform == "FFT_DIT":
        transformed = tf.fft_dit(signal_for_transform)
    elif selected_transform == "FFT_DIF":
        transformed = tf.fft_dif(signal_for_transform)
    elif selected_transform == "DCT":
        transformed = tf.dct(np.real(signal_for_transform))
    elif selected_transform == "FCT":
        transformed = tf.fct(np.real(signal_for_transform))
    elif selected_transform == "WHT":
        transformed = tf.wht(np.real(signal_for_transform))
    elif selected_transform == "FWHT":
        transformed = tf.fwht(np.real(signal_for_transform))
    elif selected_transform == "Wavelet":
        a, d = tf.wavelet_transform(np.real(signal_for_transform))
        transformed = (a, d)
    elif selected_transform == "FastWavelet":
        transformed = tf.wavelet_fast_transform(np.real(signal_for_transform))
    else:
        messagebox.showerror("Błąd", "Nieobsługiwany typ transformacji.")
        return

    duration = time.time() - start_time
    messagebox.showinfo("Czas operacji", f"Czas wykonania transformacji: {duration:.4f} sekund")

    signal_type = f"Transformacja: {selected_transform}"
    save_complex_signal(transformed, params1, signal_type)  # zakładam, że masz już tę funkcję

    print("Transformacja zakończona.")


