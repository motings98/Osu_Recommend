from bs4 import BeautifulSoup
import requests
import random
import pyttanko as osu
import sys
import lib_data
import json
import os

def htmlOutput(url):
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    demo = r.text
    soup = BeautifulSoup(demo, "html.parser")
    f = open("html.txt", "a+", encoding='utf-8')
    f.write(soup.prettify())
    f.close()

'''
p = osu.parser()
# bmap = p.map(open("./lib/beatmaps/es.osu"))
bmap = p.map(open("https://osu.ppy.sh/osu/774965"))

stars = osu.diff_calc().calc(bmap)
print("%g stars" % stars.total)
print("%g stars" % stars.aim)

print(osu.ppv2(stars.aim, stars.speed, bmap=bmap))
'''



