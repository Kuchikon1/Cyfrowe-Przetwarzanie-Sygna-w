import numpy as np
import matplotlib.pyplot as plt

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

def plot_signal(time, signal, title="Wykres sygnału"):
    plt.plot(time, signal)
    plt.xlabel("Czas [s]")
    plt.ylabel("Amplituda")
    plt.title(title)
    plt.grid()
    plt.show()

def plot_histogram(signal, title="Histogram sygnału", bins=10):
    plt.hist(signal, bins=bins, alpha=0.75, color='blue', edgecolor='black')
    plt.xlabel("Amplituda")
    plt.ylabel("Liczność")
    plt.title(title)
    plt.grid()
    plt.show()

# Wybór sygnału i parametrów
signal_type = input("Wybierz sygnał (S1, S2, S3, ..., S11): ")
frequency = float(input("Podaj częstotliwość (Hz): "))
amplitude = float(input("Podaj amplitudę: "))
duration = float(input("Podaj czas trwania (s): "))
sampling_rate = int(input("Podaj częstotliwość próbkowania (Hz): "))
bins = int(input("Podaj liczbę przedziałów histogramu: "))

# Generowanie sygnału
time, signal = generate_signal(signal_type, frequency, amplitude, duration, sampling_rate)

# Wyświetlanie wykresu sygnału i histogramu
plot_signal(time, signal, f"Sygnał {signal_type}")
plot_histogram(signal, f"Histogram {signal_type}", bins)
