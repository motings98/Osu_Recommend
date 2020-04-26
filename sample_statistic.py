import matplotlib.pyplot as plt
import os
import json


def statistic_user_info(folder):
    above_300000 = 0
    between_200000_299999 = 0
    between_100000_199999 = 0
    between_50000_99999 = 0
    between_20000_49999 = 0
    between_10000_19999 = 0
    between_5000_9999 = 0
    between_2000_4999 = 0
    between_1000_1999 = 0
    between_500_999 = 0
    between_200_499 = 0
    between_50_199 = 0
    between_1_49 = 0

    gap_300000_above = 0
    gap_200000_299999 = 0
    gap_100000_199999 = 0
    gap_100000_under = 0
    fileList = os.listdir(folder)
    for file in fileList:
        info = json.load(open("lib/newtotal/" + file))
        if int(info.get("user_stats")["global_rank"]) > 300000:
            above_300000 += 1
            gap_300000_above += 1

        if 200000 <= int(info.get("user_stats")["global_rank"]) <= 299999:
            between_200000_299999 += 1
            gap_200000_299999 += 1

        if 100000 <= int(info.get("user_stats")["global_rank"]) <= 199999:
            between_100000_199999 += 1
            gap_100000_199999 += 1

        if 50000 <= int(info.get("user_stats")["global_rank"]) <= 99999:
            between_50000_99999 += 1
            gap_100000_under += 1

        if 20000 <= int(info.get("user_stats")["global_rank"]) <= 49999:
            between_20000_49999 += 1
            gap_100000_under += 1

        if 10000 <= int(info.get("user_stats")["global_rank"]) <= 19999:
            between_10000_19999 += 1
            gap_100000_under += 1

        if 5000 <= int(info.get("user_stats")["global_rank"]) <= 9999:
            between_5000_9999 += 1
            gap_100000_under += 1

        if 2000 <= int(info.get("user_stats")["global_rank"]) <= 4999:
            between_2000_4999 += 1
            gap_100000_under += 1

        if 1000 <= int(info.get("user_stats")["global_rank"]) <= 1999:
            between_1000_1999 += 1
            gap_100000_under += 1

        if 500 <= int(info.get("user_stats")["global_rank"]) <= 999:
            between_500_999 += 1
            gap_100000_under += 1

        if 200 <= int(info.get("user_stats")["global_rank"]) <= 499:
            between_200_499 += 1
            gap_100000_under += 1

        if 50 <= int(info.get("user_stats")["global_rank"]) <= 199:
            between_50_199 += 1
            gap_100000_under += 1

        if 1 <= int(info.get("user_stats")["global_rank"]) <= 49:
            between_1_49 += 1
            gap_100000_under += 1

    return between_1_49, between_50_199, between_200_499, between_500_999, between_1000_1999, between_2000_4999, \
        between_5000_9999, between_10000_19999, between_20000_49999, between_50000_99999, between_100000_199999, \
        between_200000_299999, above_300000, gap_100000_under, gap_100000_199999, gap_200000_299999, gap_300000_above


def getGlobalList(folder):
    global_list = []
    fileList = os.listdir(folder)
    for file in fileList:
        info = json.load(open("lib/newtotal/" + file))
        global_list.append(int(info.get("user_stats")["global_rank"]))
        # global_list.append(info.get("user_stats")["global_rank"])
    return global_list


# list = statistic_user_info("./lib/newtotal")
gloabl_list_a = getGlobalList("./lib/newtotal")

list_h = [1, 3, 11, 13, 31, 58, 116, 197, 631, 658, 874, 438, 411]
list_l = [1719, 874, 438, 411]
list_l_x = ["under 100000", "100000-199999", "200000-300000", "above 300000"]

# plt.bar( x= list_l_x, height= list_l )

#list_sample = [1,1,3,3,5,7,5,9,3,6,4,7,5]
#plt.hist(x= list_sample , bins= 5)
plt.hist(x=gloabl_list_a, bins=30, color="steelblue", edgecolor="black")
plt.xlabel("全球排名")
plt.ylabel("玩家数量")
plt.title("模型启动样本分布")
plt.rcParams['font.sans-serif']=['SimHei']  # 用来正常显示中文标签
plt.show()

