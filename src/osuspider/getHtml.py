import requests
from bs4 import BeautifulSoup
import re

main_url = "https://osu.ppy.sh"
ranking_list_api = "https://osu.ppy.sh/rankings/osu/performance?country=US&page="


def getHomePage(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        html2txt = str(r.text)  # html content is fully transformed to str
        fo = open('osu_homepage.html', 'w', encoding='utf-8')
        fo.write(html2txt)
        print("getHomePage function finished!")
    except:
        print("Unable to run getHomePage function!")


def getRankingList(url):

    count = 0
    osuplayer_US = []
    for page in range(1, 201):

        real_url = url + str(page) + "#scores"
        # print(real_url)
        request_finished = False
        try_times = 1
        while not request_finished and (try_times <= 10):
            try:
                print("try page " + str(page) + "..." + "try_times:" + str(try_times))
                r = requests.get(real_url,timeout = 15)
                r.raise_for_status()
                request_finished = True
                r.encoding = r.apparent_encoding
                demo = r.text
                ranking_list_soup = BeautifulSoup(demo, "html.parser")

            except Exception as e:
                try_times += 1
                print(e)

        for info in ranking_list_soup.find_all('a', 'ranking-page-table__user-link-text js-usercard'):
            osuplayer_US.append(OsuPlayer(info.string, info.get('href')))
            fo = open('osu_ranking_list_US.txt', 'a+', encoding='utf-8')
            name = osuplayer_US[count].user_name
            link = osuplayer_US[count].user_url
            name = name.strip()
            link = link.strip()
            output_player = name + ':' + link + "\n"
            # print(output_player)
            fo.write(output_player)
            '''
            fo.write(osuplayer_US[count].user_name)
            fo.write(osuplayer_US[count].user_url)
            '''

            count += 1
        # html2txt = str(r.text)  # html content is fully transformed to str
        print("finish page " + str(page))

    print("RankingList function finished!")


class OsuPlayer:

    def __init__(self, total_score_ranked, accuracy, play_count, total_score, total_hits,
                 total_pp, global_rank, country_rank, recent_plays, top_plays, most_played, recent_24h,
                 fav_maps):
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

    def __init__(self, user_name, user_url):
        self.user_name = user_name
        self.user_url = user_url

    '''
    def printPlayerinfo(self):
        print("Total ranked socre %d" % OsuPlayer.total_score_ranked)
        print("Accuracy %d" % OsuPlayer.accuracy)
        print("Play Count %d" )
    '''


getRankingList(ranking_list_api)