import os
import json
import lib_data
from numpy import *
import math

def userStatsAnalyse(user_data):
    return 0


def VectorMultiply(v1, v2):         # 计算向量数乘结果
    if len(v1) != len(v2):
        return "Error"

    result = 0
    for i in range(len(v1)):
        result += v1[i] * v2[i]

    return result


def VectorLength(v):                # 计算向量长度
    length = 0
    for i in range(len(v)):
        length += v[i]*v[i]

    return sqrt(length)


def CalUserDiff(v1, v2):     # 传入两个用户的六维向量，范围对应向量的相差倍率,返回对应相差倍率的六维向量
    v_result = array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    for i in range(6):
        if v1[i] > v2[i]:
            v_result[i] = v2[i] / v1[i]
        if v1[i] < v2[i]:
            v_result[i] = v1[i] / v2[i]
        if v1[i] == v2[i]:
            v_result[i] = 1

    return v_result


def CalUserSimilarity_Local(user1, user2):      # 计算用户相似度，传入两个用户所对应的json文件load过后的字典
    # 先获取两个用户的六维向量，其中vector = [acc ，小圈，flow，jump，speed，stamina]
    v1 = array([user1["user_stats"]["Acc_total"], user1["user_stats"]["Precision_total"], user1["user_stats"]["Flow_total"],
         user1["user_stats"]["Jump_total"], user1["user_stats"]["Speed_total"], user1["user_stats"]["Stamina_total"]])

    v2 = array([user2["user_stats"]["Acc_total"], user2["user_stats"]["Precision_total"], user2["user_stats"]["Flow_total"],
         user2["user_stats"]["Jump_total"], user2["user_stats"]["Speed_total"], user2["user_stats"]["Stamina_total"]])

    print(v1)
    print(v2)

    multi = 1

    v_diff = CalUserDiff(v1, v2)

    print(v_diff)
    average_diff = mean(v_diff)

    multi *= average_diff

    similarity = VectorMultiply(v1, v2) / (VectorLength(v1) * VectorLength(v2))

    return similarity * multi


def CalUserSimilarity_Web(user1, user2):      # 计算用户相似度，传入两个用户所对应的json文件load过后的字典
    # 先获取两个用户的六维向量，其中vector = [acc ，小圈，flow，jump，speed，stamina]
    v1 = array([user1["user_data"]["AccuracyTotal"], user1["user_data"]["PrecisionTotal"], user1["user_data"]["FlowAimTotal"],
         user1["user_data"]["JumpAimTotal"], user1["user_data"]["SpeedTotal"], user1["user_data"]["StaminaTotal"]])

    v2 = array([user2["user_data"]["AccuracyTotal"], user2["user_data"]["PrecisionTotal"], user2["user_data"]["FlowAimTotal"],
         user2["user_data"]["JumpAimTotal"], user2["user_data"]["SpeedTotal"], user2["user_data"]["StaminaTotal"]])

    print(v1)
    print(v2)

    multi = 1

    v_diff = CalUserDiff(v1, v2)

    print(v_diff)
    average_diff = mean(v_diff)

    multi *= average_diff

    similarity = VectorMultiply(v1, v2) / (VectorLength(v1) * VectorLength(v2))

    return similarity * multi
