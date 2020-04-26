import json
import random

from bs4 import BeautifulSoup
import requests
import time
import os

country_list = ["TEST","AU", "CA", "CN", "DE", "FR", "GB", "JP", "KR", "US"]

'''
NOTICE:
    json data:0 limit 50 - 0-49
              50 limit 50 - 50-99
'''

osu_main_url = "https://osu.ppy.sh"

user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0;) Gecko/20100101 Firefox/61.0",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                    ]



#  以下为调用用户数据接口的json api，其中offset为从第几条开始查看的序号，limit为单次调用显示最大的条目数，最大为50
most_played_api = "/beatmapsets/most_played?offset=%d&limit=50"      # 游玩次数最多的图，数量不限
bp_api = "/scores/best?mode=osu&offset=%d&limit=50"                  # best performance， 最多能取到前100个
recentActicity_api = "/recent_activity?offset=%d&limit=50"           # recent activity, 数量不限
favmaps_api = "/beatmapsets/favourite?offset=%d&limit=50"            # 点过红心的图 上限100
recent24_api = "/scores/recent?mode=osu&offset=0&limit=50"                     # 最近24小时打完并上传成绩的图


def jsonViewer(url):             # 获取json，并规格化存入到本地文件中
    r = requests.get(url)
    temp = json.loads(r.text)
    content = json.dumps(temp, sort_keys=True, indent=4, separators=(',', ':'))
    o = open('json_tmep.txt', 'a+', encoding='utf-8')
    o.write(content)
    o.close()




def jsonPrettify(str):
    content = json.dumps(str, sort_keys=True, indent=4, separators=(',', ':'))
    return content


def htmlViewer(url):             # 获取html，并规格化存入到本地文件中
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    demo = r.text
    soup = BeautifulSoup(demo, "html.parser")
    f = open("html_temp.txt", "a+", encoding='utf-8')
    f.write(soup.prettify())
    f.close()





def fileWritein(filename,content):        # 写文件，参数为 文件名，内容
    f = open(filename, "a+", encoding='utf-8')
    f.write(content)
    f.close()


# limit最高只能是50，offset从0开始，由循环控制
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


def getJsonInfo(url,params = None):
    request_finished = False
    try_time = 1
    content = []
    while not request_finished and (try_time <= 10):
        try:
            kv = {"user_agent" : "Mozilla/5.0"}
            kv['User-Agent'] = random.choice(user_agent_list)
            print("try time : %d" % try_time)
            r = requests.get(url, params = params, headers = kv, timeout = 15)
            r.raise_for_status()
            request_finished = True
            content = json.loads(r.text)  # 通过json.loads将content类型转化为List
        except Exception as e:
            try_time += 1
            print(e)
            if "429" in str(e):
                print("Sleeping....")
                time.sleep(10)

    return content

a = OsuPlayer.__init__()
