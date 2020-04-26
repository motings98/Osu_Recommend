import requests
from bs4 import BeautifulSoup
import re
import json
import lib_data

'''
url = "https://osu.ppy.sh/rankings/osu/performance?page=1#scores"

r = requests.get(url)
demo = r.text
soup = BeautifulSoup(demo, "html.parser")

for info in soup.find_all('a', 'ranking-page-table__user-link-text js-usercard'):
    print(info.get('href'))
    print(info.string)

# tag_a = soup.find_all('a', 'ranking-page-table__user-link-text js-usercard')
'''


class Beatmap:
    def __init__(self, diff_id, beatmapset_id, star_rating, diff_name, total_length, hit_length,
                 bpm, cs, hp, od, ar, playcount, passcount, count_circles, count_sliders,
                 count_spinners, url, title, artist, creator, creator_id, favorite_count,
                 source, status):
        self.diff_id = diff_id
        self.beatmapset_id = beatmapset_id
        self.star_rating = star_rating
        self.diff_name = diff_name
        self.total_length = total_length
        self.hit_length = hit_length
        self.bpm = bpm
        self.cs = cs
        self.hp = hp
        self.od = od
        self.ar = ar
        self.playcount = playcount
        self.passcount = passcount
        self.count_circles = count_circles
        self.count_sliders = count_sliders
        self.count_spinners = count_spinners
        self.url = url
        self.title = title
        self.artist = artist
        self.creator = creator
        self.creator_id = creator_id
        self.favorite_count = favorite_count
        self.source = source
        self.status = status



class OsuPlayer:

    def __init__(self, user_name, user_url, total_score_ranked, accuracy, play_count, total_score, total_hits,
                 total_pp, global_rank, country_rank, recent_plays, top_plays, most_played, recent_24h,
                 fav_maps):
        self.user_name = user_name
        self.user_url = user_url
        self.total_score_ranked = total_score_ranked
        self.accuracy = accuracy
        self.play_count = play_count
        self.total_score = total_score
        self.total_hits = total_hits
        self.total_pp = total_pp
        self.global_rank = global_rank
        self.country_rank = country_rank
        self.recent_plays = recent_plays
        self.top_plays = top_plays
        self.most_played = most_played
        self.recent_24h = recent_24h
        self.fav_maps = fav_maps

    def printInfo1(self):
        print(self.user_name, self.user_url)


osuplayer_us = []

'''
for line in open("test.txt"):
    result = line.split(":", 1)
    name = result[0]
    url = result[1]
    print(name, url)
'''


def readinPlayersList(country_list):
    for i in country_list:
        list_path = "./lib/userInfo/osu_ranking_list_%s" % i  # load files one by one
        readinPlayerInfo(list_path)


path = "./lib/userInfo/osu_ranking_list_AU.txt"


def readinPlayerInfo(path):
    file = open(path, "r", encoding='utf-8')
    line = file.readline()
    while line:
        # print(line, end='')  #
        url = line.split(":", 1)[1]

        getPlayerInfo(url)

        line = file.readline()
    file.close()


idke_url = "https://osu.ppy.sh/users/4650315"

bp_api_2 = "/scores/best?mode=osu&offset=51&limit=100"

most_api = "/beatmapsets/most_played?offset=%d&limit=50"


def getTopplays(bp_content):

    return 0


def getMostplayed(most_content, start_page, end_page):   # 如果返回的most_content为空（即没有足够的Most played maps），则中断循环
    for i in range(start_page,end_page):  # 从start_page页开始，获取到end_page页，每一页有50项
        return 0

def getRecentplayed(rp_content):

    return 0

def getRecent24h(r24_content):

    return 0

def getFavmaps(fav_content):

    return 0

def getPlayerInfo(surl):
    api_list = [surl + bp_api_1, surl + bp_api_2]

    r = requests.get(surl)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    osuplyer_soup = BeautifulSoup(r.text, "html.parser")
    user_info = json.loads(osuplyer_soup.find('script', {'id': 'json-user'}, {'type': 'application/json'}).get_text()).get("statistics")
    ranked_score = user_info['ranked_score']
    accuracy = user_info['hit_accuracy']
    play_count = user_info['play_count']
    total_score = user_info['total_score']
    total_hits = user_info['total_hits']
    total_pp = user_info['pp']
    global_rank = user_info.get('rank')['global']
    country_rank = user_info.get('rank')['country']
    recent_plays = []
    top_plays = {}
    most_played = []
    recent_24h = []
    fav_maps = []

    pp_stats = {}

    for part in range(2):
        bp_api_url = api_list[part]
        bp_response = requests.get(bp_api_url)
        bp_response.raise_for_status()
        bp_response.encoding = bp_response.apparent_encoding
        # map_info_head = json.loads(bp_soup.find('script', {'id': 'json-extras'}, {'type': 'application/json'}).get_text())

        bp_content = json.loads(bp_response.text)

        for i in range(0, len(bp_content)):
            diff_id = bp_content[i].get('beatmap')["id"]
            beatmapset_id = bp_content[i].get('beatmapset')["id"]
            star_rating = bp_content[i].get('beatmap')["difficulty_rating"]
            diff_name = bp_content[i].get('beatmap')["version"]
            total_length = bp_content[i].get('beatmap')["total_length"]
            hit_length = bp_content[i].get('beatmap')["hit_length"]
            bpm = bp_content[i].get('beatmap')["bpm"]
            cs = bp_content[i].get('beatmap')["cs"]
            hp = bp_content[i].get('beatmap')["drain"]
            od = bp_content[i].get('beatmap')["accuracy"]
            ar = bp_content[i].get('beatmap')["ar"]
            playcount = bp_content[i].get('beatmap')["playcount"]
            passcount = bp_content[i].get('beatmap')["passcount"]
            count_circles = bp_content[i].get('beatmap')["count_circles"]
            count_sliders = bp_content[i].get('beatmap')["count_sliders"]
            count_spinners = bp_content[i].get('beatmap')["count_spinners"]
            url = "https://osu.ppy.sh/beatmapsets/%s#osu/%s" % (beatmapset_id, diff_id)
            title = bp_content[i].get('beatmapset')["title"]
            artist = bp_content[i].get('beatmapset')["artist"]
            creator = bp_content[i].get('beatmapset')["creator"]
            creator_id = bp_content[i].get('beatmapset')["user_id"]
            favorite_count = bp_content[i].get('beatmapset')["favourite_count"]
            source = bp_content[i].get('beatmapset')["source"]
            status = bp_content[i].get('beatmapset')["status"]
            pp_stats["%s" % url] = bp_content[i]["pp"]

            top_plays.append(Beatmap(diff_id, beatmapset_id, star_rating, diff_name, total_length, hit_length, bpm,
                                     cs, hp, od, ar, playcount, passcount, count_circles, count_sliders, count_spinners,
                                     url, title, artist, creator, creator_id, favorite_count, source, status))

    top_plays = pp_stats   # top_play is a list


def PlayerInfo_Output(ranked_score, accuracy, play_count, total_score, total_hits, total_pp, global_rank,
                      country_rank, recent_plays, top_plays, most_played, recent_24h, fav_maps):
    fo = open()



        
    



    '''
    diff_id = map_info_head[0].get('beatmap')["id"]
    beatmapset_id = map_info_head[0].get('beatmapset')["id"]
    star_rating = map_info_head[0].get('beatmap')["difficult_ranting"]
    map_score = map_info_head[0]['score']
    print(star_rating)
    '''



readinPlayerInfo()






