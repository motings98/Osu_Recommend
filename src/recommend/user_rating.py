import os
import json
from numpy import *
import math
import sys
import lib_data
import spider_main

# Pearson Correlation Coefficient : corrcoef[0][1]
# Euclidean Distance : linalg.norm


# 计算欧氏距离，如果trans为True，则将所有数值除100
def CalEuclideanDistance(v1, v2, trans = None):
    if trans:
        for i in range(len(v1)):
            v1[i] /= 100
        for i in range(len(v2)):
            v2[i] /= 100
    # print(v1, v2)
    v3 = []
    for i in range(len(v1)):
        v3.append(v1[i] - v2[i])
    ed = linalg.norm(v3)
    return ed


# 将欧氏距离转化为向量相似度
def EuclideanDistance2Similarity(ed):
    similarity = 100 - ((100*ed)/sqrt(2))
    return similarity


# 将dict转化为list
def Dict2List(dict):
    list = []
    for key in dict:
        list.append(dict[key])
    return list


# 返回各mod成绩占总pp的【字典】, 如果第二个参数为True，则返回占比
def userModsAnalyse(user_data, return_type = None):
    ''' mods = {"HR": 0, "HD": 0, "DT": 0, "EZ": 0, "FL": 0, "None": 0,
            "HDHR": 0, "HDDT": 0 , "HDFL": 0, "HDEZ": 0, "EZFL": 0, "HRFL": 0, "DTFL": 0, "EZDT": 0, "EZHD": 0, "HRDT": 0,
            "HDHRDT": 0 , "HDHRFL": 0, "HRDTFL:":0, "HDDTFL": 0, "EZHDDT": 0, "EZHDFL": 0, "EZDTFL": 0,
            "HDHRDTFL":0 , "EZHDDTFL": 0} '''   # 脑子抽风写了这么一大堆，花了好半天，结果根本用不到呜呜呜

    mods = {"None": 0}

    for scores in user_data["best_plays"]:
        if scores["mods"]:
            mod_combined = ""
            multiplier = 1
            for score_mod in scores["mods"]:

                if score_mod == "HD":
                    score_mod = ""

                if score_mod == "NF":
                    multiplier /= 0.9
                    continue

                if score_mod == "SO":
                    multiplier /= 0.95
                    continue

                if score_mod == "NC":
                    score_mod = "DT"

                if score_mod == "SD" or score_mod == "PF":
                    continue

                mod_combined += score_mod

            if not mod_combined:
                mods["None"] += scores["pp"] * (scores["percentage"] / 100)
                continue

            if not mod_combined in mods:
                mods[mod_combined] = 0

            mods[mod_combined] += scores["pp"] * (scores["percentage"] / 100) * multiplier

        else:
            mods["None"] += scores["pp"] * (scores["percentage"] / 100 )

    # print(user_data["user_stats"]["username"] + "统计后的Mod数据:" + str(mods))

    if return_type :
        for key in mods:
            mods[key] /= float(user_data["user_stats"]["total_pp"])
            mods[key] *= 100

    return mods


# 将两个向量维数统一
def userModsDimensionNormalize(mod1, mod2):

    for single_mod in mod1:
        if not single_mod in mod2:
            mod2[single_mod] = 0
    for single_mod in mod2:
        if not single_mod in mod1:
            mod1[single_mod] = 0

    # print(mod1)
    # print(mod2)

    list_a = []
    list_b = []

    for i in sorted(mod1):
        list_a.append(mod1[i])
    for i in sorted(mod2):
        list_b.append(mod2[i])

    # print(list_a)
    # print(list_b)

    return list_a,list_b


# 计算向量数乘结果
def VectorMultiply(v1, v2):
    if len(v1) != len(v2):
        return "Error"

    result = 0
    for i in range(len(v1)):
        result += v1[i] * v2[i]

    return result


# 计算向量长度
def VectorLength(v):
    length = 0
    for i in range(len(v)):
        length += v[i]*v[i]

    return sqrt(length)


# 传入两个用户的六维向量，返回对应相差倍率的六维向量
def CalUserDiff(v1, v2):
    v_result = array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    for i in range(6):
        if v1[i] > v2[i]:
            v_result[i] = v2[i] / v1[i]
        if v1[i] < v2[i]:
            v_result[i] = v1[i] / v2[i]
        if v1[i] == v2[i]:
            v_result[i] = 1

    return v_result


# 计算两个向量的余弦相似度
def CalCosineSimilarity(v1, v2):
    return VectorMultiply(v1, v2) / (VectorLength(v1) * VectorLength(v2))


# 传入两个mod向量或列表，计算相似度（目前采用欧氏距离）
def CalModSimilarity(v1, v2):
    """
    :param v1:
    :param v2:
    :return:
    """
    ed = CalEuclideanDistance(v1, v2)     # 欧氏距离
    # pcc = corrcoef(v1, v2)[0][1] # 皮尔逊
    # cs = CalCosineSimilarity(v1, v2)
    # print("欧氏距离：" + str(ed))
    # print("皮尔逊相关系数" + str(pcc))
    # print("余弦相似度" + str(cs))
    return ed


