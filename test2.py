import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def determinate_class(k, classes, new_point):
    # w przypadku sporu gatunek jest ustalany po najbliższym sąsiedzie
    race1 = 0
    race2 = 0
    race3 = 0
    for i in range(k):
        if classes[i] == 0:
            race1 += 1
        elif classes[i] == 1:
            race2 += 1
        else:
            race3 += 1

    if race1 == race2 == race3:
        # new_point[5] = random.randint(0,2)
        new_point[5] = classes[0]
    elif race1 > race2 and race1 > race3:
        new_point[5] = 0
    elif race2 > race1 and race2 > race3:
        new_point[5] = 1
    elif race3 > race2 and race3 > race1:
        new_point[5] = 2
    elif race1 == race2 and race1 > race3:
        for i in range(len(classes)):
            if classes[i] == 0:
                new_point[5] = 0
                break
            elif classes[i] == 1:
                new_point[5] = 1
                break
            else:
                continue
    elif race2 == race3 and race2 > race1:
        for i in range(len(classes)):
            if classes[i] == 1:
                new_point[5] = 1
                break
            elif classes[i] == 2:
                new_point[5] = 2
                break
            else:
                continue
    elif race3 == race1 and race3 > race2:
        for i in range(len(classes)):
            if classes[i] == 0:
                new_point[5] = 0
                break
            elif classes[i] == 2:
                new_point[5] = 2
                break
            else:
                continue
    return 0


def loop(k, training_data, new_point):
    for i in range(45):
        determinate_class(k, choose_k_neighbours(k, calculate_every_distance(training_data, new_point[i])),
                          new_point[i])


def loop_trait(k, training_data, new_point, tab1, tab2):
    for i in range(45):
        determinate_class(k, choose_k_neighbours(k, calculate_every_distance_trait(training_data, new_point[i], tab1,
                                                                                   tab2)), new_point[i])


def choose_k_neighbours(k, training_data):
    training_data.sort(key=lambda lam: lam[5])
    classing = [0.0 for _ in range(k)]
    for i in range(k):
        classing[i] = training_data[i][4]
        # print(classing)
    return classing  # gatunki najblizszych s


def calculate_every_distance(training_data, new_point):
    for i in range(105):
        training_data[i][5] = distance(training_data[i], new_point)
    return training_data


def calculate_every_distance_trait(training_data, new_point, tab1, tab2):
    for i in range(105):
        training_data[i][5] = distance_trait(training_data[i], new_point, tab1, tab2)
    return training_data


def distance(neighbour, new_point):
    return ((neighbour[0] - new_point[0]) ** 2 + (neighbour[1] - new_point[1]) ** 2 + (
                neighbour[2] - new_point[2]) ** 2 + (
                    neighbour[3] - new_point[3]) ** 2) ** 0.5


def distance_trait(neighbour, new_point, tab1, tab2):
    return ((neighbour[tab1] - new_point[tab1]) ** 2 + (neighbour[tab2] - new_point[tab2]) ** 2) ** 0.5


# def get_accuracy(test_data):
#     acc = [0 for _ in range(45)]
#     for i in range(len(test_data)):
#         acc[i] = test_data[i][5]
#     return acc
def get_accuracy(test_data):
    acc = [[0 for _ in range(2)] for _ in range(45)]
    for i in range(len(test_data)):
        for j in range(2):
            acc[i][j] = test_data[i][j + 4]
    return acc


