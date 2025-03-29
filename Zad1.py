import copy

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import math


# generacja szumów
# 1 o rozkładzie stałym / w przedziale od a do b ma stałą wartość poza ma 0
# 2 o rozkładzie gaussowskim / jakiś program na wikampie jest
# 3 sinus ze wzoru Acos(2pif0t + fi0)
# 4 sinus są tu https://pl.wikipedia.org/wiki/Sygna%C5%82_okresowy
# 5 wyżej
# 6 prostąktny czyli ma dwie wartości
# 7 prostokątny (chyba) o tych samych grubościach między skokiem
# 8 trójkatny taki jak moduł wygląda
# 9 skokowa przyjmuje 1 dla wartości nieujemnych dla ujemnych ma 0
# 10 impuls skokowy ma wartość 0 z wyjątkiem pojedyńczego punktu
# 11 nie mam pojęcia XD


def func_rand(amp, t1, dur):
    sig = []
    for i in range(dur - t1 * 100):
        sig.append(random.uniform(-amp, amp))
    return sig


def func_sin(amp, inter, t1, dur, repeats):
    sig = []
    temp = []
    for i in range(dur - t1 * (100 * inter * 2)):
        temp.append(amp * math.sin(math.radians(i)))
    for i in range(repeats):
        sig.append(temp)
    return sig


def func_gauss(amp, t1, dur):
    sig = []
    for i in range(dur - t1 * 100):
        sig.append(random.gauss(0, 1))
    return sig


def func_sin_one_half(amp, inter, t1, dur, repeats):
    sig = []
    temp = []
    for i in range(dur - t1 * (100 * inter * 2)):
        temp_var = math.sin(math.radians(i))
        temp.append(amp * (temp_var + abs(temp_var)) / 2)
    for i in range(repeats):
        sig.append(temp)
    return sig


def func_sin_two_half(amp, inter, t1, dur, repeats):
    sig = []
    temp = []
    for i in range(dur - t1 * (100 * inter * 2)):
        temp_var = math.sin(math.radians(i))
        temp.append(amp * abs(temp_var))
    for i in range(repeats):
        sig.append(temp)
    return sig


def func_rect(amp, inter, t1, dur, rise, repeats):
    sig = []
    temp = []
    for i in range(dur - t1 * (100 * inter * rise)):
        temp.append(amp)
    for i in range(dur - t1 * (100 * inter * (1 - rise))):
        temp.append(0)
    for i in range(repeats):
        sig.append(temp)
    return sig


def func_rect_sym(amp, inter, t1, dur, rise, repeats):
    sig = []
    temp = []
    for i in range(dur - t1 * (100 * inter * rise)):
        temp.append(amp)
    for i in range(dur - t1 * (100 * inter * (1 - rise))):
        temp.append(-amp)
    for i in range(repeats):
        sig.append(temp)
    return sig


def func_tria(amp, inter, t1, dur, rise, repeats):
    sig = []
    temp = []
    for i in range(dur - t1 * (100 * inter * rise)):
        temp.append(amp)
    for i in range(dur - t1 * (100 * inter * (1 - rise))):
        temp.append(-amp)
    for i in range(repeats):
        sig.append(temp)
    return sig


def func_jump(amp, dur):
    sig = []
    for i in range(dur * 100):
        sig.append(0)
    sig.append(amp / 2)
    for i in range(dur * 100):
        sig.append(amp)
    return sig


def func_imp(amp, imp, dur, freq):
    sig = []
    for i in range(dur):
        if i == imp:
            sig.append(amp)
        else:
            sig.append(0)
        for j in range(freq - 1):
            sig.append(-1)
    return sig


def func_imp_rand(amp, dur, freq, prop):
    sig = []
    check = 0
    for i in range(dur):
        check = random.random()
        if prop <= check:
            sig.append(amp)
        else:
            sig.append(0)
        for j in range(freq - 1):
            sig.append(-1)
    return sig


# def func_rand(exp, var):
#     res = (((12.0 * var)**0.5) * ((random.randint(0, 100) - 50.0)/100.0)) + exp
#     return res


# def func_gauss(exp, var):
#     n = 10
#     x = 0.0
#     for i in range(n):
#         x += random.random()
#     res = (x * (var/n) ** 0.5) + exp
#     return res


# --------------------------------


def aggregations(means, clusters1, centroids1, colors):
    ddk = "Długość działki kielicha (cm)"
    sdk = "Szerokość działki kielicha (cm)"
    dp = "Długość płatka (cm)"
    sp = "Szerokość płatka (cm)"

    show(get_table(means, clusters1, 0), get_table(means, clusters1, 1), ddk, sdk,
         get_centroid(means, centroids1, 0), get_centroid(means, centroids1, 1), colors)


def show_func(col_x, col_y, xlabel, ylabel, title):
    plt.rcParams.update({'font.size': 16})
    plt.figure(figsize=(8, 6))
    plt.plot(col_x, col_y, s=100)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.show()


def show_func_fuzz(col_x, col_y, xlabel, ylabel, title):
    plt.rcParams.update({'font.size': 16})
    x = np.array([i for i in range(2, 11)])
    plt.xticks(np.arange(1, 16, step=1))
    plt.yticks(np.arange(1, max(iterations) + 2, step=1))
    plt.hist(x, iterations, s=100, marker='.')
    plt.xlabel("k")
    plt.ylabel("Liczba iteracji")
    plt.plot(x, iterations)
    plt.show()


def show_wcss(wcss):
    plt.rcParams.update({'font.size': 16})
    x = np.array([i for i in range(2, 11)])
    plt.xticks(np.arange(1, 16, step=1))
    plt.yticks(np.arange(0, max(wcss), step=20))
    plt.scatter(x, wcss, s=100, marker='.')
    plt.xlabel("k")
    plt.ylabel("Liczba iteracji")
    plt.plot(x, wcss)
    plt.show()


def write_to_file(typer, data):
    f = open(typer, "w")
    f.write(data)
    f.close()


def read_from_file(typer):
    f = open(typer, "r")
    data = f.read()
    f.close()
    return data