# 传入两个用户的user_stats，计算most played重合度
def CalMostPlayedCoincidence(u1, u2):
    return 0


# 计算fav maps重合
def CalFavCoincidence(u1, u2):
    """
    计算fav maps里的重合
    :param u1: 用户1的完整数据
    :param u2: 用户2的完整数据
    :return: 重合数
    """
    u1favs = []
    u2favs = []
    coincidence = []
    for map in u1["fav_maps"]:
        u1favs.append(map["beatmapset_id"])
    for map in u2["fav_maps"]:
        u2favs.append(map["beatmapset_id"])
    count = len(set(u1favs) & set(u2favs))
    return count


# 计算用户相似度的主函数
def CalUserSimilarity_Local(user1, user2, Debug = None):
    """
    :param user1: 用户1的用户名(string)
    :param user2: 用户2的用户名(string)
    :return: 用户相似度(float)
    """

    user1 = user1.lower()          # 忽略大小写，其实就是全部转化成小写
    user2 = user2.lower()
    filelist = os.listdir(lib_data.user_info_dir)
    for i in range(len(filelist)):
         filelist[i] = filelist[i].lower()

    if (user1 + ".json") in filelist:   # 如果在本地有数据，则直接load，没有的话从web获取
        f1 = open(lib_data.user_info_dir + str(user1) + ".json")
        user1 = json.load(f1)
    else:
        print("Getting " + user1 + " from Web....")
        user1 = spider_main.getPlayerInfo(user1)
    if (user2 + ".json") in filelist:
        f2 = open(lib_data.user_info_dir + str(user2) + ".json")
        user2 = json.load(f2)
    else:
        print("Getting " + user2 + " from Web....")
        user2 = spider_main.getPlayerInfo(user2)

    u1mod = userModsAnalyse(user1, True)
    u2mod = userModsAnalyse(user2, True)

    # 先获取两个用户的六维向量，其中vector = [acc ，小圈，flow，jump，speed，stamina]

    v1 = array([user1["user_stats"]["Acc_total"], user1["user_stats"]["Precision_total"], user1["user_stats"]["Flow_total"],
         user1["user_stats"]["Jump_total"], user1["user_stats"]["Speed_total"], user1["user_stats"]["Stamina_total"]])
    v2 = array([user2["user_stats"]["Acc_total"], user2["user_stats"]["Precision_total"], user2["user_stats"]["Flow_total"],
         user2["user_stats"]["Jump_total"], user2["user_stats"]["Speed_total"], user2["user_stats"]["Stamina_total"]])

    avg_coe = [0.1, 0.1, 0.3, 0.15, 0.15, 0.2]
    # ------- acc,precision,flow,jump,speed,stamina -------

    u1modded, u2modded = userModsDimensionNormalize(u1mod, u2mod)
    mod_euclid = CalEuclideanDistance(u1modded, u2modded, True)
    mod_similarity = EuclideanDistance2Similarity(mod_euclid)
    fav_similarity = 1 + ( CalFavCoincidence(user1, user2) * 0.03 )

    multi = 1   # 初始倍率：1
    v_diff = CalUserDiff(v1, v2)

    average_diff = 0
    for i in range(6):
        average_diff += v_diff[i] * avg_coe[i]

    multi = multi * average_diff * mod_similarity * fav_similarity

    if Debug:
        print(user1["user_stats"]["username"] + "的pp+数据为: " + str(v1))
        print(user2["user_stats"]["username"] + "的pp+数据为: " + str(v2))
        print("pp+数据倍率差为: " + str(v_diff))
        print("平均倍率差: "+ str(average_diff))
        print("mod相似度为: " + str(mod_similarity))
        print("fav相似度为: " + str(fav_similarity))


    return multi

''' 已废除，被整合了
def CalUserSimilarity_Web(user1, user2):      # 计算用户相似度，传入两个用户所对应的json文件load过后的字典
    # 先获取两个用户的六维向量，其中vector = [acc ，小圈，flow，jump，speed，stamina]
    v1 = array([user1["user_data"]["AccuracyTotal"], user1["user_data"]["PrecisionTotal"], user1["user_data"]["FlowAimTotal"],
         user1["user_data"]["JumpAimTotal"], user1["user_data"]["SpeedTotal"], user1["user_data"]["StaminaTotal"]])

    v2 = array([user2["user_data"]["AccuracyTotal"], user2["user_data"]["PrecisionTotal"], user2["user_data"]["FlowAimTotal"],
         user2["user_data"]["JumpAimTotal"], user2["user_data"]["SpeedTotal"], user2["user_data"]["StaminaTotal"]])
    print(v1)
    print(v2)
    multi = 1         # 默认倍率是1
    v_diff = CalUserDiff(v1, v2)        # 计算六维向量的相差倍率
    print(v_diff)
    average_diff = mean(v_diff)         # 取平均值
    multi *= average_diff               # 倍率 = 六维数据均值的倍率差
    similarity = VectorMultiply(v1, v2) / (VectorLength(v1) * VectorLength(v2))   # 余弦相似度
    return similarity * multi           # 返回 （余弦相似度 * 倍率）
'''