def write_matrix(acc, string, par):
    # temp = acc
    # index = 1
    # for i in range(15):
    #     if temp < acc[i]:
    #         temp = acc[i]
    #         index = i + 1
    # if par:
    #     loop(index, training_data, test_data)
    #     mat = get_accuracy(test_data)
    # else:
    #     loop_trait(index, training_data, test_data, tab1, tab2)
    #     mat = get_accuracy(test_data)
    list_mat = [[0 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(15):
            if acc[(15 * i) + j][1] == i:
                list_mat[i][i] += 1
            else:
                list_mat[i][acc[15 * i + j][1]] += 1

    print(par, "sąsiadów")
    print(string + "\n")
    # print("klasa faktyczna:")
    # for i in range(45):
    #     print(acc[i][0], end=",")
    # print("\nklasa rozpoznana: ")
    # for i in range(45):
    #     print(acc[i][1], end=",")
    for i in range(3):
        print(list_mat[i][0], list_mat[i][1], list_mat[i][2])
    print("\n\n\n")


def calculate_accuracy(matrix):
    acc = 0.0
    right = 0
    allin = 45
    for i in range(45):
        if matrix[i][0] == matrix[i][1]:
            right = right + 1
    acc = (right / allin) * 100
    return acc


def show_graph(y_acc, title):
    plt.rcParams.update({'font.size': 20})
    plt.figure(figsize=(10, 7))
    plt.ylabel("Dokładność [%]")
    plt.ylim(0, 105)
    k = np.array([i for i in range(1, 16)])
    plt.xticks(np.arange(1, 16, step=1))
    plt.yticks(np.arange(0, 101, step=20))
    plt.xlabel("k")
    plt.title(title)
    plt.bar(k, y_acc)

    plt.show()


def read_file():
    file_train = pd.read_csv("data_train.csv", header=None)

    first_column_train = file_train.iloc[:, 0]
    second_column_train = file_train.iloc[:, 1]
    third_column_train = file_train.iloc[:, 2]
    fourth_column_train = file_train.iloc[:, 3]
    fifth_column_train = file_train.iloc[:, 4]

    file_test = pd.read_csv("data_test.csv", header=None)

    first_column_test = file_test.iloc[:, 0]
    second_column_test = file_test.iloc[:, 1]
    third_column_test = file_test.iloc[:, 2]
    fourth_column_test = file_test.iloc[:, 3]
    fifth_column_test = file_test.iloc[:, 4]

    flag1 = 0
    flag2 = 0
    flag3 = 0
    flag4 = 0
    flag5 = 0
    flag6 = 0
    flag7 = 0
    acc_copy1 = [[3 for _ in range(2)] for _ in range(15)]
    acc_copy2 = [[3 for _ in range(2)] for _ in range(15)]
    acc_copy3 = [[3 for _ in range(2)] for _ in range(15)]
    acc_copy4 = [[3 for _ in range(2)] for _ in range(15)]
    acc_copy5 = [[3 for _ in range(2)] for _ in range(15)]
    acc_copy6 = [[3 for _ in range(2)] for _ in range(15)]
    acc_copy7 = [[3 for _ in range(2)] for _ in range(15)]

    training_data = [[None for _ in range(6)] for _ in range(105)]
    test_data = [[None for _ in range(6)] for _ in range(45)]
    for i in range(len(first_column_train)):
        training_data[i] = [first_column_train[i], second_column_train[i], third_column_train[i],
                            fourth_column_train[i], fifth_column_train[i], 0.0]
    for i in range(len(first_column_test)):
        test_data[i] = [first_column_test[i], second_column_test[i], third_column_test[i], fourth_column_test[i],
                        fifth_column_test[i], 3]
    knn_acc1 = [0.0 for _ in range(15)]
    knn_acc2 = [0.0 for _ in range(15)]
    knn_acc3 = [0.0 for _ in range(15)]
    knn_acc4 = [0.0 for _ in range(15)]
    knn_acc5 = [0.0 for _ in range(15)]
    knn_acc6 = [0.0 for _ in range(15)]
    knn_acc7 = [0.0 for _ in range(15)]
    current_max_acc_1 = knn_acc1[0]
    current_max_acc_2 = knn_acc2[0]
    current_max_acc_3 = knn_acc3[0]
    current_max_acc_4 = knn_acc4[0]
    current_max_acc_5 = knn_acc5[0]
    current_max_acc_6 = knn_acc6[0]
    current_max_acc_7 = knn_acc7[0]
    for i in range(15):
        loop(i + 1, training_data, test_data)
        matrix1 = get_accuracy(test_data)
        loop_trait(i + 1, training_data, test_data, 0, 1)
        matrix2 = get_accuracy(test_data)
        loop_trait(i + 1, training_data, test_data, 0, 2)
        matrix3 = get_accuracy(test_data)
        loop_trait(i + 1, training_data, test_data, 0, 3)
        matrix4 = get_accuracy(test_data)
        loop_trait(i + 1, training_data, test_data, 1, 2)
        matrix5 = get_accuracy(test_data)
        loop_trait(i + 1, training_data, test_data, 1, 3)
        matrix6 = get_accuracy(test_data)
        loop_trait(i + 1, training_data, test_data, 2, 3)
        matrix7 = get_accuracy(test_data)
        knn_acc1[i] = calculate_accuracy(matrix1)
        knn_acc2[i] = calculate_accuracy(matrix2)
        knn_acc3[i] = calculate_accuracy(matrix3)
        knn_acc4[i] = calculate_accuracy(matrix4)
        knn_acc5[i] = calculate_accuracy(matrix5)
        knn_acc6[i] = calculate_accuracy(matrix6)
        knn_acc7[i] = calculate_accuracy(matrix7)
        if calculate_accuracy(matrix1) > current_max_acc_1:
            acc_copy1 = matrix1.copy()
            flag1 = i + 1
            current_max_acc_1 = knn_acc1[i]
        if calculate_accuracy(matrix2) > current_max_acc_2:
            acc_copy2 = matrix2.copy()
            flag2 = i + 1
            current_max_acc_2 = knn_acc2[i]
        if calculate_accuracy(matrix3) > current_max_acc_3:
            acc_copy3 = matrix3.copy()
            flag3 = i + 1
            current_max_acc_3 = knn_acc3[i]
        if calculate_accuracy(matrix4) > current_max_acc_4:
            acc_copy4 = matrix4.copy()
            flag4 = i + 1
            current_max_acc_4 = knn_acc4[i]
        if calculate_accuracy(matrix5) > current_max_acc_5:
            acc_copy5 = matrix5.copy()
            flag5 = i + 1
            current_max_acc_5 = knn_acc5[i]
        if calculate_accuracy(matrix6) > current_max_acc_6:
            acc_copy6 = matrix6.copy()
            flag6 = i + 1
            current_max_acc_6 = knn_acc6[i]
        if calculate_accuracy(matrix7) > current_max_acc_7:
            acc_copy7 = matrix7.copy()
            flag7 = i + 1
            current_max_acc_7 = knn_acc7[i]

    # write_matrix(knn_acc1, "Wszystkie cechy", False, training_data, test_data, 0, 0)
    # write_matrix(knn_acc1, "Długość działki kielicha do szerokości działki kielicha", True, training_data,
    #              test_data, 0, 1)
    # write_matrix(knn_acc1, "Długość działki kielicha do długości płatka", True, training_data,
    #              test_data, 0, 2)
    # write_matrix(knn_acc1, "Długość działki kielicha do szerokości płatka", True, training_data,
    #              test_data, 0, 3)
    # write_matrix(knn_acc1, "Szerokość działki kielicha do długości płatka", True, training_data,
    #              test_data, 1, 2)
    # write_matrix(knn_acc1, "Szerokość działki kielicha do szerokości płatka", True, training_data,
    #              test_data, 1, 3)
    # write_matrix(knn_acc1, "Długość płatka do szerokości płatka", True, training_data,
    #              test_data, 2, 3)
    write_matrix(acc_copy1, "Wszystkie cechy", flag1)
    write_matrix(acc_copy2, "Długość działki kielicha do szerokości działki kielicha", flag2)
    write_matrix(acc_copy3, "Długość działki kielicha do długości płatka", flag3)
    write_matrix(acc_copy4, "Długość działki kielicha do szerokości płatka", flag4)
    write_matrix(acc_copy5, "Szerokość działki kielicha do długości płatka", flag5)
    write_matrix(acc_copy6, "Szerokość działki kielicha do szerokości płatka", flag6)
    write_matrix(acc_copy7, "Długość płatka do szerokości płatka", flag7)

    show_graph(knn_acc1, "Wszystkie dostępne cechy")
    show_graph(knn_acc2, "Długość działki kielicha do szerokości działki kielicha")
    show_graph(knn_acc3, "Długość działki kielicha do długości płatka")
    show_graph(knn_acc4, "Długość działki kielicha do szerokości płatka")
    show_graph(knn_acc5, "Szerokość działki kielicha do długości płatka")
    show_graph(knn_acc6, "Szerokość działki kielicha do szerokości płatka")
    show_graph(knn_acc7, "Długość płatka do szerokości płatka")


read_file()