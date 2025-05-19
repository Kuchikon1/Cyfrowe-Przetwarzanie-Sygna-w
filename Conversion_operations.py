import math

import numpy as np

def probkowanie_rownomierne(t, y, f):
    Ts = 1 / f
    t_sampled = np.arange(t[0], t[-1] + Ts, Ts)
    y_sampled = np.interp(t_sampled, t, y)
    return t_sampled, y_sampled

def kwantyzacja_rownomierna_obciecie(y, L, ymin=None, ymax=None):
    if ymin is None: ymin = np.min(y)
    if ymax is None: ymax = np.max(y)

    delta = (ymax - ymin) / (L - 1)
    yq = np.floor((y - ymin) / delta) * delta + ymin
    yq = np.clip(yq, ymin, ymax)  # obcięcie

    return yq

def kwantyzacja_rownomierna_zaokraglanie(y, L, ymin=None, ymax=None):
    if ymin is None: ymin = np.min(y)
    if ymax is None: ymax = np.max(y)

    delta = (ymax - ymin) / (L - 1)
    yq = np.round((y - ymin) / delta) * delta + ymin
    yq = np.clip(yq, ymin, ymax)  # zaokrąglanie

    return yq

def rekonstrukcja_zerowego_rzedu(t_sampled, y_sampled, t):
    t_zoh = np.repeat(t_sampled, 2)[1:]
    t_zoh = np.append(t_zoh, t[-1])
    y_zoh = np.repeat(y_sampled, 2)
    return t_zoh, y_zoh

def rekonstrukcja_pierwszego_rzedu(t_sampled, y_sampled, t):
    t_foh = t_sampled
    y_foh = np.interp(t, t_sampled, y_sampled)
    return t_foh, y_foh

def sinc(x):
    y = np.empty_like(x, dtype=float)
    for i, val in np.ndenumerate(x):
        if val == 0:
            y[i] = 1.0
        else:
            y[i] = math.sin(math.pi * val) / (math.pi * val)
    return y

def rekonstrukcja_sinc(t_sampled, y_sampled, t, neighbors):
    y_reconstructed = np.zeros_like(t)
    Ts = np.mean(np.diff(t_sampled))

    N = len(t_sampled)
    total_neighbors = int(2 * neighbors + 1)
    if total_neighbors > N:
        total_neighbors = N

    for i, ti in enumerate(t):
        diffs = np.abs(t_sampled - ti)
        neighbor_indices = np.argsort(diffs)[:total_neighbors]
        sinc_args = (ti - t_sampled[neighbor_indices]) / Ts
        y_reconstructed[i] = np.sum(y_sampled[neighbor_indices] * sinc(sinc_args))

    return t, y_reconstructed

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