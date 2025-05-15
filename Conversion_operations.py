import numpy as np

def probkowanie_rownomierne(t, y, f):
    Ts = 1 / f
    t_sampled = np.arange(t[0], t[-1], Ts)
    y_sampled = np.interp(t_sampled, t, y)
    return t_sampled, y_sampled


def kwantyzacja_rownomierna_obciecie(y, L, ymin=None, ymax=None):
    if ymin is None: ymin = np.min(y)
    if ymax is None: ymax = np.max(y)

    delta = (ymax - ymin) / L
    yq = np.floor((y - ymin) / delta) * delta + ymin
    yq = np.clip(yq, ymin, ymax - delta)  # obcięcie

    return yq


def kwantyzacja_rownomierna_zaokraglanie(y, L, ymin=None, ymax=None):
    if ymin is None: ymin = np.min(y)
    if ymax is None: ymax = np.max(y)

    delta = (ymax - ymin) / L
    yq = np.round((y - ymin) / delta) * delta + ymin
    yq = np.clip(yq, ymin, ymax)  # zaokrąglanie

    return yq

def rekonstrukcja_zerowego_rzedu(t_sampled, y_sampled, t):
    y_reconstructed = np.zeros_like(t)
    j = 0
    for i in range(len(t)):
        while j < len(t_sampled) - 1 and t_sampled[j+1] <= t[i]:
            j += 1
        y_reconstructed[i] = y_sampled[j]
    return y_reconstructed

def rekonstrukcja_pierwszego_rzedu(t_sampled, y_sampled, t):
    y_reconstructed = np.interp(t, t_sampled, y_sampled)
    return y_reconstructed

def sinc(x):
    return np.sinc(x / np.pi)

def rekonstrukcja_sinc(t_sampled, y_sampled, t):
    Ts = t_sampled[1] - t_sampled[0]
    y_reconstructed = np.zeros_like(t)
    for i in range(len(t)):
        y_reconstructed[i] = np.sum(y_sampled * sinc(np.pi * (t[i] - t_sampled) / Ts))
    return y_reconstructed

def mse(y, yq):
    return np.mean((y - yq) ** 2)

def snr(y, yq):
    signal_power = np.mean(y ** 2)
    noise_power = np.mean((y - yq) ** 2)
    return 10 * np.log10(signal_power / noise_power) if noise_power > 0 else np.inf

def psnr(y, yq):
    peak = np.max(np.abs(y))
    mse_val = mse(y, yq)
    return 20 * np.log10(peak / np.sqrt(mse_val)) if mse_val > 0 else np.inf

def max_diff(y, yq):
    return np.max(np.abs(y - yq))
