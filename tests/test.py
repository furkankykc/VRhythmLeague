import matplotlib.pyplot as plt
import numpy as np


# from League.mixins import normpdf


def mean(array):
    return array.mean()


import math


def normpdf(x, mean, sd):
    var = float(sd) ** 2
    denom = (2 * math.pi * var) ** .5
    num = math.exp(-(float(x) - float(mean)) ** 2 / (2 * var))
    return num / denom


def normalized_sore(total_score, min_a, max_a) -> float:
    return (total_score - min_a) / (max_a - min_a)


def calculate_normal(total_score, array):
    min_a = array.min()
    max_a = array.max()
    len_a = array.size

    return normpdf(total_score, array.mean(), array.std())


def calc():
    array = np.random.rand(40023)
    array2 = np.multiply(array, 50)

    # sonuc = calculate_normal(0.9, array)
    print(array.mean())
    plt.plot(array2-array2.mean(), [calculate_normal(x, array2) for x in array2])
    plt.show()


calc()
