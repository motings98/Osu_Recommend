from bs4 import BeautifulSoup
import requests
import random
import pyttanko as osu
import sys
import lib_data
import json
import os
import numpy
import spider_main
import pickle

def Dict2List(dict):   # 将dict转化为list
    list = []
    for key in dict:
        list.append(dict[key])
    return list


def DimensionNormalize(dict_a, dict_b):
    for key in dict_a:
        if not key in dict_b:
            dict_b[key] = 0

    for key in dict_b:
        if not key in dict_a:
            dict_a[key] = 0

    print(dict_a)
    print(dict_b)

    list_a = []
    list_b = []

    for i in sorted(dict_a):
        list_a.append(dict_a[i])
    for i in sorted(dict_b):
        list_b.append(dict_b[i])

    print(list_a)
    print(list_b)


# test = open(lib_data.getBackPath(1) + "/UserInfo/matrix/user_matrix.pkl", "rb")










