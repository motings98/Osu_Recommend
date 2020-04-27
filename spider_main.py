# coding=utf-8
import requests
from bs4 import BeautifulSoup
import re
import json
from lib_data import OsuPlayer
from lib_data import Beatmap
import lib_data
import Web_api
import random
import os


def readinPlayersList(country_list,country):   # 读取lib_data中的country_list后，逐个分析文件，注意调用时是从lib_data里调用的
        list_path = "./lib/userInfo/osu_ranking_list_%s.txt" % country  # 逐个读取文件
        readinPlayerInfo(list_path)


def readinPlayerInfo(country):    # 读取已经存放在lib/userInfo的用户列表数据，并逐个调用readinPLayerInfo函数
    print ("==================================================")
    file = open("./lib/userInfo/osu_ranking_list_%s.txt" % country, "r", encoding='utf-8')
    line = file.readline()
    while line:
        ran = random.randint(0,20)
        if ran != 10:
            line = file.readline()
            continue
        url = line.split(":", 1)[1]   # 获取单行数据里冒号后的信息，即玩家所对应的的url
        print("Player:" + line.split(":", 1)[0])
        content = getPlayerInfo(url)
        filename = content[0]["username"]
        lib_data.fileWritein("./lib/userInfo/%s/%s.json" % (country, filename), json.dumps(content,indent = 4))

        print("Player:" + filename + " Successfully Write in")

        line = file.readline()
    file.close()


def getBestplays(user_url):   # bp数据只能取到前100个，共两页 每页50个，由于数据不多，只传入玩家url
    print("Getting Best Plays ...")
    bp_list = []
    for i in range(2):
        bp_request = user_url + lib_data.bp_api % (i*50)   # 生成获取bp的api
        bp_content = lib_data.getJsonInfo(bp_request)
        for j in range(len(bp_content)):
            beatmapset_id = bp_content[j].get("beatmapset")["id"]
            beatmap_id = bp_content[j].get("beatmap")["id"]
            acc = bp_content[j]["accuracy"]
            pp = bp_content[j]["pp"]
            percentage = bp_content[j].get("weight")["percentage"]
            mods = bp_content[j]["mods"]
            date = bp_content[j]["created_at"]
            info_dict = {}    # 每一项字典里包含map信息，acc，pp及权重，使用的mod及创建日期
            info_dict["beatmapset_id"] = beatmapset_id
            info_dict["beatmap_id"] = beatmap_id
            info_dict["acc"] = acc
            info_dict["pp"] = pp
            info_dict["percentage"] = percentage
            info_dict["mods"] = mods
            info_dict["date"] = date
            bp_list.append(info_dict)

    return bp_list   # 2020/4/13 用print(getMostplayed("https://osu.ppy.sh/users/8179335"))测试无误


def getMostplayed(user_url, start_page, end_page):   # 如果返回的most_content为空（即没有足够的Most played maps），则中断循环
    print("Getting Most Played ...")
    most_played_list = []     # 传入的url是玩家的url
    for i in range(start_page,end_page):  # 从start_page页开始，获取到end_page页，每一页有50项
        most_played_request = user_url + lib_data.most_played_api % (i*50)     # 生成请求用api

        most_played_content = lib_data.getJsonInfo(most_played_request)

        '''  以下为异常处理源代码 现已被封装进lib_data，函数名为getJsonInfo()
        request_finished = False
        try_time = 1
        while not request_finished and (try_time <= 10):
            try:
                print("No.%d data is being processed, " % i + "try time: %d" % try_time)
                r = requests.get(most_played_request, timeout=15)
                r.raise_for_status()
                request_finished = True
                most_played_content = json.loads(r.text)  # most_played_content现在是List
            except Exception as e:
                try_time += 1
                print(e)
        '''
        if len(most_played_content) == 0:
            break

        for j in range(len(most_played_content)):

            beatmapset_id = most_played_content[j].get("beatmapset")["id"]
            beatmap_id = most_played_content[j].get("beatmap")["id"]
            count = most_played_content[j]["count"]
            info_dict = {}
            info_dict["beatmapset_id"] = beatmapset_id
            info_dict["beatmap_id"] = beatmap_id
            info_dict["count"] = count
            most_played_list.append(info_dict)
    return most_played_list   # 2020/4/13 用print(getMostplayed("https://osu.ppy.sh/users/8179335",0, 5))测试无误


def getRecentActivity(user_url):  # 最远能获取到当前时间30天内的 所以直接全部获取，只传入用户url
    print("Getting Recent Activity ...")
    recent_activity_list = []
    page_count = 0
    while True:
        recent_activity_request = user_url + lib_data.recentActicity_api % (page_count * 50)
        recent_activity_content = lib_data.getJsonInfo(recent_activity_request)
        page_count += 1
        if len(recent_activity_content) == 0 :    # 如果下一次获取到的content为空，中断循环
            break

        for j in range(len(recent_activity_content)):  # 如果是osu mode 的rank信息才执行
            if "mode" in recent_activity_content[j] and "rank" in recent_activity_content[j]:
                if recent_activity_content[j]["mode"] == "osu" and recent_activity_content[j]["type"] == "rank":
                    title = recent_activity_content[j].get("beatmap")["title"]
                    beatmap_url = lib_data.osu_main_url + recent_activity_content[j].get("beatmap")["url"]
                    date_set = recent_activity_content[j]["createdAt"]
                    rank = recent_activity_content[j]["rank"]
                    info_dict = {}
                    info_dict["title"] = title
                    info_dict["beatmap_url"] = beatmap_url
                    info_dict["date_set"] = date_set
                    info_dict["rank"] = rank
                    recent_activity_list.append(info_dict)
                else:
                    continue

            else:
                continue

    return recent_activity_list  # 2020/4/15 用print(getRecentActivity("https://osu.ppy.sh/users/4504101"))测试无误


