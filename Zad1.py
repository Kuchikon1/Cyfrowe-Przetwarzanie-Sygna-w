import copy

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

iteration = 0
temp = 0

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


def func_rand(exp, var):
    res = (((12.0 * var)**0.5) * ((random.randint(0, 100) - 50.0)/100.0)) + exp
    return res


def func_gauss(exp, var):
    n = 10
    x = 0.0
    for i in range(n):
        x += random.random()
    res = (x * (var/n) ** 0.5) + exp
    return res


#--------------------------------


def end_algorithm(old_cen, new_cen, k):
    # print("old cen:")
    # print(old_cen)
    # print("new cen:")
    # print(new_cen)
    checked = False
    flag = 0
    for i in range(k):
        if np.array_equal(old_cen[i], new_cen[i]):
            flag += 1
    if flag == k:
        checked = True
    return checked


def loop(k, cen, agg):  # poczatkowe centroidy randomowe, agg - wszystkie dane z pliku

    old_cen = copy.deepcopy(cen)
    # print("stare centroidy\n")
    # print(old_cen)
    iterationy = 0
    while True:
        new_clusters = cluster(k, old_cen, agg)  # robimy k klastrow w ktorych sa dane
        new_cen = update_centroids(k, new_clusters)
        # print("nowe centroidy: \n")
        # print(new_cen)
        global iteration
        iteration += 1
        iterationy = iterationy + 1
        print(f"Iteration: {iterationy}")

        if end_algorithm(old_cen, new_cen, k):
            global temp
            temp = iteration
            iteration = 0
            break
        else:
            old_cen = new_cen

    # for i in range(len(new_clusters)):
    #     print(f"Cluster {i + 1}: {new_clusters[i]}")
    return new_cen


def update_centroids(k, clusters):
    cen = [0.0 for _ in range(k)]
    for i in range(k):
        cen[i] = mean_centroid(clusters[i])  # zastapienie starego centroidu nowa srednia
    return cen


def mean_centroid(clusters):
    mean_vector = [0.0 for _ in range(4)]  # nowy centroid z nowej sredniej dla klastra
    # print("wyglad clusterow")
    # print(clusters)
    for vector in clusters:
        for i in range(4):
            mean_vector[i] += vector[i]

    mean_vector[0] /= len(clusters)
    mean_vector[1] /= len(clusters)
    mean_vector[2] /= len(clusters)
    mean_vector[3] /= len(clusters)
    return mean_vector


def place_centroid(k, agg):
    centroids = random.sample(agg, k)  # GIT
    return centroids


def cluster(k, cen, agg):
    clusters = [[] for _ in range(k)]
    for i in range(len(agg)):
        clusters[grouping(k, cen, agg[i])].append(agg[i])

        # for i in range(len(clusters)):
        #     print(f"Cluster {i + 1}: {clusters[i]}")
    return clusters


def distance(tab, cent):
    return (((tab[0] - cent[0]) ** 2) + ((tab[1] - cent[1]) ** 2) + ((tab[2] - cent[2]) ** 2) +
            ((tab[3] - cent[3]) ** 2)) ** 0.5  # GIT


def grouping(k, cen, agg):
    min_val = 0
    temp = distance(agg, cen[0])  # odleglosc pierwszego punktu od pierwszego centroidu
    for i in range(1, k):
        temp_dist = distance(agg, cen[i])  # odlegosc pierwszgo punktu od drugiego centroidu
        if temp_dist < temp:  # GIT
            min_val = i
            temp = temp_dist
    return min_val


def get_table(k, clustersy, index):
    table = [0.0 for _ in range(150)]
    a = 0
    for i in range(k):
        for j in range(len(clustersy[i])):
            table[a] = clustersy[i][j][index]
            a += 1
    return table


def get_centroid(k, cen, index):
    table = [0.0 for _ in range(k)]
    for i in range(k):
        table[i] = cen[i][index]
    return table


