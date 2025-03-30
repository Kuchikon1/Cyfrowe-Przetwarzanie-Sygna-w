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