def getRecent24h(user_url):
    print("Getting Recent 24h ...")
    recent24_list = []
    recent24_request = user_url + lib_data.recent24_api
    recent24_content = lib_data.getJsonInfo(recent24_request)

    for i in range(len(recent24_content)):
        mapset_id = recent24_content[i].get("beatmapset")["id"]
        map_id = recent24_content[i].get("beatmap")["id"]
        # ''' # 以下数据本用于未完成map的进度分析
        # object_hits = recent24_content[i].get("statistics")["count_300"] \
        #               + recent24_content[i].get("statistics")["count_100"] \
        #               + recent24_content[i].get("statistics")["count_50"] \
        #               + recent24_content[i].get("statistics")["count_miss"]
        # object_total = recent24_content[i].get("beatmap")["count_total"]
        # progress_rate = object_hits / object_total
        # '''
        acc = recent24_content[i]["accuracy"]
        mods = recent24_content[i]["mods"]
        rank = recent24_content[i]["rank"]
        info_dict = {}
        info_dict["mapset_id"] = mapset_id
        info_dict["map_id"] = map_id
        '''
        info_dict["object_hits"] = object_hits
        info_dict["object_total"] = object_total
        info_dict["progress_rate"] = progress_rate
        '''
        info_dict["acc"] = acc
        info_dict["mods"] = mods
        info_dict["rank"] = rank
        recent24_list.append(info_dict)

    return recent24_list


def getFavmaps(user_url):   # 点过红心的图上限是1000，而且一般没有那么多，所以一次性爬完
    print("Getting Favorite Maps ...")
    favmaps_list = []
    for i in range(20):
        favmaps_request = user_url + lib_data.favmaps_api % (i*50)
        favmaps_content = lib_data.getJsonInfo(favmaps_request)

        if len(favmaps_content) == 0:
            break

        for j in range(len(favmaps_content)):

            beatmapset_id = favmaps_content[j].get("beatmaps")[0]["beatmapset_id"]
            info_dict = {}
            info_dict["beatmapset_id"] = beatmapset_id
            favmaps_list.append(info_dict)

    return favmaps_list


'''
getPlayerInfo(url):
传入用户主页url，返回一个存有用户信息的列表
返回的list[0]为用户信息字典，list[1]为bp列表，列表中有100个字典
list[2]为打的最多的图列表，列表里有200个字典， list[3]为最近30天活动信息的列表，列表里n个字典
list[4]为24小时内上传成绩的图的列表，列表里有n个字典，list[5]是点过红心的图的列表，列表里有最多100个字典
'''


def getPlayerInfo(url):
    player_list = []
    user_info = Web_api.getUserInfo(url)
    user_name = user_info[0]["username"]
    joined_date = user_info[0]["join_date"]
    user_url = url
    total_ranked_score = user_info[0]["ranked_score"]
    total_score = user_info[0]["total_score"]
    accuracy = user_info[0]["accuracy"]
    play_count = user_info[0]["playcount"]
    total_hits = int(user_info[0]["count100"]) + int(user_info[0]["count300"]) + int(user_info[0]["count50"])
    total_pp = user_info[0]["pp_raw"]
    global_rank = user_info[0]["pp_rank"]
    country = user_info[0]["country"]
    country_rank = user_info[0]["pp_country_rank"]
    top_plays = getBestplays(url)
    most_played = getMostplayed(url, 1, 3)   # 取 即前200个
    recent_plays = getRecentActivity(url)
    recent_24h = getRecent24h(url)
    fav_maps = getFavmaps(url)
    user_info_pretty = {"username": user_name, "joined_date": joined_date, "user_url": user_url, "total_ranked_score":
                        total_ranked_score, "total_score": total_score, "accuracy": accuracy, "play_count": play_count
                        , "total_hits": total_hits, "total_pp": total_pp, "global_rank": global_rank, "county_rank":
                        country_rank, "country": country}

    player_list.append(user_info_pretty)
    player_list.append(top_plays)
    player_list.append(most_played)
    player_list.append(recent_plays)
    player_list.append(recent_24h)
    player_list.append(fav_maps)

    return player_list


def playerInfoUpdate_MultiDimensions(dirs):
    files = os.listdir(dirs)
    process = 0
    total = len(files)
    for filename in files:
        # print(filename.split(".")[0])
        print("Now(" + str((process+1)) + "/" + str(total) + "):" + filename.split(".")[0] )
        path = dirs + "/" + filename
        file_in = open(path, "r")
        original_info = json.load(file_in)
        file_out = open("lib/pptotal/" + filename, "w")
        info = lib_data.getJsonInfo("https://syrin.me/pp+/api/user/" + filename.split(".")[0])

        if info:
            original_info.get("user_stats")["Acc_total"] = info.get("user_data")["AccuracyTotal"]
            original_info.get("user_stats")["Aim_total"] = info.get("user_data")["AimTotal"]
            original_info.get("user_stats")["Flow_total"] = info.get("user_data")["FlowAimTotal"]
            original_info.get("user_stats")["Jump_total"] = info.get("user_data")["JumpAimTotal"]
            original_info.get("user_stats")["Speed_total"] = info.get("user_data")["SpeedTotal"]
            original_info.get("user_stats")["Stamina_total"] = info.get("user_data")["StaminaTotal"]

            file_out.write(json.dumps(original_info, indent=4, separators=(',', ':')))
            process += 1
        else:
            print("Player Info Update Failed!")
            process += 1


def UpdatePlayerInfo():
    return 0