def color(k, clustresy):
    table = [0 for _ in range(150)]
    a = 0
    for i in range(k):
        for j in range(len(clustresy[i])):
            table[a] = i
            a += 1
    return table


def aggregations(means, clusters1, centroids1, colors):
    ddk = "Długość działki kielicha (cm)"
    sdk = "Szerokość działki kielicha (cm)"
    dp = "Długość płatka (cm)"
    sp = "Szerokość płatka (cm)"

    show(get_table(means, clusters1, 0), get_table(means, clusters1, 1), ddk, sdk,
         get_centroid(means, centroids1, 0), get_centroid(means, centroids1, 1), colors)
    show(get_table(means, clusters1, 0), get_table(means, clusters1, 2), ddk, dp,
         get_centroid(means, centroids1, 0), get_centroid(means, centroids1, 2), colors)
    show(get_table(means, clusters1, 0), get_table(means, clusters1, 3), ddk, sp,
         get_centroid(means, centroids1, 0), get_centroid(means, centroids1, 3), colors)
    show(get_table(means, clusters1, 1), get_table(means, clusters1, 2), sdk, dp,
         get_centroid(means, centroids1, 1), get_centroid(means, centroids1, 2), colors)
    show(get_table(means, clusters1, 1), get_table(means, clusters1, 3), sdk, sp,
         get_centroid(means, centroids1, 1), get_centroid(means, centroids1, 3), colors)
    show(get_table(means, clusters1, 2), get_table(means, clusters1, 3), dp, sp,
         get_centroid(means, centroids1, 2), get_centroid(means, centroids1, 3), colors)


def show(col_x, col_y, xlabel, ylabel, cen_x, cen_y, colors):
    # start = math.floor(min(colX)) - 0.1
    # end = math.ceil(max(colX))
    cen_colors = [0, 1, 2]
    plt.rcParams.update({'font.size': 16})
    plt.figure(figsize=(8, 6))
    plt.scatter(col_x, col_y, s=100, c=colors)
    plt.scatter(cen_x, cen_y, s=250, c=cen_colors, edgecolors='black', marker='D')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.show()


def show_iterations(iterations):
    plt.rcParams.update({'font.size': 16})
    x = np.array([i for i in range(2, 11)])
    plt.xticks(np.arange(1, 16, step=1))
    plt.yticks(np.arange(1, max(iterations)+2, step=1))
    plt.scatter(x, iterations, s=100, marker='.')
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


def get_wcss(agg, cen):
    wcss = 0.0
    for i in range(len(agg)):
        wcss += (distance(agg[i], cen)) ** 2
    return wcss


def get_all_wcss(clu, cen):
    wcss = 0.0
    for i in range(len(cen)):
        wcss += get_wcss(clu[i], cen[i])
    return wcss


def read_file():
    data = pd.read_csv("data.csv", header=None)

    first_column = data.iloc[:, 0]
    second_column = data.iloc[:, 1]
    third_column = data.iloc[:, 2]
    fourth_column = data.iloc[:, 3]

    iterations = [0 for _ in range(9)]
    aggregate = [[None for _ in range(4)] for _ in range(150)]
    for i in range(len(first_column)):
        aggregate[i] = [first_column[i], second_column[i], third_column[i], fourth_column[i], 0]

    # means = 3
    # centroids = place_centroid(means, aggregate)
    # centroids1 = loop(means, centroids, aggregate)
    wcsss = [0.0 for _ in range(9)]
    for i in range(2, 11):
        means = i
        print("Teraz dla k = " + str(means) + "\n")
        centroids = place_centroid(means, aggregate)
        centroids1 = loop(means, centroids, aggregate)
        clusters1 = cluster(means, centroids1, aggregate)
        colors = color(means, clusters1)
        if means == 3:
            aggregations(means, clusters1, centroids1, colors)
        iterations[i - 2] = temp
        wcsss[i - 2] = get_all_wcss(clusters1, centroids1)

    show_iterations(iterations)

    show_wcss(wcsss)


read_file()
