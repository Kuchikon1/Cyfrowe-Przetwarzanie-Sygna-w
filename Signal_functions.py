import numpy as np
import math

N = 1000 # Liczba próbek dla sygnałów ciągłych

# Funkcja do generowania szumu o równomiernym rozkładzie
def szum_o_rozkładzie_jednostajnym(A, t1, d):
    t = np.linspace(t1, t1 + d, N)
    y = (np.random.random(N) * 2 - 1) * A
    return t, y, d, t1

# Funkcja do generowania szumu Gaussa
def szum_gaussowski(A, t1, d):
    t = np.linspace(t1, t1 + d, N)
    y = np.random.normal(size=N) * A
    return t, y, d, t1

def sygnal_sinusoidalny(A, T, t1, d):
    t = np.linspace(t1, t1 + d, N)
    y = A * np.sin(2 * np.pi * (t - t1) / T)

    return t, y, d, t1

def sygnal_sinusoidalny_wyprosotowany_jednopolowkowo(A, T, t1, d):
    t = np.linspace(t1, t1 + d, N)
    y = A * (np.sin(2 * np.pi * (t - t1) / T) + np.abs(np.sin(2 * np.pi * (t - t1) / T))) / 2

    return t, y, d, t1

def sygnal_sinusoidalny_wyprosotowany_dwupolowkowo(A, T, t1, d):
    t = np.linspace(t1, t1 + d, N)
    y = np.abs(A * np.sin(2 * np.pi * (t - t1) / T))

    return t, y, d, t1

def sygnal_prostokatny(A, T, t1, d, kw):
    t = np.linspace(t1, t1 + d, N)
    y = np.zeros_like(t)

    high_duration = kw * T

    for k in range(math.ceil((d) / T)):
        start = t1 + k * T
        high_end = start + high_duration

        for i, elem in enumerate(t):
            if start <= elem < high_end:
                y[i] = A

    return t, y, d, t1

def sygnal_prostokatny_symetryczny(A, T, t1, d, kw):
    t = np.linspace(t1, t1 + d, N)
    y = np.zeros_like(t)

    high_duration = kw * T
    low_duration = T - high_duration

    for k in range(math.ceil((d) / T)):
        start = t1 + k * T
        high_end = start + high_duration
        low_end = high_end + low_duration

        for i, elem in enumerate(t):
            if start <= elem < high_end:
                y[i] = A
            elif high_end <= elem < low_end:
                y[i] = -A

    return t, y, d, t1

def sygnal_trojkatny(A, T, t1, d, kw):
    t = np.linspace(t1, t1 + d, N)
    y = np.ones_like(t)

    ranges = []

    for k in range(math.ceil((t1 + d) / T)):
        ranges.append(((k * T + t1, k * T + kw * T + t1, k), (kw * T + t1 + k * T, T + k * T + t1, k)))

    for r in ranges:
        for i, elem in enumerate(t):
            if elem >= r[0][0] and elem < r[0][1]:
                y[i] = A * (elem - r[0][2] * T - t1) / (kw * T)
    for r in ranges:
        for i, elem in enumerate(t):
            if elem >= r[1][0] and elem < r[1][1]:
                y[i] = -A * (elem - r[1][2] * T - t1) / (T * (1 - kw)) + A / (1 - kw)

    return t, y, d, t1

def skok_jednostkowy(A, t1, d, ts):
    t = np.linspace(t1, t1 + d, N)
    y = np.zeros_like(t)

    y[t >= ts] = A
    return t, y, d, t1

def impuls_jednostkowy(A, ns, n1, d, f):
    t = np.arange(n1, d, f)
    y = np.zeros_like(t)

    y[int(ns - n1)] = A

    return t, y, d

def szum_impulsowy(A, t1, d, f, p):
    t = np.arange(t1, t1 + d, f)
    y = np.random.random(t.shape[0])
    y = np.where(y <= p, A, 0)

    return t, y, d